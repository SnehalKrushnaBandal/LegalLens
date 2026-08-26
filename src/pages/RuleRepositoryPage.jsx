import React, { useEffect, useState } from 'react';
import { 
  BookOpenCheck, 
  Scale, 
  CheckCircle2, 
  ToggleLeft, 
  ToggleRight, 
  Edit3, 
  Save, 
  X, 
  Plus, 
  AlertCircle,
  RefreshCw
} from 'lucide-react';
import { api } from '../services/api';

export default function RuleRepositoryPage() {
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingRuleId, setEditingRuleId] = useState(null);
  const [editFormData, setEditFormData] = useState({});

  const fetchRules = async () => {
    try {
      setLoading(true);
      const data = await api.getRules();
      setRules(data);
    } catch (err) {
      console.error('Failed to load rules:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRules();
  }, []);

  const handleToggleActive = async (ruleId) => {
    try {
      const updated = await api.toggleRule(ruleId);
      setRules(prev => prev.map(r => r.id === ruleId ? updated : r));
    } catch (err) {
      alert('Failed to toggle rule status: ' + err.message);
    }
  };

  const handleStartEdit = (rule) => {
    setEditingRuleId(rule.id);
    setEditFormData({
      requirement_text: rule.requirement_text,
      severity: rule.severity,
      validation_type: rule.validation_type
    });
  };

  const handleSaveEdit = async (ruleId) => {
    try {
      const updated = await api.updateRule(ruleId, editFormData);
      setRules(prev => prev.map(r => r.id === ruleId ? updated : r));
      setEditingRuleId(null);
    } catch (err) {
      alert('Failed to update rule: ' + err.message);
    }
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-600">
            <Scale className="w-4 h-4" />
            <span>Configurable Legal Engine</span>
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            Legal Metrology Rule Repository
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Statutory requirements under Legal Metrology (Packaged Commodities) Rules, 2011 & Gazette Amendments.
          </p>
        </div>

        <button
          onClick={fetchRules}
          className="p-2.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-600"
          title="Refresh rules"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* Info notice about configurable rules */}
      <div className="p-4 rounded-xl bg-blue-50 border border-blue-200 text-xs text-blue-900 flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <span className="font-bold">Dynamic Rule Customization Architecture:</span>
          <p className="leading-relaxed text-blue-800">
            Legal rules and validation thresholds are stored dynamically in the database. Officers can toggle rules, update penalty severity, or customize requirements as new Legal Metrology gazette notifications or amendments are published.
          </p>
        </div>
      </div>

      {/* Rules Grid */}
      <div className="grid grid-cols-1 gap-4">
        {loading ? (
          <div className="p-8 text-center text-slate-500 text-xs">
            Loading rules repository...
          </div>
        ) : rules.map((rule) => {
          const isEditing = editingRuleId === rule.id;

          return (
            <div
              key={rule.id}
              className={`bg-white rounded-xl p-5 border transition-all shadow-sm ${
                rule.is_active ? 'border-slate-200' : 'border-slate-200 bg-slate-50/60 opacity-60'
              }`}
            >
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 pb-3 border-b border-slate-100">
                <div className="flex items-center gap-3">
                  <span className="font-mono font-bold text-xs px-2.5 py-1 rounded bg-blue-600 text-white shadow-sm">
                    {rule.rule_code}
                  </span>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">{rule.category}</h3>
                    <div className="text-[11px] text-slate-500 font-mono">{rule.legal_reference}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                    rule.severity === 'CRITICAL' ? 'bg-red-50 text-red-700 border-red-200' :
                    rule.severity === 'HIGH' ? 'bg-amber-50 text-amber-700 border-amber-200' :
                    'bg-blue-50 text-blue-700 border-blue-200'
                  }`}>
                    {rule.severity} SEVERITY
                  </span>

                  <span className="text-[10px] font-mono px-2 py-0.5 bg-slate-100 text-slate-700 rounded border border-slate-200">
                    {rule.validation_type}
                  </span>

                  <button
                    type="button"
                    onClick={() => handleToggleActive(rule.id)}
                    className="text-xs font-semibold flex items-center gap-1.5 transition-colors"
                  >
                    {rule.is_active ? (
                      <span className="text-emerald-600 flex items-center gap-1">
                        <ToggleRight className="w-6 h-6 text-emerald-600" /> Active
                      </span>
                    ) : (
                      <span className="text-slate-400 flex items-center gap-1">
                        <ToggleLeft className="w-6 h-6 text-slate-400" /> Inactive
                      </span>
                    )}
                  </button>
                </div>
              </div>

              {/* Requirement Text / Editor */}
              <div className="mt-3 text-xs">
                {isEditing ? (
                  <div className="space-y-3 p-3 bg-blue-50/50 rounded-lg border border-blue-200">
                    <div>
                      <label className="block font-bold text-slate-700 mb-1">Requirement Specification</label>
                      <textarea
                        rows={2}
                        value={editFormData.requirement_text}
                        onChange={(e) => setEditFormData({ ...editFormData, requirement_text: e.target.value })}
                        className="w-full p-2 bg-white border border-slate-300 rounded text-xs"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block font-bold text-slate-700 mb-1">Severity</label>
                        <select
                          value={editFormData.severity}
                          onChange={(e) => setEditFormData({ ...editFormData, severity: e.target.value })}
                          className="w-full p-1.5 bg-white border border-slate-300 rounded text-xs"
                        >
                          <option value="CRITICAL">CRITICAL</option>
                          <option value="HIGH">HIGH</option>
                          <option value="MEDIUM">MEDIUM</option>
                          <option value="LOW">LOW</option>
                        </select>
                      </div>
                      <div>
                        <label className="block font-bold text-slate-700 mb-1">Validation Method</label>
                        <select
                          value={editFormData.validation_type}
                          onChange={(e) => setEditFormData({ ...editFormData, validation_type: e.target.value })}
                          className="w-full p-1.5 bg-white border border-slate-300 rounded text-xs"
                        >
                          <option value="TEXT_PRESENCE">TEXT_PRESENCE</option>
                          <option value="PATTERN">PATTERN</option>
                          <option value="NUMERICAL">NUMERICAL</option>
                          <option value="READABILITY">READABILITY</option>
                        </select>
                      </div>
                    </div>
                    <div className="flex justify-end gap-2 pt-2">
                      <button
                        type="button"
                        onClick={() => setEditingRuleId(null)}
                        className="px-3 py-1 bg-slate-200 hover:bg-slate-300 rounded text-xs font-semibold"
                      >
                        Cancel
                      </button>
                      <button
                        type="button"
                        onClick={() => handleSaveEdit(rule.id)}
                        className="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-semibold flex items-center gap-1"
                      >
                        <Save className="w-3.5 h-3.5" /> Save Rule
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex justify-between items-start gap-4">
                    <div>
                      <p className="text-slate-600">{rule.description}</p>
                      <div className="mt-2 p-2.5 rounded bg-slate-50 border border-slate-200 text-slate-800 font-medium">
                        <span className="text-[10px] uppercase font-bold text-slate-500 block mb-0.5">Statutory Requirement:</span>
                        {rule.requirement_text}
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleStartEdit(rule)}
                      className="p-1.5 rounded-lg border border-slate-200 hover:bg-slate-100 text-slate-600 shrink-0"
                      title="Edit Rule"
                    >
                      <Edit3 className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
