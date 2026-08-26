import React, { useState } from 'react';
import { AlertTriangle, AlertCircle, CheckCircle2, XCircle, HelpCircle, ArrowRight } from 'lucide-react';

export default function ViolationCard({ 
  violation, 
  onUpdateStatus = () => {},
  onInspectZone = () => {}
}) {
  const [status, setStatus] = useState(violation.status || 'ACTIVE');

  const handleStatusChange = (newStatus) => {
    setStatus(newStatus);
    onUpdateStatus(violation.id, newStatus);
  };

  const getSeverityBadge = () => {
    switch (violation.severity) {
      case 'CRITICAL':
        return 'bg-red-700 text-white border-red-800';
      case 'HIGH':
        return 'bg-red-500/10 text-red-700 border-red-200';
      case 'MEDIUM':
        return 'bg-amber-500/10 text-amber-700 border-amber-200';
      default:
        return 'bg-blue-500/10 text-blue-700 border-blue-200';
    }
  };

  return (
    <div className={`p-4 rounded-xl border transition-all ${
      status === 'VERIFIED'
        ? 'bg-slate-50 border-slate-200 opacity-80'
        : status === 'DISMISSED'
        ? 'bg-slate-100 border-slate-300 opacity-60'
        : 'bg-white border-red-200 shadow-sm'
    }`}>
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <span className="p-1 rounded bg-red-100 text-red-600">
            <AlertTriangle className="w-4 h-4" />
          </span>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-800">
                {violation.category}
              </span>
              <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold border ${getSeverityBadge()}`}>
                {violation.severity} SEVERITY
              </span>
            </div>
            <div className="text-[11px] text-slate-500 font-mono">
              {violation.legal_reference || violation.rule_code || 'Legal Metrology (PC) Rules, 2011'}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-1.5">
          <span className="text-[11px] font-mono text-slate-500">
            Conf: {Math.round((violation.confidence || 0.95) * 100)}%
          </span>
        </div>
      </div>

      {/* Main Issue */}
      <div className="mt-3 text-xs text-slate-800 font-medium leading-relaxed">
        {violation.issue}
      </div>

      {/* Comparison Grid */}
      <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
        <div className="p-2.5 rounded-lg bg-red-50/60 border border-red-100">
          <span className="text-[10px] uppercase font-bold text-red-800 block mb-0.5">
            Detected on Package:
          </span>
          <span className="text-slate-800 font-medium">
            {violation.detected_value || 'Missing / Not Found'}
          </span>
        </div>

        <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="text-[10px] uppercase font-bold text-slate-600 block mb-0.5">
            Legal Requirement:
          </span>
          <span className="text-slate-700">
            {violation.expected_requirement}
          </span>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2">
        <button
          type="button"
          onClick={() => onInspectZone(violation.evidence_zone)}
          className="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1"
        >
          View Evidence Zone <ArrowRight className="w-3 h-3" />
        </button>

        <div className="flex items-center gap-1.5 text-xs">
          <button
            type="button"
            onClick={() => handleStatusChange('VERIFIED')}
            className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-colors flex items-center gap-1 ${
              status === 'VERIFIED'
                ? 'bg-emerald-600 text-white'
                : 'bg-slate-100 hover:bg-emerald-50 text-slate-700 hover:text-emerald-700 border border-slate-200'
            }`}
          >
            <CheckCircle2 className="w-3 h-3" />
            Mark Verified
          </button>
          
          <button
            type="button"
            onClick={() => handleStatusChange('MANUAL_REVIEW')}
            className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-colors flex items-center gap-1 ${
              status === 'MANUAL_REVIEW'
                ? 'bg-amber-600 text-white'
                : 'bg-slate-100 hover:bg-amber-50 text-slate-700 hover:text-amber-700 border border-slate-200'
            }`}
          >
            <HelpCircle className="w-3 h-3" />
            Manual Review
          </button>

          <button
            type="button"
            onClick={() => handleStatusChange('DISMISSED')}
            className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-colors flex items-center gap-1 ${
              status === 'DISMISSED'
                ? 'bg-slate-600 text-white'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-600 border border-slate-200'
            }`}
          >
            <XCircle className="w-3 h-3" />
            Dismiss
          </button>
        </div>
      </div>
    </div>
  );
}
