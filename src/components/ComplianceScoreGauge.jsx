import React from 'react';
import { ShieldCheck, AlertOctagon, HelpCircle, CheckCircle2 } from 'lucide-react';

export default function ComplianceScoreGauge({ 
  score = 0, 
  status = 'PENDING', 
  breakdown = {} 
}) {
  const getStatusColor = () => {
    switch (status) {
      case 'COMPLIANT':
        return {
          bg: 'bg-emerald-50 border-emerald-200 text-emerald-800',
          badge: 'bg-emerald-600 text-white',
          text: 'text-emerald-600',
          bar: 'bg-emerald-500',
          icon: CheckCircle2,
          label: 'COMPLIANT'
        };
      case 'NON-COMPLIANT':
        return {
          bg: 'bg-red-50 border-red-200 text-red-800',
          badge: 'bg-red-600 text-white',
          text: 'text-red-600',
          bar: 'bg-red-500',
          icon: AlertOctagon,
          label: 'NON-COMPLIANT'
        };
      case 'NEEDS_MANUAL_VERIFICATION':
      default:
        return {
          bg: 'bg-amber-50 border-amber-200 text-amber-800',
          badge: 'bg-amber-500 text-white',
          text: 'text-amber-600',
          bar: 'bg-amber-500',
          icon: HelpCircle,
          label: 'MANUAL VERIFICATION REQUIRED'
        };
    }
  };

  const statusConfig = getStatusColor();
  const StatusIcon = statusConfig.icon;

  const categories = [
    { label: 'Mandatory Declarations', key: 'mandatory_declarations', weight: '30%' },
    { label: 'Net Quantity Standard Units', key: 'quantity_declaration', weight: '20%' },
    { label: 'MRP & Tax Declaration', key: 'mrp_compliance', weight: '20%' },
    { label: 'Consumer Care Cell Details', key: 'consumer_care', weight: '20%' },
    { label: 'Readability & Font Estimation', key: 'readability_formatting', weight: '10%' },
  ];

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-5">
      {/* Top Score & Status Header */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pb-4 border-b border-slate-100">
        <div className="flex items-center gap-4">
          <div className="relative flex items-center justify-center w-20 h-20 rounded-full bg-slate-900 text-white shadow-inner">
            <div className="text-center">
              <span className="text-2xl font-black tracking-tight">{Math.round(score)}</span>
              <span className="text-[10px] text-slate-400 block -mt-1 font-semibold">/100</span>
            </div>
            {/* SVG circle meter */}
            <svg className="absolute inset-0 w-full h-full -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-slate-800"
                strokeWidth="3.5"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                className={score >= 85 ? 'text-emerald-500' : score >= 70 ? 'text-amber-500' : 'text-red-500'}
                strokeDasharray={`${score}, 100`}
                strokeWidth="3.5"
                strokeLinecap="round"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
          </div>

          <div>
            <span className="text-xs uppercase tracking-wider font-bold text-slate-400">
              Overall Legal Metrology Compliance
            </span>
            <div className="flex items-center gap-2 mt-1">
              <span className={`px-3 py-1 rounded-md text-xs font-bold flex items-center gap-1.5 shadow-sm ${statusConfig.badge}`}>
                <StatusIcon className="w-3.5 h-3.5" />
                {statusConfig.label}
              </span>
            </div>
          </div>
        </div>

        <div className="text-right text-xs text-slate-500 hidden sm:block">
          <div>Evaluated against</div>
          <span className="font-semibold text-slate-700">Legal Metrology Rules, 2011</span>
        </div>
      </div>

      {/* Category Breakdown Bars */}
      <div className="space-y-3">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
          Compliance Category Breakdown
        </h4>

        {categories.map((cat) => {
          const val = breakdown[cat.key] !== undefined ? breakdown[cat.key] : 100;
          const barColor = val >= 90 ? 'bg-emerald-500' : val >= 70 ? 'bg-amber-500' : 'bg-red-500';

          return (
            <div key={cat.key} className="space-y-1">
              <div className="flex justify-between items-center text-xs">
                <span className="font-medium text-slate-700">
                  {cat.label} <span className="text-slate-400 text-[11px]">({cat.weight})</span>
                </span>
                <span className="font-mono font-semibold text-slate-800">{val}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${barColor}`}
                  style={{ width: `${val}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
