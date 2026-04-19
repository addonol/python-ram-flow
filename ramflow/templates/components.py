"""HTML Components for RAM-FLOW reports.

This module contains atomic HTML fragments used by the PremiumReporter
to assemble the final dashboard without embedding HTML strings in logic files.
"""

# Wrapper grid for the top-level status cards
SUMMARY_CARD_GRID = (
    '<div class="grid grid-cols-1 {grid_cols} gap-6 mb-12 text-center">\n'
    '    <div class="glass p-6 rounded-3xl">\n'
    '        <p class="text-[10px] font-bold text-slate-400 uppercase '
    'tracking-widest mb-1">Bootstrap</p>\n'
    '        <p class="text-2xl font-black text-slate-900">+{start_mem:.2f} MB</p>\n'
    '        <p class="text-[9px] text-slate-400 mt-1 uppercase italic">'
    "Python Baseline</p>\n"
    "    </div>\n"
    "    {django_card}\n"
    '    <div class="glass p-6 rounded-3xl border-b-4 {border}">\n'
    '        <p class="text-[10px] font-bold text-slate-400 uppercase '
    'tracking-widest mb-1">Integrity</p>\n'
    '        <p class="text-xl font-bold {color} italic uppercase">{status}</p>\n'
    '        <p class="text-[9px] text-slate-400 mt-1 uppercase italic">'
    "Final Release Audit</p>\n"
    "    </div>\n"
    "</div>"
)

# Optional card for Django framework overhead
DJANGO_CARD = (
    '<div class="glass p-6 rounded-3xl border-b-4 border-blue-600">\n'
    '    <p class="text-[10px] font-bold text-slate-400 uppercase '
    'tracking-widest mb-1">Ecosystem Bloat</p>\n'
    '    <p class="text-2xl font-black text-slate-900">+{overhead:.2f} MB</p>\n'
    '    <p class="text-[9px] text-slate-400 mt-1 uppercase italic">'
    "Django Infrastructure</p>\n"
    "</div>"
)

# Individual task row with vertical audit trail
TIMELINE_ROW = (
    '<tr class="group transition-all hover:bg-white/80">\n'
    '    <td class="p-6 relative">\n'
    '        <div class="flex items-start gap-4 relative z-20">\n'
    '            <div class="w-10 flex flex-col items-center flex-shrink-0 relative">\n'
    '                <div class="absolute w-[2px] bg-slate-300 z-10 '
    'top-[-24px] bottom-[-24px] group-first:top-1/2"></div>\n'
    '                <div class="mt-1 h-4 w-4 rounded-full border-4 border-white '
    '{dot_color} shadow-md z-20"></div>\n'
    "            </div>\n"
    '            <div class="flex-1">\n'
    '                <p class="text-base font-bold text-slate-800 leading-tight">{label}</p>\n'
    '                <div class="flex items-center gap-3 mt-2">\n'
    '                    <span class="text-[11px] mono text-blue-600 font-black '
    'bg-blue-50/80 border border-blue-100 px-2 py-0.5 rounded-md">{time}</span>\n'
    '                    <span class="text-[11px] text-slate-400 font-semibold '
    'mono uppercase tracking-wider">{extra}</span>\n'
    "                </div>\n"
    "            </div>\n"
    "        </div>\n"
    "    </td>\n"
    '    <td class="p-6 text-center">\n'
    '        <div class="inline-flex flex-col items-center px-4 py-2 rounded-2xl '
    '{bg_badge} border border-slate-100/50 min-w-[100px]">\n'
    '            <span class="mono text-base font-black {color}">{diff:+.2f} MB</span>\n'
    '            <span class="text-[9px] font-black text-slate-400 uppercase '
    'tracking-widest mt-0.5">Net Self</span>\n'
    "        </div>\n"
    "    </td>\n"
    '    <td class="p-6 text-right">\n'
    '        <p class="text-xs font-bold text-slate-400 mono">{dur:.3f}s</p>\n'
    '        <p class="text-[9px] text-slate-300 font-black uppercase mt-1">Duration</p>\n'
    "    </td>\n"
    "</tr>"
)

