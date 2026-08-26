import os
import time
import cv2
import numpy as np
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from model import classify_message
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Use absolute path for UPLOAD_FOLDER to avoid CWD issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_ROOT = os.path.join(BASE_DIR, 'uploads')
INPUT_FOLDER = os.path.join(UPLOAD_ROOT, 'input')
OUTPUT_FOLDER = os.path.join(UPLOAD_ROOT, 'output')
TEMP_FOLDER = os.path.join(UPLOAD_ROOT, 'temp')

for folder in [INPUT_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['INPUT_FOLDER'] = INPUT_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['TEMP_FOLDER'] = TEMP_FOLDER

DELIMITER = "1111111111111110"
SIGNATURE = "01010101010101010101010101010101" # 32-bit robust signature

def check_for_signature(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    if not ret: 
        print(f"CheckSig: Could not read first frame of {video_path}")
        return False
    
    # Check the first 64 pixels for the signature to allow for minor alignment shifts
    height, width, _ = frame.shape
    check_len = min(64, width)
    
    lsbs = (frame[0, :check_len, 0] & 1).astype(np.uint8)
    found_bits = bytes(lsbs + ord('0')).decode()
    print(f"CheckSig: Found bits: {found_bits}")
    
    if SIGNATURE in found_bits:
        print("CheckSig: MATCH FOUND. Blocking re-encoding.")
        return True
    return False

def message_to_bin(message):
    return ''.join([format(ord(i), "08b") for i in message])

def bin_to_message(binary_data):
    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
    decoded_message = ""
    for byte in all_bytes:
        if len(byte) < 8: break
        decoded_message += chr(int(byte, 2))
    return decoded_message

def encode_video(input_path, output_path, secret_message):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        return False, "Could not open video."

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Use FFV1 codec for lossless encoding in AVI container
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        cap.release()
        return False, "Failed to initialize VideoWriter. Check if codec 'FFV1' is supported."

    # Prepend signature to the message
    binary_msg = SIGNATURE + message_to_bin(secret_message) + DELIMITER
    data_idx = 0
    msg_len = len(binary_msg)

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if data_idx < msg_len:
            # Vectorized LSB embedding
            blue_channel = frame[:, :, 0].flatten()
            bits_to_embed = min(len(blue_channel), msg_len - data_idx)
            
            # Efficient conversion of binary string to numpy array
            bits_slice = binary_msg[data_idx:data_idx + bits_to_embed]
            bits_array = np.frombuffer(bits_slice.encode(), dtype=np.uint8) - ord('0')
            
            blue_channel[:bits_to_embed] = (blue_channel[:bits_to_embed] & 0xFE) | bits_array
            frame[:, :, 0] = blue_channel.reshape((height, width))
            
            data_idx += bits_to_embed
            
        out.write(frame)
        frame_count += 1
        
        # Ensure we write at least 30 frames to make the file playable in players like VLC
        if data_idx >= msg_len and frame_count >= 30:
            break

    cap.release()
    out.release()
    return True, None

def decode_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, "Could not open video."

    binary_data_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Vectorized extraction of LSB from blue channel
        lsbs = (frame[:, :, 0] & 1).flatten().astype(np.uint8)
        # Efficiently convert bit array to string
        chunk = bytes(lsbs + ord('0')).decode()
        binary_data_list.append(chunk)
        
        # Check for delimiter in the accumulated binary data
        full_string = "".join(binary_data_list)
        if DELIMITER in full_string:
            # Skip the signature (first 16 bits) and extract up to delimiter
            msg_bits = full_string[len(SIGNATURE):]
            end_idx = msg_bits.find(DELIMITER)
            cap.release()
            return bin_to_message(msg_bits[:end_idx]), None

    cap.release()
    return None, "Delimiter not found. No hidden message."

@app.route('/encode', methods=['POST'])
def encode():
    if 'video' not in request.files or 'message' not in request.form:
        return jsonify({"error": "Missing video or message"}), 400

    video_file = request.files['video']
    message = request.form['message']

    # ML Classification
    classification = classify_message(message)
    if classification == 'spam':
        return jsonify({"error": "Spam message detected! Message blocked by AI."}), 403

    timestamp = int(time.time())
    filename = secure_filename(video_file.filename)
    input_filename = f"{timestamp}_{filename}"
    input_path = os.path.join(app.config['INPUT_FOLDER'], input_filename)
    
    output_filename = f"encoded_{timestamp}_{os.path.splitext(filename)[0]}.avi"
    output_filename = output_filename.replace(" ", "_")
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    
    video_file.save(input_path)

    # Protection: Prevent double encoding
    if check_for_signature(input_path):
        os.remove(input_path) # Cleanup
        return jsonify({"error": "Security Alert: This video already contains a hidden message. Re-encoding is blocked to prevent data corruption."}), 403

    success, error = encode_video(input_path, output_path, message)
    
    # Cleanup: Remove the original input file after encoding
    if os.path.exists(input_path):
        os.remove(input_path)

    if not success:
        return jsonify({"error": error}), 500

    return send_file(output_path, as_attachment=True)

@app.route('/decode', methods=['POST'])
def decode():
    if 'video' not in request.files:
        return jsonify({"error": "Missing video file"}), 400

    video_file = request.files['video']
    timestamp = int(time.time())
    filename = secure_filename(video_file.filename)
    video_path = os.path.join(app.config['TEMP_FOLDER'], f"decode_{timestamp}_{filename}")
    video_file.save(video_path)

    message, error = decode_video(video_path)
    
    # Cleanup: Remove decoded video after extraction
    if os.path.exists(video_path):
        os.remove(video_path)

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
