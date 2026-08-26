import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Scale, Lock, User, AlertCircle, ArrowRight, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

export default function LoginPage() {
  const navigate = useNavigate();
  const [officerId, setOfficerId] = useState('LMO001');
  const [password, setPassword] = useState('admin123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await api.login(officerId, password);
      navigate('/');
    } catch (err) {
      setError(err.message || 'Invalid Officer credentials. Please check and retry.');
    } finally {
      setLoading(false);
    }
  };

  const fillDemoCreds = () => {
    setOfficerId('LMO001');
    setPassword('admin123');
    setError('');
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-between relative overflow-hidden font-sans text-slate-100">
      {/* Background ambient lighting */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />

      {/* Top Header Bar */}
      <header className="px-8 py-4 border-b border-slate-800/80 bg-slate-900/60 backdrop-blur flex justify-between items-center z-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-600/30">
            <Scale className="w-6 h-6 text-amber-300" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white tracking-tight">
              Legal Metrology Compliance Enforcement Portal
            </h1>
            <p className="text-xs text-slate-400">
              Department of Consumer Affairs • Government of India
            </p>
          </div>
        </div>

        <div className="hidden sm:flex items-center gap-2 text-xs text-amber-300 bg-amber-500/10 border border-amber-500/30 px-3 py-1 rounded-md font-mono">
          <span>SIH 2026 PROTOTYPE (SIH26034)</span>
        </div>
      </header>

      {/* Main Login Card */}
      <main className="flex-1 flex items-center justify-center p-4 z-10">
        <div className="w-full max-w-md bg-slate-900/90 border border-slate-800 rounded-2xl p-8 shadow-2xl backdrop-blur relative">
          {/* Official Emblem Banner */}
          <div className="text-center mb-6">
            <div className="inline-flex p-3 rounded-full bg-blue-500/10 border border-blue-400/20 text-blue-400 mb-3 shadow-inner">
              <Shield className="w-8 h-8" />
            </div>
            <h2 className="text-xl font-bold text-white">Officer Authentication</h2>
            <p className="text-xs text-slate-400 mt-1">
              Legal Metrology (Packaged Commodities) Rules, 2011 Inspection System
            </p>
          </div>

          {/* Quick Demo Credentials Pill */}
          <div className="mb-6 p-3 rounded-xl bg-blue-950/50 border border-blue-500/30 text-xs text-slate-300 flex items-center justify-between">
            <div>
              <span className="text-amber-300 font-semibold block text-[11px]">Demo Inspector Login:</span>
              <span className="font-mono text-slate-300">ID: LMO001 • Pass: admin123</span>
            </div>
            <button
              type="button"
              onClick={fillDemoCreds}
              className="px-2.5 py-1 rounded bg-blue-600 hover:bg-blue-500 text-white font-medium text-[11px] transition-colors"
            >
              Auto Fill
            </button>
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-lg bg-red-950/60 border border-red-500/40 text-red-300 text-xs flex items-start gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Officer ID / Badge Number
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <User className="w-4 h-4" />
                </div>
                <input
                  type="text"
                  required
                  value={officerId}
                  onChange={(e) => setOfficerId(e.target.value)}
                  placeholder="e.g. LMO001"
                  className="w-full pl-9 pr-4 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-mono transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-9 pr-4 py-2.5 bg-slate-950 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-mono transition-all"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-sm rounded-lg shadow-lg shadow-blue-600/30 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
            >
              {loading ? (
                <span>Authenticating Officer...</span>
              ) : (
                <>
                  <span>Access Enforcement Dashboard</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        </div>
      </main>

      {/* Footer */}
      <footer className="px-8 py-3 border-t border-slate-800/80 text-center text-xs text-slate-500">
        Legal Metrology (Packaged Commodities) Rules, 2011 • Official Enforcement Screening Prototype
      </footer>
    </div>
  );
}