# Footer row for final process reclamation state
RECLAMATION_FOOTER = (
    '<tr class="bg-slate-50/50 border-t-2 border-slate-100 group">\n'
    '    <td class="p-6 relative">\n'
    '        <div class="flex items-center gap-4 relative z-20">\n'
    '            <div class="w-10 flex flex-col items-center flex-shrink-0 relative">\n'
    '                <div class="absolute w-[2px] bg-slate-300 z-10 '
    'top-[-24px] h-[calc(50%+24px)]"></div>\n'
    '                <div class="h-4 w-4 rounded-full border-4 border-white '
    '{dot_f} shadow-sm z-20"></div>\n'
    "            </div>\n"
    '            <p class="font-bold text-slate-500 text-xs uppercase '
    'tracking-widest">Final Reclamation Audit</p>\n'
    "        </div>\n"
    "    </td>\n"
    '    <td class="p-6 text-center">\n'
    '        <div class="flex flex-col items-center px-4 py-2 rounded-2xl '
    'bg-white/50 border border-slate-200/50 min-w-[100px]">\n'
    '            <span class="mono text-base font-black text-slate-700">{leak:+.2f} MB</span>\n'
    '            <span class="text-[10px] font-black {color} uppercase '
    'tracking-wide">{status}</span>\n'
    "        </div>\n"
    "    </td>\n"
    '    <td class="p-6 text-right"><span class="text-[10px] font-bold '
    'text-slate-400 mono uppercase">Audit End</span></td>\n'
    "</tr>"
)

# Component: Wrapper for a complete table section (System or Logic)
TABLE_SECTION_WRAPPER = (
    '<section class="{margin_class}">\n'
    '    <div class="flex items-center justify-between mb-6 px-6">\n'
    '        <h3 class="text-xs font-black text-slate-400 uppercase '
    'tracking-[0.3em] flex items-center gap-3">\n'
    '            <span class="w-1.5 h-1.5 rounded-full bg-blue-600"></span>\n'
    "            {title}\n"
    "        </h3>\n"
    '        <div class="px-3 py-1 bg-slate-100 rounded-full border '
    'border-slate-200/50">\n'
    '            <span class="text-[10px] font-black text-slate-600 mono '
    'uppercase tracking-widest">\n'
    "                {count} {unit} recorded\n"
    "            </span>\n"
    "        </div>\n"
    "    </div>\n"
    '    <main class="glass rounded-[2.5rem] overflow-hidden">\n'
    '        <table class="w-full text-left border-collapse">\n'
    '            <tbody class="divide-y divide-slate-100/50">\n'
    "                {rows}\n"
    "                {footer}\n"
    "            </tbody>\n"
    "        </table>\n"
    "    </main>\n"
    "</section>"
)

