import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Package, Search, Filter, RefreshCw, ArrowRight, CheckCircle2, AlertTriangle } from 'lucide-react';
import { api } from '../services/api';

export default function ProductRepositoryPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('ALL');

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const data = await api.getProducts({
        category: categoryFilter !== 'ALL' ? categoryFilter : undefined,
        search: search
      });
      setProducts(data);
    } catch (err) {
      console.error('Failed to load products:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, [categoryFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchProducts();
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-600">
            <Package className="w-4 h-4" />
            <span>Commodity Database</span>
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
            Product Repository & Compliance Catalog
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Central repository of all packaged goods, brand manufacturers, and historical inspection tracking.
          </p>
        </div>

        <Link
          to="/scan"
          className="px-4 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-md shadow-blue-600/30 transition-all"
        >
          + Scan New Commodity
        </Link>
      </div>

      {/* Search & Filter */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row gap-3 items-center justify-between">
        <form onSubmit={handleSearchSubmit} className="relative flex-1 w-full">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search products by name or manufacturer..."
            className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 focus:bg-white focus:border-blue-500"
          />
        </form>

        <button
          onClick={fetchProducts}
          className="p-2 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-600"
          title="Refresh"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* Products Grid / Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-slate-500 text-xs font-medium">
            Loading product repository...
          </div>
        ) : products.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-xs">
            No products found.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider text-[10px] border-b border-slate-200">
                <tr>
                  <th className="px-4 py-3">Product Code</th>
                  <th className="px-4 py-3">Product Name</th>
                  <th className="px-4 py-3">Category</th>
                  <th className="px-4 py-3">Manufacturer</th>
                  <th className="px-4 py-3">Net Quantity</th>
                  <th className="px-4 py-3">MRP (₹)</th>
                  <th className="px-4 py-3">Inspections</th>
                  <th className="px-4 py-3">Latest Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {products.map((p) => {
                  const isOk = p.latest_status === 'COMPLIANT';
                  const isWarn = p.latest_status === 'NEEDS_MANUAL_VERIFICATION';
                  const statusBadge = isOk
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    : isWarn
                    ? 'bg-amber-50 text-amber-700 border-amber-200'
                    : 'bg-red-50 text-red-700 border-red-200';

                  return (
                    <tr key={p.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="px-4 py-3.5 font-mono font-bold text-blue-600">
                        {p.product_code}
                      </td>
                      <td className="px-4 py-3.5 font-semibold text-slate-900">
                        {p.name}
                      </td>
                      <td className="px-4 py-3.5 text-slate-600">
                        {p.category}
                      </td>
                      <td className="px-4 py-3.5 text-slate-600">
                        {p.manufacturer_name || 'Declared on package'}
                      </td>
                      <td className="px-4 py-3.5 font-mono text-slate-700">
                        {p.net_quantity || 'N/A'}
                      </td>
                      <td className="px-4 py-3.5 font-mono font-bold text-slate-800">
                        {p.standard_mrp ? `₹${p.standard_mrp}` : 'Declared on pack'}
                      </td>
                      <td className="px-4 py-3.5 font-mono font-semibold text-slate-700">
                        {p.inspection_count} audits
                      </td>
                      <td className="px-4 py-3.5">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${statusBadge}`}>
                          {p.latest_status.replace('_', ' ')}
                        </span>
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
