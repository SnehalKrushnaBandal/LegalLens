import React, { useState } from 'react';
import { 
  Globe2, 
  AlertTriangle, 
  CheckCircle2, 
  Scale, 
  ArrowRight, 
  Sparkles, 
  ShieldAlert,
  HelpCircle,
  FileText
} from 'lucide-react';
import { api } from '../services/api';

const ECOMM_DEMO_PRESETS = [
  {
    title: 'MRP Overcharging Violation (Amazon)',
    platform: 'Amazon India',
    listing_title: 'Basmati Rice Premium Extra Long Grain 5kg',
    listing_mrp: 720.0,
    listing_selling_price: 680.0,
    listing_net_quantity: '5 kg',
    listing_manufacturer: 'ABC Foods Pvt Ltd',
    listing_country_of_origin: 'India',
    package_mrp: 650.0,
    package_net_quantity: '5 kg',
    package_manufacturer: 'ABC Foods Pvt Ltd'
  },
  {
    title: 'Quantity Mismatch & Missing Origin (Flipkart)',
    platform: 'Flipkart',
    listing_title: 'Butter Delight Cookies & Biscuits Snack Pack',
    listing_mrp: 35.0,
    listing_selling_price: 30.0,
    listing_net_quantity: '250 g', // Package is actually 200g!
    listing_manufacturer: 'Sunlight Bakeries Ltd',
    listing_country_of_origin: '', // Missing origin on listing
    package_mrp: 35.0,
    package_net_quantity: '200 g',
    package_manufacturer: 'Sunlight Bakeries Ltd'
  },
  {
    title: 'Fully Compliant Listing (Blinkit)',
    platform: 'Blinkit',
    listing_title: 'Royal Garam Masala Powder 100g Pouch',
    listing_mrp: 75.0,
    listing_selling_price: 70.0,
    listing_net_quantity: '100 g',
    listing_manufacturer: 'Heritage Spices Co.',
    listing_country_of_origin: 'India',
    package_mrp: 75.0,
    package_net_quantity: '100 g',
    package_manufacturer: 'Heritage Spices Co.'
  }
];

