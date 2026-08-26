import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  ArrowLeft, 
  Download, 
  CheckCircle2, 
  AlertTriangle, 
  FileText, 
  User, 
  Clock, 
  Scale, 
  ShieldCheck,
  RotateCcw,
  Sparkles
} from 'lucide-react';
import { api } from '../services/api';
import BoundingBoxViewer from '../components/BoundingBoxViewer';
import ComplianceScoreGauge from '../components/ComplianceScoreGauge';
import ViolationCard from '../components/ViolationCard';
import ReadabilityBadge from '../components/ReadabilityBadge';

export default function InspectionDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [inspection, setInspection] = useState(null);
  const [loading, setLoading] = useState(true);
  const [signing, setSigning] = useState(false);
  const [remarks, setRemarks] = useState('');
  const [highlightedField, setHighlightedField] = useState(null);

  const fetchInspection = async () => {
    try {
      setLoading(true);
      const data = await api.getInspectionById(id);
      setInspection(data);
      setRemarks(data.remarks || '');
    } catch (err) {
      console.error('Failed to load inspection details:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInspection();
  }, [id]);

  const handleSignVerification = async () => {
    try {
      setSigning(true);
      const updated = await api.verifyInspection(id, {
        remarks,
        final_status: inspection.compliance_status
      });
      setInspection(updated);
      alert('Inspection verified and digitally stamped by officer.');
    } catch (err) {
      alert('Failed to sign verification: ' + err.message);
    } finally {
      setSigning(false);
    }
  };

  const handleDownloadPdf = () => {
    window.open(api.getReportDownloadUrl(id), '_blank');
  };

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-500 font-medium min-h-[50vh] flex items-center justify-center">
        Loading Inspection Record #{id}...
      </div>
    );
  }

  if (!inspection) {
    return (
      <div className="p-8 text-center space-y-3">
        <p className="text-red-600 font-bold">Inspection record not found.</p>
        <Link to="/inspections" className="text-blue-600 underline text-xs">Return to Inspection History</Link>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-16">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/inspections')}
            className="p-2 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-600 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                {inspection.inspection_number}
              </span>
              <span className="text-xs text-slate-500">•</span>
              <span className="text-xs text-slate-500 font-medium">
                {new Date(inspection.inspection_date).toLocaleDateString()}
              </span>
            </div>
            <h2 className="text-xl font-black text-slate-900 tracking-tight mt-1">
              {inspection.product_name}
            </h2>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleDownloadPdf}
            className="px-4 py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-2 shadow-md shadow-emerald-600/30 transition-all"
          >
            <Download className="w-4 h-4" />
            Download PDF Report
          </button>
        </div>
      </div>

      {/* Compliance Score Gauge */}
      <ComplianceScoreGauge
        score={inspection.compliance_score}
        status={inspection.compliance_status}
        breakdown={inspection.score_breakdown}
      />

      {/* Grid: Image Evidence + Extracted Declarations */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Bounding Box Evidence Viewer */}
        <div className="lg:col-span-5 flex flex-col">
          <BoundingBoxViewer
            originalImage={inspection.image_path}
            evidenceImage={inspection.evidence_image_path}
            declarations={inspection.declarations}
            highlightedField={highlightedField}
            onSelectField={(f) => setHighlightedField(f)}
          />
        </div>

        {/* Right: Declarations Table */}
        <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <FileText className="w-4 h-4 text-blue-600" />
            Mandatory Declarations (Rule 6 Analysis)
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider text-[10px] border-b border-slate-200">
                <tr>
                  <th className="px-3 py-2">Declaration</th>
                  <th className="px-3 py-2">Detected Value</th>
                  <th className="px-3 py-2">Status</th>
                  <th className="px-3 py-2">Confidence</th>
                  <th className="px-3 py-2">Readability</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {inspection.declarations?.map((dec) => {
                  const isHighlighted = highlightedField === dec.field_name;
                  return (
                    <tr
                      key={dec.id || dec.field_name}
                      onMouseEnter={() => setHighlightedField(dec.field_name)}
                      className={`transition-colors ${isHighlighted ? 'bg-blue-50/70' : 'hover:bg-slate-50/60'}`}
                    >
                      <td className="px-3 py-2 font-bold text-slate-800">
                        {dec.field_name.replace('_', ' ').toUpperCase()}
                      </td>
                      <td className="px-3 py-2 font-medium text-slate-700">
                        {dec.detected_value || 'Missing / Not Declared'}
                      </td>
                      <td className="px-3 py-2">
                        {dec.is_present && !String(dec.detected_value || '').toLowerCase().includes('missing') ? (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                            Compliant
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-50 text-red-700 border border-red-200">
                            Violation
                          </span>
                        )}
                      </td>
                      <td className="px-3 py-2 font-mono text-slate-500">
                        {Math.round((dec.confidence || 0.95) * 100)}%
                      </td>
                      <td className="px-3 py-2">
                        <ReadabilityBadge
                          fontSizePx={dec.estimated_font_size_px}
                          status={dec.readability_status}
                        />
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Violations Section */}
      <div className="space-y-4">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
          Detected Violations & Legal References ({inspection.violations?.length || 0})
        </h3>

        {inspection.violations?.length === 0 ? (
          <div className="p-6 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-medium text-center">
            <CheckCircle2 className="w-8 h-8 mx-auto text-emerald-600 mb-2" />
            Zero non-conformities found. Product is fully compliant with Legal Metrology Rules, 2011.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {inspection.violations?.map((viol) => (
              <ViolationCard
                key={viol.id}
                violation={viol}
                onUpdateStatus={(vId, st) => api.updateViolationStatus(inspection.id, vId, st)}
                onInspectZone={() => setHighlightedField(viol.category.toLowerCase())}
              />
            ))}
          </div>
        )}
      </div>

      {/* Officer Verification & Signature Block */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-blue-600" />
            Officer Verification & Legal Stamping
          </h3>
          <span className={`px-2 py-0.5 rounded text-[10px] font-bold font-mono ${
            inspection.officer_verified ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
          }`}>
            {inspection.officer_verified ? 'OFFICIALLY VERIFIED' : 'PENDING OFFICER SIGNATURE'}
          </span>
        </div>

        <textarea
          rows={2}
          value={remarks}
          onChange={(e) => setRemarks(e.target.value)}
          placeholder="Official notes or compounding directions..."
          className="w-full p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 focus:bg-white focus:border-blue-500"
        />

        <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
          <div className="text-xs text-slate-500">
            Inspecting Officer: <span className="font-semibold text-slate-800">{inspection.officer_name || 'Inspector Rajesh Sharma (LMO001)'}</span>
          </div>

          <button
            type="button"
            onClick={handleSignVerification}
            disabled={signing}
            className="px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold flex items-center gap-2 shadow-md shadow-blue-600/30 transition-all"
          >
            <ShieldCheck className="w-4 h-4" />
            {signing ? 'Signing...' : 'Sign & Stamp Inspection Record'}
          </button>
        </div>
      </div>
    </div>
  );
}
