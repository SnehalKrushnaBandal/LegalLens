import React from 'react';
import { Shield, Bell, LogOut, User, CheckCircle2, AlertTriangle, Scale } from 'lucide-react';
import { getOfficerProfile, logoutOfficer } from '../services/api';

export default function Navbar({ onOpenNotifications }) {
  const officer = getOfficerProfile() || {
    full_name: 'Inspector Rajesh Sharma',
    officer_id: 'LMO001',
    designation: 'Senior Legal Metrology Officer'
  };

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-40 shadow-md">
      {/* Top micro banner */}
      <div className="bg-gradient-to-r from-blue-900 via-indigo-950 to-slate-900 px-6 py-1 text-xs flex justify-between items-center text-slate-300 border-b border-slate-800/80">
        <div className="flex items-center gap-2">
          <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="font-medium text-slate-200">Government of India</span>
          <span className="text-slate-500">•</span>
          <span>Ministry of Consumer Affairs, Food & Public Distribution</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="bg-amber-500/20 text-amber-300 border border-amber-500/40 text-[10px] px-2 py-0.5 rounded font-mono font-semibold">
            PROTOTYPE / DEMO MODE (SIH 2026 - SIH26034)
          </span>
          <span className="text-slate-400 text-[11px] font-mono">v1.0.0</span>
        </div>
      </div>

      {/* Main Navbar */}
      <div className="px-6 py-3 flex justify-between items-center">
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center shadow-lg shadow-blue-900/40 border border-blue-400/30">
            <Scale className="w-6 h-6 text-amber-300" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-2">
                StegoAI Legal Metrology Inspector
                <span className="bg-blue-600/30 text-blue-300 text-xs px-2 py-0.5 rounded border border-blue-500/30 font-medium">
                  Packaged Commodities (PC) Rules, 2011
                </span>
              </h1>
            </div>
            <p className="text-xs text-slate-400">
              Automated AI-Assisted Product Declaration Verification & Compliance Engine
            </p>
          </div>
        </div>

        {/* Right Officer Card & Actions */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3 bg-slate-800/80 border border-slate-700 px-3.5 py-1.5 rounded-lg">
            <div className="w-8 h-8 rounded-full bg-blue-700/50 border border-blue-500/40 flex items-center justify-center text-blue-200">
              <User className="w-4 h-4" />
            </div>
            <div className="text-left">
              <div className="text-xs font-semibold text-white flex items-center gap-1.5">
                {officer.full_name}
                <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-[9px] px-1.5 py-0.2 rounded font-mono">
                  {officer.officer_id}
                </span>
              </div>
              <div className="text-[10px] text-slate-400">{officer.designation}</div>
            </div>
          </div>

          <button
            onClick={logoutOfficer}
            className="p-2 rounded-lg bg-slate-800 hover:bg-red-900/30 hover:text-red-300 hover:border-red-500/40 border border-slate-700 text-slate-300 transition-colors"
            title="Sign Out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
