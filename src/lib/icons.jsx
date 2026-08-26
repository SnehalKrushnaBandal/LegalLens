import React from 'react';

function createIcon(svgPath, defaultAttrs = {}) {
  return function Icon({ className = 'w-4 h-4', ...props }) {
    return (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
        {...defaultAttrs}
        {...props}
      >
        {svgPath}
      </svg>
    );
  };
}

export const Shield = createIcon(<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />);
export const Scale = createIcon(<>
  <path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/>
  <path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/>
  <path d="M7 21h10"/>
  <path d="M12 3v18"/>
  <path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>
</>);
export const Lock = createIcon(<>
  <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
</>);
export const User = createIcon(<>
  <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
  <circle cx="12" cy="7" r="4"/>
</>);
export const AlertCircle = createIcon(<>
  <circle cx="12" cy="12" r="10"/>
  <line x1="12" x2="12" y1="8" y2="12"/>
  <line x1="12" x2="12.01" y1="16" y2="16"/>
</>);
export const AlertTriangle = createIcon(<>
  <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
  <line x1="12" x2="12" y1="9" y2="13"/>
  <line x1="12" x2="12.01" y1="17" y2="17"/>
</>);
export const CheckCircle2 = createIcon(<>
  <circle cx="12" cy="12" r="10"/>
  <path d="m9 12 2 2 4-4"/>
</>);
export const ArrowRight = createIcon(<>
  <path d="M5 12h14"/>
  <path d="m12 5 7 7-7 7"/>
</>);
export const ArrowLeft = createIcon(<>
  <path d="m12 19-7-7 7-7"/>
  <path d="M19 12H5"/>
</>);
export const ArrowUpRight = createIcon(<>
  <path d="M7 7h10v10"/>
  <path d="M7 17 17 7"/>
</>);
export const LogOut = createIcon(<>
  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
  <polyline points="16 17 21 12 16 7"/>
  <line x1="21" x2="9" y1="12" y2="12"/>
</>);
export const Bell = createIcon(<>
  <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
  <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>
</>);
export const ShieldCheck = createIcon(<>
  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
  <path d="m9 12 2 2 4-4"/>
</>);
export const ShieldAlert = createIcon(<>
  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
  <line x1="12" x2="12" y1="8" y2="12"/>
  <line x1="12" x2="12.01" y1="16" y2="16"/>
</>);
export const LayoutDashboard = createIcon(<>
  <rect width="7" height="9" x="3" y="3" rx="1"/>
  <rect width="7" height="5" x="14" y="3" rx="1"/>
  <rect width="7" height="9" x="14" y="12" rx="1"/>
  <rect width="7" height="5" x="3" y="16" rx="1"/>
</>);
export const ScanLine = createIcon(<>
  <path d="M3 7V5a2 2 0 0 1 2-2h2"/>
  <path d="M17 3h2a2 2 0 0 1 2 2v2"/>
  <path d="M21 17v2a2 2 0 0 1-2 2h-2"/>
  <path d="M7 21H5a2 2 0 0 1-2-2v-2"/>
  <line x1="7" x2="17" y1="12" y2="12"/>
</>);
export const Globe2 = createIcon(<>
  <circle cx="12" cy="12" r="10"/>
  <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>
  <path d="M2 12h20"/>
</>);
export const ClipboardList = createIcon(<>
  <rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>
  <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
  <path d="M12 11h4"/>
  <path d="M12 16h4"/>
  <path d="M8 11h.01"/>
  <path d="M8 16h.01"/>
</>);
export const ClipboardCheck = createIcon(<>
  <rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>
  <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
  <path d="m9 14 2 2 4-4"/>
</>);
export const Package = createIcon(<>
  <path d="m7.5 4.27 9 5.15"/>
  <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>
  <path d="m3.3 7 8.7 5 8.7-5"/>
  <path d="M12 22V12"/>
</>);
export const BookOpenCheck = createIcon(<>
  <path d="M8 3H2v15h7c1.7 0 3 1.3 3 3V7c0-2.2-1.8-4-4-4Z"/>
  <path d="m16 12 2 2 4-4"/>
  <path d="M22 6V3h-6c-2.2 0-4 1.8-4 4v14c0-1.7 1.3-3 3-3h7v-2.3"/>
</>);
export const FileText = createIcon(<>
  <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>
  <path d="M14 2v4a2 2 0 0 0 2 2h4"/>
  <path d="M10 9H8"/>
  <path d="M16 13H8"/>
  <path d="M16 17H8"/>
</>);
export const Upload = createIcon(<>
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
  <polyline points="17 8 12 3 7 8"/>
  <line x1="12" x2="12" y1="3" y2="15"/>
</>);
export const Download = createIcon(<>
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
  <polyline points="7 10 12 15 17 10"/>
  <line x1="12" x2="12" y1="15" y2="3"/>
</>);
export const RefreshCw = createIcon(<>
  <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
  <path d="M21 3v5h-5"/>
  <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
  <path d="M8 16H3v5"/>
</>);
export const RotateCcw = createIcon(<>
  <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
  <path d="M3 3v5h5"/>
</>);
export const Eye = createIcon(<>
  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
  <circle cx="12" cy="12" r="3"/>
</>);
export const Layers = createIcon(<>
  <path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/>
  <path d="m22 12.5-8.58 3.91a2 2 0 0 1-1.66 0L2 12.5"/>
  <path d="m22 17.5-8.58 3.91a2 2 0 0 1-1.66 0L2 17.5"/>
</>);
export const TrendingUp = createIcon(<>
  <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>
  <polyline points="16 7 22 7 22 13"/>
</>);
export const HelpCircle = createIcon(<>
  <circle cx="12" cy="12" r="10"/>
  <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
  <line x1="12" x2="12.01" y1="17" y2="17"/>
</>);
export const Sparkles = createIcon(<>
  <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
</>);
export const Cpu = createIcon(<>
  <rect width="16" height="16" x="4" y="4" rx="2"/>
  <rect width="6" height="6" x="9" y="9" rx="1"/>
  <path d="M15 2v2"/>
  <path d="M15 20v2"/>
  <path d="M2 15h2"/>
  <path d="M2 9h2"/>
  <path d="M20 15h2"/>
  <path d="M20 9h2"/>
  <path d="M9 2v2"/>
  <path d="M9 20v2"/>
</>);
export const Edit3 = createIcon(<>
  <path d="M12 20h9"/>
  <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>
</>);
export const Save = createIcon(<>
  <path d="M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/>
  <polyline points="17 21 17 13 7 13 7 21"/>
  <polyline points="7 3 7 8 15 8"/>
</>);
export const Check = createIcon(<polyline points="20 6 9 17 4 12"/>);
export const Search = createIcon(<>
  <circle cx="11" cy="11" r="8"/>
  <line x1="21" x2="16.65" y1="21" y2="16.65"/>
</>);
export const Filter = createIcon(<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>);
export const Calendar = createIcon(<>
  <rect width="18" height="18" x="3" y="4" rx="2" ry="2"/>
  <line x1="16" x2="16" y1="2" y2="6"/>
  <line x1="8" x2="8" y1="2" y2="6"/>
  <line x1="3" x2="21" y1="10" y2="10"/>
</>);
export const FileSpreadsheet = createIcon(<>
  <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>
  <path d="M14 2v4a2 2 0 0 0 2 2h4"/>
  <path d="M8 13h2"/>
  <path d="M14 13h2"/>
  <path d="M8 17h2"/>
  <path d="M14 17h2"/>
</>);
export const ToggleLeft = createIcon(<>
  <rect width="20" height="12" x="2" y="6" rx="6" ry="6"/>
  <circle cx="8" cy="12" r="2"/>
</>);
export const ToggleRight = createIcon(<>
  <rect width="20" height="12" x="2" y="6" rx="6" ry="6"/>
  <circle cx="16" cy="12" r="2"/>
</>);
export const X = createIcon(<>
  <line x1="18" x2="6" y1="6" y2="18"/>
  <line x1="6" x2="18" y1="6" y2="18"/>
</>);
export const Plus = createIcon(<>
  <line x1="12" x2="12" y1="5" y2="19"/>
  <line x1="5" x2="19" y1="12" y2="12"/>
</>);
export const Type = createIcon(<>
  <polyline points="4 7 4 4 20 4 20 7"/>
  <line x1="9" x2="15" y1="20" y2="20"/>
  <line x1="12" x2="12" y1="4" y2="20"/>
</>);
export const Loader2 = createIcon(<>
  <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
</>);
export const Binary = createIcon(<>
  <rect x="14" y="14" width="4" height="6" rx="2"/>
  <rect x="6" y="4" width="4" height="6" rx="2"/>
  <path d="M6 20h4"/>
  <path d="M14 10h4"/>
  <path d="M6 14h2v6"/>
  <path d="M14 4h2v6"/>
</>);
export const AlertOctagon = createIcon(<>
  <polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/>
  <line x1="12" x2="12" y1="8" y2="12"/>
  <line x1="12" x2="12.01" y1="16" y2="16"/>
</>);
export const XCircle = createIcon(<>
  <circle cx="12" cy="12" r="10"/>
  <line x1="15" x2="9" y1="9" y2="15"/>
  <line x1="9" x2="15" y1="9" y2="15"/>
</>);
export const Info = createIcon(<>
  <circle cx="12" cy="12" r="10"/>
  <line x1="12" x2="12" y1="16" y2="12"/>
  <line x1="12" x2="12.01" y1="8" y2="8"/>
</>);
export const ZoomIn = createIcon(<>
  <circle cx="11" cy="11" r="8"/>
  <line x1="21" x2="16.65" y1="21" y2="16.65"/>
  <line x1="11" x2="11" y1="8" y2="14"/>
  <line x1="8" x2="14" y1="11" y2="11"/>
</>);
export const Camera = createIcon(<>
  <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>
  <circle cx="12" cy="13" r="3"/>
</>);
export const Clock = createIcon(<>
  <circle cx="12" cy="12" r="10"/>
  <polyline points="12 6 12 12 16 14"/>
</>);
