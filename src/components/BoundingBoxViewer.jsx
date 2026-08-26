import React, { useState } from 'react';
import { Eye, Layers, ZoomIn, Info, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function BoundingBoxViewer({ 
  originalImage, 
  evidenceImage, 
  declarations = [],
  highlightedField = null,
  onSelectField = () => {}
}) {
  const [viewMode, setViewMode] = useState('annotated'); // 'annotated' or 'original'
  const [selectedBox, setSelectedBox] = useState(null);

  const activeImage = viewMode === 'annotated' && evidenceImage ? evidenceImage : originalImage;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-full">
      {/* Header Toolbar */}
      <div className="px-4 py-3 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-blue-600" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
            Package Visual Evidence & Bounding Boxes
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <div className="bg-slate-200 p-0.5 rounded-lg flex text-xs">
            <button
              type="button"
              onClick={() => setViewMode('annotated')}
              className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                viewMode === 'annotated'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Annotated Vision
            </button>
            <button
              type="button"
              onClick={() => setViewMode('original')}
              className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                viewMode === 'original'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Raw Image
            </button>
          </div>
        </div>
      </div>

      {/* Image Preview Canvas */}
      <div className="relative flex-1 min-h-[380px] max-h-[500px] bg-slate-950 flex items-center justify-center p-4 overflow-hidden select-none">
        {activeImage ? (
          <div className="relative max-h-[460px] max-w-full inline-block group">
            <img
              src={activeImage}
              alt="Packaged Commodity"
              className="max-h-[460px] w-auto rounded-lg shadow-2xl object-contain border border-slate-800"
            />

            {/* Interactive Overlay Bounding Boxes (if original view is selected or interactive mode active) */}
            {viewMode === 'original' && declarations.map((dec, idx) => {
              const box = dec.raw_bounding_box;
              if (!box) return null;

              const isHighlighted = highlightedField === dec.field_name || selectedBox === dec.field_name;
              const isOk = dec.is_present && dec.readability_status === 'PASS';
              const isWarn = dec.readability_status === 'MANUAL_VERIFICATION' || dec.readability_status === 'WARNING';
              
              const borderColor = !dec.is_present 
                ? 'border-red-500 bg-red-500/20 text-red-200' 
                : isWarn 
                ? 'border-amber-400 bg-amber-400/20 text-amber-200' 
                : 'border-emerald-400 bg-emerald-400/20 text-emerald-200';

              return (
                <div
                  key={idx}
                  onClick={() => {
                    setSelectedBox(dec.field_name);
                    onSelectField(dec.field_name);
                  }}
                  onMouseEnter={() => setSelectedBox(dec.field_name)}
                  onMouseLeave={() => setSelectedBox(null)}
                  style={{
                    position: 'absolute',
                    left: `${box.x}%`,
                    top: `${box.y}%`,
                    width: `${box.w}%`,
                    height: `${box.h}%`,
                  }}
                  className={`border-2 cursor-pointer transition-all duration-200 rounded flex items-start justify-start p-1 ${borderColor} ${
                    isHighlighted ? 'ring-4 ring-blue-400 ring-offset-1 z-20 scale-[1.02]' : 'opacity-70 hover:opacity-100 z-10'
                  }`}
                  title={`${dec.field_name.replace('_', ' ').toUpperCase()}: ${dec.detected_value || 'Missing'}`}
                >
                  <span className="text-[9px] font-bold px-1 rounded bg-slate-900/90 shadow text-white truncate max-w-full">
                    {dec.field_name.replace('_', ' ').toUpperCase()}
                  </span>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center text-slate-500 space-y-2">
            <Info className="w-8 h-8 mx-auto text-slate-600" />
            <p className="text-xs">No package image uploaded yet.</p>
          </div>
        )}
      </div>

      {/* Legend & Vision Metrics */}
      <div className="px-4 py-2.5 bg-slate-50 border-t border-slate-200 text-xs flex flex-wrap items-center justify-between gap-2 text-slate-600">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
            Compliant Zone
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500 inline-block"></span>
            Missing / Violation Zone
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span>
            Readability / Ambiguous
          </span>
        </div>
        <div className="text-[11px] text-slate-500 font-mono">
          AI OCR Zone Detection • Click any box to inspect
        </div>
      </div>
    </div>
  );
}
