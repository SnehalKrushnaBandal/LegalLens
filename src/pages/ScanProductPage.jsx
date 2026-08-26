import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Upload, 
  Camera, 
  Sparkles, 
  CheckCircle2, 
  AlertTriangle, 
  FileText, 
  Download, 
  RotateCcw, 
  Eye, 
  Layers, 
  Edit3, 
  Save, 
  Scale,
  Cpu,
  Info,
  Check
} from 'lucide-react';
import { api } from '../services/api';
import ProcessingTimeline from '../components/ProcessingTimeline';
import BoundingBoxViewer from '../components/BoundingBoxViewer';
import ComplianceScoreGauge from '../components/ComplianceScoreGauge';
import ViolationCard from '../components/ViolationCard';
import ReadabilityBadge from '../components/ReadabilityBadge';

const DEMO_PRESETS = [
  { id: 'basmati_rice', name: 'Premium Basmati Rice (5kg)', category: 'Packaged Food / Rice', compliance: 'Compliant' },
  { id: 'biscuits', name: 'Butter Delight Biscuits (200g)', category: 'Bakery', compliance: 'Non-Compliant (Missing Helpline)' },
  { id: 'cooking_oil', name: 'Pure Mustard Cooking Oil (1L)', category: 'Edible Oils', compliance: 'Non-Compliant (MRP Tax Phrase Missing)' },
  { id: 'detergent', name: 'Active Clean Detergent (1kg)', category: 'Household', compliance: 'Non-Compliant (Non-SI Units "GMS")' },
  { id: 'shampoo', name: 'Herbal Glow Shampoo (180ml)', category: 'Cosmetics', compliance: 'Non-Compliant (Incomplete Address)' },
  { id: 'garam_masala', name: 'Royal Garam Masala (100g)', category: 'Spices', compliance: 'Manual Verification (Date Ambiguous)' },
];

