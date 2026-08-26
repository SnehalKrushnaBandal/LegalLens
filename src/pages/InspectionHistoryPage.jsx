import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  ClipboardList, 
  Search, 
  Filter, 
  Download, 
  Eye, 
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  HelpCircle,
  Calendar,
  FileSpreadsheet
} from 'lucide-react';
import { api } from '../services/api';

export default function InspectionHistoryPage() {
  const [inspections, setInspections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [categoryFilter, setCategoryFilter] = useState('ALL');

  const fetchInspections = async () => {
    try {
      setLoading(true);
      const data = await api.getInspections({
        status: statusFilter,
        category: categoryFilter,
        search: search
      });
      setInspections(data);
    } catch (err) {
      console.error('Failed to load inspection history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInspections();
  }, [statusFilter, categoryFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchInspections();
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-600">
            <ClipboardList className="w-4 h-4" />
            <span>Statutory Audit Logs</span>
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            Inspection History & Records
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Complete historical registry of scanned packaged commodities and enforcement outcomes.
          </p>
        </div>

        <Link
          to="/scan"
          className="px-4 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-md shadow-blue-600/30 transition-all"
        >
          + New Inspection
        </Link>
      </div>

      {/* Search & Filter Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row gap-3 items-center justify-between">
        <form onSubmit={handleSearchSubmit} className="relative flex-1 w-full">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by Product Name, Manufacturer, or Inspection ID..."
            className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 focus:bg-white focus:border-blue-500"
          />
        </form>

        <div className="flex items-center gap-2 w-full md:w-auto">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700 font-medium focus:bg-white"
          >
            <option value="ALL">All Compliance Statuses</option>
            <option value="COMPLIANT">Compliant Only</option>
            <option value="NON-COMPLIANT">Non-Compliant Only</option>
            <option value="NEEDS_MANUAL_VERIFICATION">Manual Verification</option>
          </select>

          <button
            onClick={fetchInspections}
            className="p-2 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-600"
            title="Refresh"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-slate-500 text-xs font-medium">
            Loading inspections...
          </div>
        ) : inspections.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-xs">
            No inspection records match your filters.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider text-[10px] border-b border-slate-200">
                <tr>
                  <th className="px-4 py-3">Inspection ID</th>
                  <th className="px-4 py-3">Date</th>
                  <th className="px-4 py-3">Product Name</th>
                  <th className="px-4 py-3">Category</th>
                  <th className="px-4 py-3">Manufacturer</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3">Score</th>
                  <th className="px-4 py-3">Violations</th>
                  <th className="px-4 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {inspections.map((insp) => {
                  const isOk = insp.compliance_status === 'COMPLIANT';
                  const isWarn = insp.compliance_status === 'NEEDS_MANUAL_VERIFICATION';
                  const statusBadge = isOk
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    : isWarn
                    ? 'bg-amber-50 text-amber-700 border-amber-200'
                    : 'bg-red-50 text-red-700 border-red-200';

                  return (
                    <tr key={insp.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="px-4 py-3.5 font-mono font-bold text-blue-600">
                        {insp.inspection_number}
                      </td>
                      <td className="px-4 py-3.5 text-slate-500 whitespace-nowrap">
                        {new Date(insp.inspection_date).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-3.5 font-semibold text-slate-900">
                        {insp.product_name}
                      </td>
                      <td className="px-4 py-3.5 text-slate-600">
                        {insp.category}
                      </td>
                      <td className="px-4 py-3.5 text-slate-600">
                        {insp.manufacturer || 'Declared on package'}
                      </td>
                      <td className="px-4 py-3.5 whitespace-nowrap">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${statusBadge}`}>
                          {insp.compliance_status.replace('_', ' ')}
                        </span>
                      </td>
                      <td className="px-4 py-3.5 font-mono font-bold text-slate-800">
                        {Math.round(insp.compliance_score)}/100
                      </td>
                      <td className="px-4 py-3.5">
                        <span className={`font-mono text-xs font-semibold ${insp.violations_count > 0 ? 'text-red-600' : 'text-emerald-600'}`}>
                          {insp.violations_count}
                        </span>
                      </td>
                      <td className="px-4 py-3.5 text-right space-x-2 whitespace-nowrap">
                        <Link
                          to={`/inspections/${insp.id}`}
                          className="px-2.5 py-1 rounded bg-blue-50 text-blue-700 hover:bg-blue-100 font-semibold text-[11px]"
                        >
                          View
                        </Link>
                        <button
                          type="button"
                          onClick={() => window.open(api.getReportDownloadUrl(insp.id), '_blank')}
                          className="px-2.5 py-1 rounded bg-slate-100 text-slate-700 hover:bg-slate-200 font-semibold text-[11px]"
                        >
                          Report (PDF)
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
