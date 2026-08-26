import React from 'react';

export function ResponsiveContainer({ width = '100%', height = '100%', children }) {
  return (
    <div style={{ width, height, position: 'relative' }} className="flex items-center justify-center">
      {children}
    </div>
  );
}

export function PieChart({ width = 200, height = 200, children }) {
  return (
    <svg viewBox="0 0 200 200" className="w-full h-full max-h-48 overflow-visible">
      {children}
    </svg>
  );
}

export function Pie({ data = [], dataKey = 'value', nameKey = 'name', cx = '50%', cy = '50%', innerRadius = 45, outerRadius = 70, children }) {
  const total = data.reduce((acc, curr) => acc + (curr[dataKey] || 0), 0) || 1;
  let accumulatedAngle = 0;

  const center = 100;
  const rIn = innerRadius;
  const rOut = outerRadius;

  const paths = data.map((item, index) => {
    const val = item[dataKey] || 0;
    const sliceAngle = (val / total) * 360;
    const startAngle = accumulatedAngle;
    const endAngle = accumulatedAngle + sliceAngle;
    accumulatedAngle += sliceAngle;

    // Convert polar to cartesian
    const startRad = ((startAngle - 90) * Math.PI) / 180;
    const endRad = ((endAngle - 90) * Math.PI) / 180;

    const x1 = center + rOut * Math.cos(startRad);
    const y1 = center + rOut * Math.sin(startRad);
    const x2 = center + rOut * Math.cos(endRad);
    const y2 = center + rOut * Math.sin(endRad);

    const x3 = center + rIn * Math.cos(endRad);
    const y3 = center + rIn * Math.sin(endRad);
    const x4 = center + rIn * Math.cos(startRad);
    const y4 = center + rIn * Math.sin(startRad);

    const largeArc = sliceAngle > 180 ? 1 : 0;

    const d = sliceAngle >= 359.9
      ? `M ${center} ${center - rOut} A ${rOut} ${rOut} 0 1 1 ${center - 0.01} ${center - rOut} M ${center} ${center - rIn} A ${rIn} ${rIn} 0 1 0 ${center - 0.01} ${center - rIn} Z`
      : `M ${x1} ${y1} A ${rOut} ${rOut} 0 ${largeArc} 1 ${x2} ${y2} L ${x3} ${y3} A ${rIn} ${rIn} 0 ${largeArc} 0 ${x4} ${y4} Z`;

    const color = item.color || (index === 0 ? '#10B981' : index === 1 ? '#EF4444' : '#F59E0B');

    return (
      <path
        key={index}
        d={d}
        fill={color}
        className="transition-all hover:opacity-80 cursor-pointer"
      >
        <title>{`${item[nameKey]}: ${val}`}</title>
      </path>
    );
  });

  return <g>{paths}</g>;
}

export function Cell() {
  return null;
}

export function BarChart({ data = [], margin = {}, children }) {
  const maxVal = Math.max(...data.map(d => d.count || 0), 5);
  const chartHeight = 140;
  const barWidth = 24;
  const gap = 16;
  const totalWidth = Math.max(300, data.length * (barWidth + gap) + 40);

  return (
    <svg viewBox={`0 0 ${totalWidth} 180`} className="w-full h-full max-h-48 overflow-visible">
      {/* Grid lines */}
      <line x1="30" y1="20" x2={totalWidth - 10} y2="20" stroke="#E2E8F0" strokeDasharray="3 3" />
      <line x1="30" y1="80" x2={totalWidth - 10} y2="80" stroke="#E2E8F0" strokeDasharray="3 3" />
      <line x1="30" y1="140" x2={totalWidth - 10} y2="140" stroke="#CBD5E1" strokeWidth="1.5" />

      {data.map((item, idx) => {
        const val = item.count || 0;
        const bHeight = Math.max(4, (val / maxVal) * 110);
        const x = 40 + idx * (barWidth + gap);
        const y = 140 - bHeight;

        return (
          <g key={idx} className="group cursor-pointer">
            <rect
              x={x}
              y={y}
              width={barWidth}
              height={bHeight}
              rx="4"
              fill="#3B82F6"
              className="hover:fill-blue-600 transition-colors"
            >
              <title>{`${item.category}: ${val}`}</title>
            </rect>
            <text
              x={x + barWidth / 2}
              y={y - 4}
              textAnchor="middle"
              className="text-[10px] font-bold fill-slate-700 font-mono"
            >
              {val}
            </text>
            <text
              x={x + barWidth / 2}
              y="156"
              textAnchor="middle"
              className="text-[9px] fill-slate-500 truncate"
            >
              {(item.category || '').substring(0, 7)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

export function Bar() {
  return null;
}

export function AreaChart({ data = [], children }) {
  const maxVal = Math.max(...data.map(d => d.inspections || 0), 8);
  const totalWidth = 320;
  const height = 140;

  const points = data.map((d, i) => {
    const x = 30 + (i / Math.max(1, data.length - 1)) * (totalWidth - 50);
    const y = 140 - ((d.inspections || 0) / maxVal) * 100;
    return { x, y, data: d };
  });

  const pathD = points.length > 0
    ? points.reduce((acc, p, i) => i === 0 ? `M ${p.x} ${p.y}` : `${acc} L ${p.x} ${p.y}`, '')
    : '';

  const areaD = points.length > 0
    ? `${pathD} L ${points[points.length - 1].x} 140 L ${points[0].x} 140 Z`
    : '';

  return (
    <svg viewBox={`0 0 ${totalWidth} 170`} className="w-full h-full max-h-48 overflow-visible">
      <defs>
        <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.4" />
          <stop offset="100%" stopColor="#3B82F6" stopOpacity="0.02" />
        </linearGradient>
      </defs>

      <line x1="30" y1="40" x2={totalWidth - 20} y2="40" stroke="#E2E8F0" strokeDasharray="3 3" />
      <line x1="30" y1="90" x2={totalWidth - 20} y2="90" stroke="#E2E8F0" strokeDasharray="3 3" />
      <line x1="30" y1="140" x2={totalWidth - 20} y2="140" stroke="#CBD5E1" strokeWidth="1.5" />

      {areaD && <path d={areaD} fill="url(#areaGrad)" />}
      {pathD && <path d={pathD} fill="none" stroke="#2563EB" strokeWidth="2.5" strokeLinecap="round" />}

      {points.map((p, idx) => (
        <g key={idx} className="group cursor-pointer">
          <circle cx={p.x} cy={p.y} r="3.5" fill="#2563EB" stroke="#FFFFFF" strokeWidth="2" />
          <text x={p.x} y="156" textAnchor="middle" className="text-[9px] fill-slate-500">
            {p.data.date || p.data.day}
          </text>
          <title>{`${p.data.date || p.data.day}: ${p.data.inspections} inspections`}</title>
        </g>
      ))}
    </svg>
  );
}

export function Area() {
  return null;
}

export function XAxis() {
  return null;
}

export function YAxis() {
  return null;
}

export function Tooltip() {
  return null;
}
