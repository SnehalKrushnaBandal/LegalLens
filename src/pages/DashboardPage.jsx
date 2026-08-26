import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  ClipboardCheck, 
  AlertTriangle, 
  CheckCircle2, 
  HelpCircle, 
  ScanLine, 
  TrendingUp, 
  Layers, 
  ArrowUpRight,
  RefreshCw,
  Scale,
  FileText,
  AlertCircle
} from 'lucide-react';
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip as RechartsTooltip, 
  AreaChart, 
  Area 
} from 'recharts';
import { api } from '../services/api';

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchDashboardData = async () => {
    try {
      setRefreshing(true);
      const data = await api.getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load dashboard statistics:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="flex items-center gap-3 text-slate-500 font-medium">
          <RefreshCw className="w-5 h-5 animate-spin text-blue-600" />
          Loading Legal Metrology Analytics...
        </div>
      </div>
    );
  }

  const kpis = [
    {
      title: 'Total Inspections',
      value: stats?.total_inspections || 0,
      icon: ClipboardCheck,
      color: 'text-blue-600',
      bg: 'bg-blue-50 border-blue-200',
      sub: 'All packaged commodities'
    },
    {
      title: 'Compliant Products',
      value: stats?.compliant_products || 0,
      icon: CheckCircle2,
      color: 'text-emerald-600',
      bg: 'bg-emerald-50 border-emerald-200',
      sub: `${stats?.compliance_rate || 0}% compliance rate`
    },
    {
      title: 'Non-Compliant Products',
      value: stats?.non_compliant_products || 0,
      icon: AlertTriangle,
      color: 'text-red-600',
      bg: 'bg-red-50 border-red-200',
      sub: 'Violations flagged'
    },
    {
      title: 'Manual Verification',
      value: stats?.manual_verification_required || 0,
      icon: HelpCircle,
      color: 'text-amber-600',
      bg: 'bg-amber-50 border-amber-200',
      sub: 'Readability / blurred date'
    },
    {
      title: 'Total Violations',
      value: stats?.violations_detected || 0,
      icon: Layers,
      color: 'text-purple-600',
      bg: 'bg-purple-50 border-purple-200',
      sub: 'Rule non-conformities'
    }
  ];

  return (
    <div className="space-y-6 pb-12">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-600">
            <Scale className="w-4 h-4" />
            <span>Legal Metrology Inspection Analytics</span>
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            Enforcement Overview & Compliance Dashboard
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Automated monitoring under the Legal Metrology (Packaged Commodities) Rules, 2011
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchDashboardData}
            disabled={refreshing}
            className="p-2.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-600 transition-colors"
            title="Refresh statistics"
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
          </button>

          <Link
            to="/scan"
            className="px-4 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold flex items-center gap-2 shadow-md shadow-blue-600/30 transition-all"
          >
            <ScanLine className="w-4 h-4" />
            Scan New Product
          </Link>
        </div>
      </div>

      {/* Demo dataset disclaimer banner */}
      <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-900 text-xs flex items-center justify-between">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>
            <b>Demo Dataset Notice:</b> Displaying realistic synthetic inspection scans for SIH 2026 prototype evaluation. Not official government enforcement records.
          </span>
        </div>
        <span className="font-mono text-[10px] font-bold bg-amber-200/60 text-amber-900 px-2 py-0.5 rounded">
          DEMO DATA
        </span>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {kpis.map((kpi, idx) => {
          const Icon = kpi.icon;
          return (
            <div key={idx} className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  {kpi.title}
                </span>
                <span className={`p-2 rounded-lg border ${kpi.bg}`}>
                  <Icon className={`w-4 h-4 ${kpi.color}`} />
                </span>
              </div>
              <div>
                <div className="text-2xl font-black text-slate-900 tracking-tight">
                  {kpi.value}
                </div>
                <div className="text-[11px] text-slate-400 font-medium mt-0.5">
                  {kpi.sub}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Compliance Distribution Pie Chart */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Compliance Status Distribution
            </h3>
            <p className="text-[11px] text-slate-400">Scanned packages compliance proportion</p>
          </div>

          <div className="h-48 my-2">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats?.compliance_distribution || []}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={45}
                  outerRadius={70}
                  paddingAngle={4}
                >
                  {(stats?.compliance_distribution || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <RechartsTooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-3 gap-2 pt-3 border-t border-slate-100 text-center text-xs">
            <div>
              <div className="font-bold text-emerald-600">{stats?.compliant_products || 0}</div>
              <div className="text-[10px] text-slate-400">Compliant</div>
            </div>
            <div>
              <div className="font-bold text-red-600">{stats?.non_compliant_products || 0}</div>
              <div className="text-[10px] text-slate-400">Non-Compliant</div>
            </div>
            <div>
              <div className="font-bold text-amber-600">{stats?.manual_verification_required || 0}</div>
              <div className="text-[10px] text-slate-400">Manual Check</div>
            </div>
          </div>
        </div>

        {/* Violations by Category Bar Chart */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Violations by Category
            </h3>
            <p className="text-[11px] text-slate-400">Non-compliance by Legal Metrology rule area</p>
          </div>

          <div className="h-48 my-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats?.violations_by_category || []} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <XAxis dataKey="category" tick={{ fontSize: 9 }} interval={0} />
                <YAxis tick={{ fontSize: 9 }} allowDecimals={false} />
                <RechartsTooltip />
                <Bar dataKey="count" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="text-[11px] text-slate-400 text-center pt-2 border-t border-slate-100">
            Most frequent: <span className="font-semibold text-slate-700">Consumer Care & MRP Declarations</span>
          </div>
        </div>

        {/* Inspections Trend Area Chart */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Inspection Activity Trend
            </h3>
            <p className="text-[11px] text-slate-400">Daily screening volume over past 7 days</p>
          </div>

          <div className="h-48 my-2">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.inspections_trend || []} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorInsp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" tick={{ fontSize: 9 }} />
                <YAxis tick={{ fontSize: 9 }} allowDecimals={false} />
                <RechartsTooltip />
                <Area type="monotone" dataKey="inspections" stroke="#2563EB" fillOpacity={1} fill="url(#colorInsp)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="text-[11px] text-slate-400 text-center pt-2 border-t border-slate-100">
            Average daily screening: <span className="font-semibold text-slate-700">6.4 packages / day</span>
          </div>
        </div>
      </div>

      {/* Top Violations & Recent Inspections Table */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Most Common Violations List */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Top Detected Violations
            </h3>
            <p className="text-[11px] text-slate-400">Repeated non-conformities across market samples</p>
          </div>

          <div className="space-y-3">
            {(stats?.most_common_violations || []).map((cv, idx) => (
              <div key={idx} className="p-3 rounded-lg bg-slate-50 border border-slate-200/80 space-y-1">
                <div className="flex justify-between items-start text-xs">
                  <span className="font-semibold text-slate-800 line-clamp-1">{cv.issue}</span>
                  <span className="font-mono text-xs font-bold text-red-600 bg-red-50 px-1.5 py-0.5 rounded border border-red-100 shrink-0">
                    {cv.occurrences} cases
                  </span>
                </div>
                <div className="flex items-center justify-between text-[10px] text-slate-500">
                  <span>Category: {cv.category}</span>
                  <span className="font-medium text-amber-700">{cv.severity} Severity</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Inspections Table */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col justify-between">
          <div className="p-4 border-b border-slate-200 flex justify-between items-center bg-slate-50/50">
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800">
                Recent Market Inspections
              </h3>
              <p className="text-[11px] text-slate-500">Latest packaged products scanned and evaluated</p>
            </div>
            <Link
              to="/inspections"
              className="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-1"
            >
              View All History <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100/75 text-slate-600 font-semibold uppercase tracking-wider text-[10px] border-b border-slate-200">
                <tr>
                  <th className="px-4 py-2.5">Inspection ID</th>
                  <th className="px-4 py-2.5">Product & Manufacturer</th>
                  <th className="px-4 py-2.5">Status</th>
                  <th className="px-4 py-2.5">Score</th>
                  <th className="px-4 py-2.5">Violations</th>
                  <th className="px-4 py-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {(stats?.recent_inspections || []).map((insp) => {
                  const isOk = insp.compliance_status === 'COMPLIANT';
                  const isWarn = insp.compliance_status === 'NEEDS_MANUAL_VERIFICATION';
                  const statusBadge = isOk
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    : isWarn
                    ? 'bg-amber-50 text-amber-700 border-amber-200'
                    : 'bg-red-50 text-red-700 border-red-200';

                  return (
                    <tr key={insp.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="px-4 py-3 font-mono font-medium text-slate-800">
                        {insp.inspection_number}
                      </td>
                      <td className="px-4 py-3">
                        <div className="font-semibold text-slate-900">{insp.product_name}</div>
                        <div className="text-[10px] text-slate-500">{insp.manufacturer || 'Declared on package'}</div>
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${statusBadge}`}>
                          {insp.compliance_status.replace('_', ' ')}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-mono font-bold text-slate-800">
                        {Math.round(insp.compliance_score)}/100
                      </td>
                      <td className="px-4 py-3">
                        <span className={`font-mono text-xs font-semibold ${insp.violations_count > 0 ? 'text-red-600' : 'text-emerald-600'}`}>
                          {insp.violations_count} detected
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right space-x-2">
                        <Link
                          to={`/inspections/${insp.id}`}
                          className="px-2.5 py-1 rounded bg-blue-50 text-blue-700 hover:bg-blue-100 font-semibold text-[11px] transition-colors"
                        >
                          Details
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