export default function OnlineListingPage() {
  const [formData, setFormData] = useState({
    platform_name: 'Amazon India',
    listing_title: 'Premium Basmati Rice 5kg',
    listing_mrp: 720,
    listing_selling_price: 680,
    listing_net_quantity: '5 kg',
    listing_manufacturer: 'ABC Foods Pvt Ltd',
    listing_country_of_origin: 'India',
    package_mrp: 650,
    package_net_quantity: '5 kg',
    package_manufacturer: 'ABC Foods Pvt Ltd'
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handlePresetSelect = (preset) => {
    setFormData({
      platform_name: preset.platform,
      listing_title: preset.listing_title,
      listing_mrp: preset.listing_mrp,
      listing_selling_price: preset.listing_selling_price,
      listing_net_quantity: preset.listing_net_quantity,
      listing_manufacturer: preset.listing_manufacturer,
      listing_country_of_origin: preset.listing_country_of_origin,
      package_mrp: preset.package_mrp,
      package_net_quantity: preset.package_net_quantity,
      package_manufacturer: preset.package_manufacturer
    });
    setResult(null);
  };

  const handleVerify = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await api.verifyEcommerce({
        platform_name: formData.platform_name,
        listing_title: formData.listing_title,
        listing_mrp: parseFloat(formData.listing_mrp),
        listing_selling_price: formData.listing_selling_price ? parseFloat(formData.listing_selling_price) : null,
        listing_net_quantity: formData.listing_net_quantity,
        listing_manufacturer: formData.listing_manufacturer,
        listing_country_of_origin: formData.listing_country_of_origin,
        package_mrp: parseFloat(formData.package_mrp),
        package_net_quantity: formData.package_net_quantity,
        package_manufacturer: formData.package_manufacturer
      });
      setResult(res);
    } catch (err) {
      alert('Verification failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-600">
          <Globe2 className="w-4 h-4" />
          <span>E-Commerce & Digital Marketplace Inspector</span>
        </div>
        <h2 className="text-2xl font-black text-slate-900 tracking-tight mt-1">
          Online Product Listing vs Physical Package Verification
        </h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Auditing compliance under Legal Metrology (Packaged Commodities) Amendment Rules & Rule 6(11).
        </p>
      </div>

      {/* Demo Presets Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-2">
        <div className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
          <Sparkles className="w-4 h-4 text-amber-500" />
          <span>Select Pre-configured E-Commerce Test Case:</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
          {ECOMM_DEMO_PRESETS.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handlePresetSelect(preset)}
              className="p-2.5 text-left rounded-lg bg-slate-50 hover:bg-blue-50 border border-slate-200 hover:border-blue-300 text-xs transition-all"
            >
              <div className="font-bold text-slate-800">{preset.title}</div>
              <div className="text-[11px] text-slate-500 mt-0.5">{preset.platform} • Package MRP: ₹{preset.package_mrp} vs Listing: ₹{preset.listing_mrp}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Comparison Form */}
      <form onSubmit={handleVerify} className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Online Listing Details */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <div className="pb-2 border-b border-slate-100 flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800 flex items-center gap-2">
              <Globe2 className="w-4 h-4 text-blue-600" />
              Digital Marketplace Product Listing
            </h3>
            <span className="text-[10px] font-mono px-2 py-0.5 bg-blue-50 text-blue-700 rounded">
              E-Commerce Data
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Marketplace Platform</label>
              <input
                type="text"
                value={formData.platform_name}
                onChange={(e) => setFormData({ ...formData, platform_name: e.target.value })}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Product Title / Heading on Page</label>
              <input
                type="text"
                value={formData.listing_title}
                onChange={(e) => setFormData({ ...formData, listing_title: e.target.value })}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Declared Listing MRP (₹)</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.listing_mrp}
                  onChange={(e) => setFormData({ ...formData, listing_mrp: e.target.value })}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-mono font-bold"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Listing Net Quantity</label>
                <input
                  type="text"
                  value={formData.listing_net_quantity}
                  onChange={(e) => setFormData({ ...formData, listing_net_quantity: e.target.value })}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-mono"
                />
              </div>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Declared Country of Origin on Platform</label>
              <input
                type="text"
                value={formData.listing_country_of_origin}
                onChange={(e) => setFormData({ ...formData, listing_country_of_origin: e.target.value })}
                placeholder="Leave blank to simulate missing declaration"
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900"
              />
            </div>
          </div>
        </div>

        {/* Right: Physical Package Values */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <div className="pb-2 border-b border-slate-100 flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800 flex items-center gap-2">
              <Scale className="w-4 h-4 text-emerald-600" />
              Actual Physical Packaging Ground Truth
            </h3>
            <span className="text-[10px] font-mono px-2 py-0.5 bg-emerald-50 text-emerald-700 rounded">
              Physical Sample
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Physical Package Stamped MRP (₹)</label>
              <input
                type="number"
                step="0.01"
                value={formData.package_mrp}
                onChange={(e) => setFormData({ ...formData, package_mrp: e.target.value })}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-mono font-bold"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Physical Stamped Net Quantity</label>
              <input
                type="text"
                value={formData.package_net_quantity}
                onChange={(e) => setFormData({ ...formData, package_net_quantity: e.target.value })}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-mono"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Physical Manufacturer Name</label>
              <input
                type="text"
                value={formData.package_manufacturer}
                onChange={(e) => setFormData({ ...formData, package_manufacturer: e.target.value })}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900"
              />
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-lg shadow-md shadow-blue-600/30 flex items-center justify-center gap-2 transition-all"
              >
                <Scale className="w-4 h-4" />
                {loading ? 'Evaluating Discrepancies...' : 'Execute Digital Marketplace Compliance Audit'}
              </button>
            </div>
          </div>
        </div>
      </form>

      {/* Verification Results Panel */}
      {result && (
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-slate-100">
            <div>
              <div className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Audit Result & Risk Assessment
              </div>
              <div className="text-xl font-black text-slate-900 mt-1 flex items-center gap-2">
                {result.status === 'PASS' ? (
                  <span className="text-emerald-600 flex items-center gap-1.5">
                    <CheckCircle2 className="w-6 h-6" /> COMPLIANT E-COMMERCE LISTING
                  </span>
                ) : result.status === 'HIGH_RISK' ? (
                  <span className="text-red-600 flex items-center gap-1.5">
                    <ShieldAlert className="w-6 h-6" /> HIGH RISK / STATUTORY OVERCHARGING VIOLATION
                  </span>
                ) : (
                  <span className="text-amber-600 flex items-center gap-1.5">
                    <AlertTriangle className="w-6 h-6" /> DISCREPANCIES DETECTED
                  </span>
                )}
              </div>
            </div>

            <div className="text-right">
              <span className="text-2xl font-black font-mono text-slate-900">{result.compliance_score}/100</span>
              <div className="text-[10px] text-slate-400 font-semibold uppercase">E-Commerce Compliance Score</div>
            </div>
          </div>

          {/* Legal Recommendation */}
          <div className={`p-4 rounded-xl border text-xs font-medium ${
            result.status === 'HIGH_RISK' ? 'bg-red-50 border-red-200 text-red-900' : 'bg-blue-50 border-blue-200 text-blue-900'
          }`}>
            <span className="font-bold block mb-1">Official Legal Metrology Action Directive:</span>
            {result.recommendation}
          </div>

          {/* Discrepancies Table */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Itemized Listing Discrepancies ({result.discrepancies?.length || 0})
            </h4>

            {result.discrepancies?.length === 0 ? (
              <div className="p-4 bg-emerald-50 text-emerald-800 rounded-lg text-xs font-medium">
                No discrepancies found between digital listing and physical packaging.
              </div>
            ) : (
              <div className="space-y-3">
                {result.discrepancies.map((item, idx) => (
                  <div key={idx} className="p-4 rounded-xl border border-red-200 bg-red-50/40 space-y-2">
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-bold text-slate-900">{item.field}</span>
                      <span className="px-2 py-0.5 rounded font-mono font-bold text-[10px] bg-red-600 text-white">
                        {item.severity}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-3 text-xs bg-white p-3 rounded-lg border border-red-100">
                      <div>
                        <span className="text-[10px] uppercase font-bold text-slate-500 block">Package Ground Truth:</span>
                        <span className="font-semibold text-slate-800">{item.package_value}</span>
                      </div>
                      <div>
                        <span className="text-[10px] uppercase font-bold text-red-600 block">Online Listing:</span>
                        <span className="font-semibold text-red-700">{item.listing_value}</span>
                      </div>
                    </div>
                    <p className="text-xs text-slate-700">{item.description}</p>
                    <div className="text-[10px] text-slate-500 font-mono">Reference: {item.legal_rule}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