export default function ScanProductPage() {
  const navigate = useNavigate();

  // Scan & Upload State
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [demoPreset, setDemoPreset] = useState('basmati_rice');
  const [uploadedData, setUploadedData] = useState(null);

  // Processing State
  const [processing, setProcessing] = useState(false);
  const [currentStage, setCurrentStage] = useState(1);
  const [analysisResult, setAnalysisResult] = useState(null);

  // Editable Declarations
  const [declarations, setDeclarations] = useState([]);
  const [highlightedField, setHighlightedField] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  // Final Compliance Results
  const [complianceResult, setComplianceResult] = useState(null);
  const [evaluatingRules, setEvaluatingRules] = useState(false);
  const [officerRemarks, setOfficerRemarks] = useState('');
  const [savedInspectionId, setSavedInspectionId] = useState(null);

  // Handle File Selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setDemoPreset('');
      resetAnalysis();
    }
  };

  const handleSelectDemoPreset = (presetId) => {
    setDemoPreset(presetId);
    setSelectedFile(null);
    setPreviewUrl(null);
    resetAnalysis();
  };

  const resetAnalysis = () => {
    setUploadedData(null);
    setAnalysisResult(null);
    setDeclarations([]);
    setComplianceResult(null);
    setSavedInspectionId(null);
  };

  // Step 1: Upload and Preprocess
  const handleAnalyzeClick = async () => {
    setProcessing(true);
    setCurrentStage(1);

    try {
      const formData = new FormData();
      if (selectedFile) {
        formData.append('file', selectedFile);
      } else if (demoPreset) {
        formData.append('demo_product_id', demoPreset);
      }

      // Stage 1: Upload
      const uploadRes = await api.uploadProduct(formData);
      setUploadedData(uploadRes);
      setCurrentStage(2);

      // Simulate step progression for smooth visual experience
      await new Promise(r => setTimeout(r, 600));
      setCurrentStage(3);

      // Stage 2: OCR Extraction
      const analyzeForm = new FormData();
      analyzeForm.append('raw_image_path', uploadRes.raw_image_path);
      if (uploadRes.demo_product_id) {
        analyzeForm.append('demo_product_id', uploadRes.demo_product_id);
      }
      analyzeForm.append('product_name', uploadRes.product_name);
      analyzeForm.append('category', uploadRes.category);

      const result = await api.analyzeProduct(analyzeForm);
      setAnalysisResult(result);
      setDeclarations(result.declarations);

      await new Promise(r => setTimeout(r, 500));
      setCurrentStage(5);
    } catch (err) {
      alert('Error during OCR analysis: ' + err.message);
    } finally {
      setProcessing(false);
    }
  };

  // Handle Declaration Text Editing
  const handleDeclarationChange = (fieldName, newValue) => {
    setDeclarations(prev => prev.map(dec => {
      if (dec.field_name === fieldName) {
        return {
          ...dec,
          detected_value: newValue,
          is_present: Boolean(newValue && newValue.trim().length > 0 && !newValue.toLowerCase().includes('missing')),
          is_officer_edited: true
        };
      }
      return dec;
    }));
  };

  // Step 2: Run Configurable Rule Engine
  const handleRunComplianceCheck = async () => {
    setEvaluatingRules(true);

    try {
      const payload = {
        raw_image_path: uploadedData?.raw_image_path || '',
        evidence_image_path: analysisResult?.evidence_image_path || '',
        product_name: uploadedData?.product_name || 'Packaged Commodity',
        category: uploadedData?.category || 'General Food / Grocery',
        declarations: declarations,
        evidence_items: analysisResult?.evidence_items || [],
        demo_product_id: uploadedData?.demo_product_id,
        remarks: officerRemarks || 'Screening conducted by inspecting officer.'
      };

      const result = await api.createInspection(payload);
      setComplianceResult(result);
      setSavedInspectionId(result.id);
    } catch (err) {
      alert('Failed to execute compliance rule evaluation: ' + err.message);
    } finally {
      setEvaluatingRules(false);
    }
  };

  // Download PDF Report
  const handleDownloadReport = async () => {
    if (!savedInspectionId) return;
    try {
      window.open(api.getReportDownloadUrl(savedInspectionId), '_blank');
    } catch (err) {
      alert('Could not download inspection report: ' + err.message);
    }
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Header Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-600">
            <Scale className="w-4 h-4" />
            <span>Legal Metrology Packaged Commodities (Rules 2011)</span>
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            Scan & Verify Packaged Product
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Extract mandatory declarations, evaluate rule compliance, and inspect visual evidence.
          </p>
        </div>

        {complianceResult && (
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={handleDownloadReport}
              className="px-4 py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-2 shadow-md shadow-emerald-600/30 transition-all"
            >
              <Download className="w-4 h-4" />
              Download Official PDF Report
            </button>
            <button
              type="button"
              onClick={resetAnalysis}
              className="px-3.5 py-2.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold flex items-center gap-1.5 transition-all"
            >
              <RotateCcw className="w-4 h-4" />
              Scan Another
            </button>
          </div>
        )}
      </div>

      {/* Upload & Demo Product Selection Section */}
      {!analysisResult && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Upload Box */}
          <div className="lg:col-span-2 bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
              <Upload className="w-4 h-4 text-blue-600" />
              Upload Product Packaging Image
            </h3>

            <div className="border-2 border-dashed border-slate-300 hover:border-blue-500 rounded-xl p-8 text-center transition-all bg-slate-50/50 hover:bg-blue-50/20">
              <input
                type="file"
                id="package-file-input"
                accept="image/jpeg,image/png,image/jpg"
                onChange={handleFileChange}
                className="hidden"
              />
              <label htmlFor="package-file-input" className="cursor-pointer block space-y-3">
                <div className="w-14 h-14 mx-auto rounded-full bg-blue-100/80 text-blue-600 flex items-center justify-center shadow-inner">
                  <Upload className="w-7 h-7" />
                </div>
                <div>
                  <span className="text-sm font-bold text-blue-600 hover:text-blue-700">
                    Click to upload package image
                  </span>
                  <span className="text-sm text-slate-500"> or drag and drop</span>
                  <p className="text-xs text-slate-400 mt-1">Supports JPG, JPEG, PNG (Max: 10MB)</p>
                </div>
              </label>
            </div>

            {previewUrl && (
              <div className="p-3 bg-slate-100 rounded-xl flex items-center justify-between text-xs">
                <span className="font-semibold text-slate-700 truncate max-w-xs">{selectedFile?.name}</span>
                <span className="text-emerald-600 font-bold flex items-center gap-1">
                  <Check className="w-3.5 h-3.5" /> Ready for OCR
                </span>
              </div>
            )}
          </div>

          {/* Quick Demo Products Selector */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-500" />
                Select Demo Packaged Commodity
              </h3>
              <p className="text-[11px] text-slate-400 mt-0.5">
                Instant test datasets for hackathon evaluation
              </p>
            </div>

            <div className="space-y-2 max-h-[280px] overflow-y-auto custom-scrollbar pr-1">
              {DEMO_PRESETS.map((preset) => {
                const isSelected = demoPreset === preset.id;
                return (
                  <button
                    key={preset.id}
                    type="button"
                    onClick={() => handleSelectDemoPreset(preset.id)}
                    className={`w-full text-left p-3 rounded-xl border text-xs transition-all ${
                      isSelected
                        ? 'bg-blue-50/80 border-blue-500 ring-2 ring-blue-500/20 font-semibold'
                        : 'bg-slate-50/50 border-slate-200 hover:bg-slate-100 text-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-900">{preset.name}</span>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono ${
                        preset.compliance.startsWith('Compliant') ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {preset.compliance.split(' ')[0]}
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-500 mt-0.5">{preset.category}</div>
                    <div className="text-[10px] text-slate-400 font-mono mt-1">{preset.compliance}</div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Analyze Button */}
      {!analysisResult && (
        <div className="flex justify-end">
          <button
            type="button"
            onClick={handleAnalyzeClick}
            disabled={processing || (!selectedFile && !demoPreset)}
            className="px-8 py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-sm rounded-xl shadow-lg shadow-blue-600/30 flex items-center gap-2.5 transition-all disabled:opacity-50"
          >
            <Cpu className="w-5 h-5" />
            {processing ? 'Processing OCR & Text Detection...' : 'Analyze Product Packaging'}
          </button>
        </div>
      )}

      {/* Processing Timeline Indicator */}
      {processing && (
        <ProcessingTimeline currentStage={currentStage} isComplete={currentStage === 5} />
      )}

      {/* OCR Results & Human-In-The-Loop Declaration Review */}
      {analysisResult && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left: Interactive Bounding Box Vision Evidence */}
            <div className="lg:col-span-5 flex flex-col">
              <BoundingBoxViewer
                originalImage={uploadedData?.image_path}
                evidenceImage={analysisResult?.evidence_image_path}
                declarations={declarations}
                highlightedField={highlightedField}
                onSelectField={(field) => setHighlightedField(field)}
              />
            </div>

            {/* Right: Mandatory Declarations Table (Editable) */}
            <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div>
                  <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <FileText className="w-4 h-4 text-blue-600" />
                    Mandatory Declarations Extraction (Rule 6)
                  </h3>
                  <p className="text-xs text-slate-500">
                    Review and correct extracted values before legal rule validation
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-mono px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 rounded">
                    Human-in-the-Loop OCR
                  </span>
                </div>
              </div>

              {/* Declarations Extraction Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider text-[10px] border-b border-slate-200">
                    <tr>
                      <th className="px-3 py-2">Declaration</th>
                      <th className="px-3 py-2">Extracted / Verified Value</th>
                      <th className="px-3 py-2">Status</th>
                      <th className="px-3 py-2">Conf.</th>
                      <th className="px-3 py-2">Readability</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {declarations.map((dec) => {
                      const isHighlighted = highlightedField === dec.field_name;
                      return (
                        <tr
                          key={dec.field_name}
                          onMouseEnter={() => setHighlightedField(dec.field_name)}
                          className={`transition-colors ${
                            isHighlighted ? 'bg-blue-50/70' : 'hover:bg-slate-50/60'
                          }`}
                        >
                          <td className="px-3 py-2 font-bold text-slate-800 whitespace-nowrap">
                            {dec.field_name.replace('_', ' ').toUpperCase()}
                          </td>
                          <td className="px-3 py-2">
                            <input
                              type="text"
                              value={dec.detected_value || ''}
                              onChange={(e) => handleDeclarationChange(dec.field_name, e.target.value)}
                              placeholder="Missing declaration"
                              className="w-full px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded font-medium text-slate-900 focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-xs transition-all"
                            />
                          </td>
                          <td className="px-3 py-2 whitespace-nowrap">
                            {dec.is_present && !String(dec.detected_value || '').toLowerCase().includes('missing') ? (
                              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                                Present
                              </span>
                            ) : (
                              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-50 text-red-700 border border-red-200">
                                Violation
                              </span>
                            )}
                          </td>
                          <td className="px-3 py-2 font-mono text-slate-600 whitespace-nowrap">
                            {Math.round((dec.confidence || 0.95) * 100)}%
                          </td>
                          <td className="px-3 py-2 whitespace-nowrap">
                            <ReadabilityBadge
                              fontSizePx={dec.estimated_font_size_px}
                              status={dec.readability_status}
                            />
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {/* Officer Note & Action button */}
              <div className="pt-3 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3">
                <span className="text-[11px] text-slate-500 italic">
                  * Extracted fields are editable by officer to rectify OCR errors before rule validation.
                </span>

                <button
                  type="button"
                  onClick={handleRunComplianceCheck}
                  disabled={evaluatingRules}
                  className="px-6 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-md shadow-blue-600/30 flex items-center gap-2 transition-all"
                >
                  <Scale className="w-4 h-4" />
                  {evaluatingRules ? 'Evaluating Rules...' : 'Run Legal Metrology Rule Check'}
                </button>
              </div>
            </div>
          </div>

          {/* Compliance Results Section */}
          {complianceResult && (
            <div className="space-y-6 pt-4 border-t border-slate-200">
              <h3 className="text-lg font-black text-slate-900 tracking-tight flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                Compliance Check & Violation Findings
              </h3>

              {/* Compliance Gauge & Score Card */}
              <ComplianceScoreGauge
                score={complianceResult.compliance_score}
                status={complianceResult.compliance_status}
                breakdown={complianceResult.score_breakdown}
              />

              {/* Violations List */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                    Detected Legal Metrology Violations ({complianceResult.violations?.length || 0})
                  </h4>
                  <span className="text-xs text-slate-500">
                    Review and verify findings for official inspection log
                  </span>
                </div>

                {complianceResult.violations?.length === 0 ? (
                  <div className="p-6 rounded-xl bg-emerald-50 border border-emerald-200 text-center text-emerald-800 font-medium text-xs">
                    <CheckCircle2 className="w-8 h-8 mx-auto text-emerald-600 mb-2" />
                    No violations detected. Product meets all mandatory declarations under Legal Metrology Rules, 2011.
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {complianceResult.violations.map((viol) => (
                      <ViolationCard
                        key={viol.id}
                        violation={viol}
                        onUpdateStatus={(vId, st) => api.updateViolationStatus(complianceResult.id, vId, st)}
                        onInspectZone={() => setHighlightedField(viol.category.toLowerCase())}
                      />
                    ))}
                  </div>
                )}
              </div>

              {/* Officer Remarks & Save / Download Actions */}
              <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm space-y-4">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Officer Inspection Remarks & Final Action
                </h4>

                <textarea
                  rows={2}
                  value={officerRemarks}
                  onChange={(e) => setOfficerRemarks(e.target.value)}
                  placeholder="Enter official notes, compounding instructions, or verification remarks..."
                  className="w-full p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />

                <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                  <div className="text-[11px] text-slate-500">
                    Inspection ID: <span className="font-mono font-bold text-slate-800">{complianceResult.inspection_number}</span>
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      type="button"
                      onClick={handleDownloadReport}
                      className="px-5 py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-2 shadow-md shadow-emerald-600/30 transition-all"
                    >
                      <Download className="w-4 h-4" />
                      Generate & Download PDF Report
                    </button>
                    <button
                      type="button"
                      onClick={() => navigate('/inspections')}
                      className="px-4 py-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-all"
                    >
                      View in Inspection History
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
