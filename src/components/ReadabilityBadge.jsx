import React from 'react';
import { Type, AlertCircle, CheckCircle2, HelpCircle } from 'lucide-react';

export default function ReadabilityBadge({ fontSizePx = 14, status = 'PASS' }) {
  const getBadgeStyle = () => {
    switch (status) {
      case 'PASS':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'WARNING':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'MANUAL_VERIFICATION':
      default:
        return 'bg-amber-100 text-amber-800 border-amber-300';
    }
  };

  return (
    <div className="inline-flex items-center gap-1.5 group relative">
      <span className={`px-2 py-0.5 rounded text-[11px] font-mono font-medium border flex items-center gap-1 ${getBadgeStyle()}`}>
        <Type className="w-3 h-3" />
        {fontSizePx ? `${Math.round(fontSizePx)}px` : 'N/A'} • {status.replace('_', ' ')}
      </span>

      {/* Floating legal guidance tooltip */}
      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1.5 hidden group-hover:block w-64 p-2 bg-slate-900 text-white text-[10px] rounded-lg shadow-xl border border-slate-700 z-50 pointer-events-none leading-tight">
        <div className="font-semibold text-amber-300 mb-0.5 flex items-center gap-1">
          <AlertCircle className="w-3 h-3 shrink-0" />
          Statutory Measurement Note:
        </div>
        Estimated digital readability result. Legal font-size compliance (Rule 7) requires physical calibrated measurement on actual packaging dimensions.
      </div>
    </div>
  );
}
