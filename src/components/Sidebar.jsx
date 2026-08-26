import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  ScanLine, 
  Globe2, 
  ClipboardList, 
  Package, 
  BookOpenCheck, 
  FileText, 
  ShieldCheck,
  Info
} from 'lucide-react';

const navItems = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard, badge: null },
  { name: 'Scan Product', path: '/scan', icon: ScanLine, badge: 'OCR + AI' },
  { name: 'Online Listing', path: '/ecommerce', icon: Globe2, badge: 'Rule 6(11)' },
  { name: 'Inspections', path: '/inspections', icon: ClipboardList, badge: null },
  { name: 'Product Repository', path: '/products', icon: Package, badge: null },
  { name: 'Rule Repository', path: '/rules', icon: BookOpenCheck, badge: 'Config' },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between shrink-0 min-h-[calc(100vh-85px)] select-none">
      <div className="py-4 px-3 space-y-1">
        <div className="px-3 pb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
          Enforcement Modules
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30 font-semibold'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`
              }
            >
              <div className="flex items-center gap-3">
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-950/60 border border-blue-400/30 text-blue-200 font-mono">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </div>

      {/* Advisory Legal Disclaimer Box */}
      <div className="p-3 m-3 rounded-lg bg-slate-800/60 border border-slate-700/80 text-[11px] text-slate-400 space-y-2">
        <div className="flex items-center gap-1.5 text-slate-200 font-semibold">
          <ShieldCheck className="w-4 h-4 text-amber-400" />
          <span>Statutory Authority</span>
        </div>
        <p className="leading-relaxed text-[10.5px]">
          AI findings provide initial screening support. Final compounding & enforcement decisions rest with the inspecting officer.
        </p>
        <div className="text-[10px] text-slate-500 font-mono">
          Legal Metrology Act, 2009
        </div>
      </div>
    </aside>
  );
}
