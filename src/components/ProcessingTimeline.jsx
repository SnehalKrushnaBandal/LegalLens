import React from 'react';
import { CheckCircle2, Loader2, Sparkles, Binary, Cpu, Scale, FileSpreadsheet } from 'lucide-react';

const stages = [
  { id: 1, name: 'Image Preprocessing', desc: 'Grayscale & contrast enhancement', icon: Sparkles },
  { id: 2, name: 'Text Detection & OCR', desc: 'Optical character extraction', icon: Binary },
  { id: 3, name: 'Declaration Identification', desc: 'Rule 6 entity recognition', icon: FileSpreadsheet },
  { id: 4, name: 'Legal Rule Validation', desc: 'Metrology rules evaluation', icon: Scale },
  { id: 5, name: 'Compliance Calculation', desc: 'Scoring & evidence annotation', icon: Cpu },
];

export default function ProcessingTimeline({ currentStage = 1, isComplete = false }) {
  return (
    <div className="bg-slate-900 rounded-xl p-6 border border-slate-800 text-white shadow-xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-sm font-bold tracking-tight text-white flex items-center gap-2">
            <Cpu className="w-4 h-4 text-blue-400 animate-pulse" />
            AI & Rule Engine Processing Pipeline
          </h3>
          <p className="text-xs text-slate-400">
            Analyzing package label against Legal Metrology (Packaged Commodities) Rules, 2011
          </p>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-blue-900/50 border border-blue-500/40 text-blue-300">
          {isComplete ? 'Analysis Completed' : `Stage ${currentStage} of 5`}
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-5 gap-3 relative">
        {stages.map((st) => {
          const isDone = isComplete || currentStage > st.id;
          const isCurrent = !isComplete && currentStage === st.id;
          const Icon = st.icon;

          return (
            <div
              key={st.id}
              className={`p-3 rounded-lg border transition-all ${
                isDone
                  ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-300'
                  : isCurrent
                  ? 'bg-blue-950/60 border-blue-500 text-blue-200 ring-2 ring-blue-500/20 animate-pulse'
                  : 'bg-slate-800/40 border-slate-700/60 text-slate-500'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <Icon className={`w-4 h-4 ${isDone ? 'text-emerald-400' : isCurrent ? 'text-blue-400' : 'text-slate-500'}`} />
                {isDone ? (
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                ) : isCurrent ? (
                  <Loader2 className="w-3.5 h-3.5 text-blue-400 animate-spin" />
                ) : (
                  <span className="text-[10px] font-mono text-slate-600">0{st.id}</span>
                )}
              </div>
              <div className="text-xs font-bold truncate">{st.name}</div>
              <div className="text-[10px] text-slate-400 leading-tight mt-0.5 truncate">{st.desc}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