# Component: Full System Context with dual blocks
SYSTEM_CONTEXT_FOOTER = (
    '<footer class="mt-16 animate-fade-in space-y-8">\n'
    "    <!-- BANNER: CERTIFICATION STATUS -->\n"
    '    <div class="p-10 glass rounded-[2.5rem] border-slate-200 flex '
    'flex-col md:flex-row justify-between items-center gap-6">\n'
    '        <div class="flex items-center gap-6">\n'
    '            <div class="px-5 py-3 rounded-2xl {bg} border '
    'border-{color}/20 flex items-center gap-3">\n'
    '                <span class="flex h-3 w-3 rounded-full bg-{color} '
    'animate-pulse"></span>\n'
    '                <span class="text-xs font-black text-{color} '
    'tracking-widest uppercase">{status}</span>\n'
    "            </div>\n"
    '            <p class="text-base font-bold text-slate-400 mono">'
    "Residual: {leak:+.2f} MB</p>\n"
    "        </div>\n"
    '        <div class="text-right">\n'
    '            <p class="text-[11px] font-black text-slate-400 '
    'uppercase tracking-widest mb-1">Audit Session</p>\n'
    '            <p class="text-lg font-black text-blue-600 mono">'
    "{timestamp}</p>\n"
    "        </div>\n"
    "    </div>\n"
    "\n"
    '    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">\n'
    "        <!-- BLOCK 1: HOST INFRASTRUCTURE -->\n"
    '        <div class="p-10 glass rounded-[2.5rem] border-slate-200">\n'
    '            <h3 class="text-xs font-black text-slate-400 uppercase '
    'tracking-[0.2em] mb-8 flex items-center gap-2">\n'
    '                <span class="h-2 w-2 rounded-full bg-slate-300"></span> '
    "Host Infrastructure</h3>\n"
    '            <div class="grid grid-cols-2 gap-y-8">\n'
    '                <div><p class="text-[10px] font-black text-slate-400 '
    'uppercase mb-1">Hostname</p>\n'
    '                <p class="text-base font-black text-slate-800 mono">'
    "{host}</p></div>\n"
    '                <div><p class="text-[10px] font-black text-slate-400 '
    'uppercase mb-1">User Identity</p>\n'
    '                <p class="text-base font-black text-slate-800 mono">'
    "{user}</p></div>\n"
    '                <div><p class="text-[10px] font-black text-slate-400 '
    'uppercase mb-1">Hardware Engine</p>\n'
    '                <p class="text-base font-black text-slate-800 mono">'
    "{cpu} Cores / {total_ram:.1f} GB</p></div>\n"
    '                <div><p class="text-[10px] font-black text-slate-400 '
    'uppercase mb-1">Platform</p>\n'
    '                <p class="text-base font-black text-slate-800 mono">'
    "{os}</p></div>\n"
    "            </div>\n"
    "        </div>\n"
    "\n"
    "        <!-- BLOCK 2: RAM-FLOW CONFIGURATION -->\n"
    '        <div class="p-10 glass rounded-[2.5rem] border-slate-200">\n'
    '            <h3 class="text-xs font-black text-blue-600 uppercase '
    'tracking-[0.2em] mb-8 flex items-center gap-2">\n'
    '                <span class="h-2 w-2 rounded-full bg-blue-600"></span> '
    "Audit Parameters</h3>\n"
    '            <div class="grid grid-cols-2 gap-y-8">\n'
    '                <div><p class="text-[10px] font-black text-slate-400 '
    'uppercase mb-1">Threshold / Hard Limit</p>\n'
    '                <p class="text-base font-black text-slate-800 mono">'
    "{threshold} / {hard_limit} MB</p></div>\n"
    '                <div><p class="text-[10px] font-black text-slate-400 '
    'uppercase mb-1">Leak Sensitivity</p>\n'
    '                <p class="text-base font-black text-slate-800 mono">'
    "{medium_limit} / {high_limit} MB</p></div>\n"
    '                <div><p class="text-[10px] font-black text-slate-400 '
    'uppercase mb-1">Archiving Root</p>\n'
    '                <p class="text-base font-black text-slate-800 mono">'
    "{reports_dir}</p></div>\n"
    "            </div>\n"
    "        </div>\n"
    "    </div>\n"
    "</footer>"
)


# Helper icon for tooltips
INFO_ICON = (
    '<span class="info-tip ml-1.5">\n'
    '    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="3" class="opacity-50">\n'
    '        <circle cx="12" cy="12" r="10"></circle>'
    '<line x1="12" y1="16" x2="12" y2="12"></line>\n'
    '        <line x1="12" y1="8" x2="12.01" y2="8"></line>\n'
    "    </svg>\n"
    '    <span class="tip-text">{text}</span>\n'
    "</span>"
)

# Individual KPI Card with Tooltip support
KPI_CARD_WITH_HELP = (
    '<div class="glass p-6 border-b-4 {border_color}">\n'
    '    <div class="flex items-center mb-3">\n'
    '        <p class="text-[11px] font-black text-slate-400 uppercase '
    'tracking-widest">{label}</p>\n'
    "        {info_icon}\n"
    "    </div>\n"
    '    <p class="{val_size} font-black text-slate-900 mono">{value}'
    '<span class="{unit_class}">{unit}</span></p>\n'
    '    <p class="text-xs text-slate-500 mt-2 font-medium">{subtext}</p>\n'
    "</div>"
)

# Component: Visual timeline chart for Memory Peak vs Start
PEAK_ANALYSIS_CHART = (
    '<div class="glass p-8">\n'
    '    <h3 class="text-[11px] font-black text-slate-400 uppercase '
    'tracking-[0.2em] mb-8">Memory Expansion Journey</h3>\n'
    '    <div class="space-y-10 relative py-4">\n'
    '        <div class="absolute left-0 right-0 top-1/2 h-px bg-slate-100 '
    '-translate-y-1/2"></div>\n'
    '        <div class="flex justify-between items-center relative">\n'
    '            <div class="flex flex-col items-center">\n'
    '                <div class="text-[10px] font-black text-slate-400 '
    'mono mb-2">{start_val:.1f} MB</div>\n'
    '                <div class="h-4 w-4 rounded-full bg-white border-4 '
    'border-slate-200 z-10"></div>\n'
    '                <p class="text-[11px] font-bold text-slate-400 mt-2">START</p>\n'
    "            </div>\n"
    '            <div class="absolute left-2 h-1.5 {bar_accent} rounded-full '
    'opacity-20" style="width: calc(100% - 16px);"></div>\n'
    '            <div class="flex flex-col items-center">\n'
    '                <div class="text-[10px] font-black {txt_color} '
    'mono mb-2">{peak_val:.1f} MB</div>\n'
    '                <div class="h-6 w-6 rounded-full bg-white border-4 '
    'border-{dot_border}-500 z-10 shadow-lg"></div>\n'
    '                <p class="text-[11px] font-black {txt_color} mt-2">PEAK</p>\n'
    "            </div>\n"
    "        </div>\n"
    "    </div>\n"
    '    <div class="mt-10 pt-6 border-t border-slate-50 text-sm text-slate-600">\n'
    '        The process footprint expanded by <span class="font-black {txt_color}">'
    "x{multiplier:.1f}</span> compared to baseline.\n"
    "    </div>\n"
    "</div>"
)

# Component: Individual Top Memory Consumer Row
TOP_CONSUMER_ROW = (
    '<div class="flex justify-between items-center p-3 bg-white/40 '
    'rounded-xl mb-2 border border-slate-100">\n'
    '    <span class="text-[10px] font-black text-slate-700 uppercase">{label}</span>\n'
    '    <span class="mono text-xs font-black text-blue-600">+{diff:.2f} MB</span>\n'
    "</div>"
)

# Component: Trend Analysis Block
TREND_BLOCK = (
    '<div class="glass p-8 border-l-4 border-{bg_base}-500">\n'
    '    <h3 class="text-[11px] font-black text-slate-400 uppercase mb-6">Memory Trend Analysis</h3>\n'
    '    <div class="flex items-center gap-4 mb-3">\n'
    '        <span class="flex h-3 w-3 rounded-full bg-{bg_base}-500 animate-pulse"></span>\n'
    '        <p class="text-xl font-black {color} italic uppercase tracking-tighter">{verdict}</p>\n'
    "    </div>\n"
    '    <p class="text-sm text-slate-500 italic">"{desc}"</p>\n'
    "</div>"
)

# Component: Main Overview Wrapper
OVERVIEW_WRAPPER = (
    '<div class="space-y-10 animate-fade-in">\n'
    '    <h3 class="text-xs font-black text-slate-400 uppercase tracking-[0.3em] px-4 flex items-center gap-3">\n'
    '        <span class="h-2 w-2 rounded-full bg-blue-600"></span> Executive Dashboard\n'
    "    </h3>\n"
    "    {kpis}\n"
    '    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">\n'
    "        {trend_block}\n"
    "        {peak_chart}\n"
    "    </div>\n"
    '    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">\n'
    '        <div class="glass p-8 md:col-span-2">\n'
    '            <h3 class="text-[11px] font-black text-slate-400 uppercase mb-6">Top Memory Consumers (Self Impact)</h3>\n'
    '            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">{top_consumers}</div>\n'
    "        </div>\n"
    '        <div class="glass p-8 flex flex-col justify-center bg-slate-50/50">\n'
    '            <h3 class="text-[11px] font-black text-slate-400 uppercase mb-4">Ecosystem Impact</h3>\n'
    '            <p class="text-xs text-slate-500 leading-relaxed">\n'
    '                Your <span class="font-bold text-slate-700">{infra_label}</span> '
    'represents <span class="font-black text-blue-600">{infra_ratio:.1f}%</span> of the peak footprint.\n'
    "            </p>\n"
    "        </div>\n"
    "    </div>\n"
    "</div>"
)

# Component: Grid wrapper for the 4 main KPIs
KPI_SCORECARD_GRID = (
    '<div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">\n'
    "    {card_safety}\n"
    "    {card_footprint}\n"
    "    {card_efficiency}\n"
    "    {card_leak}\n"
    "</div>"
)
