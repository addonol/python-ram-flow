"""HTML Reporting module for RAM-FLOW.

Generates premium, standalone performance dashboards with executive KPIs,
visual execution timelines, and detailed system metadata.
"""

import os
import json
import psutil
import platform
import socket
import getpass
from typing import List, Dict, Any
from datetime import datetime
from . import config
from .templates import components


class Reporter:
    """Engine to transform memory tracking history into high-end HTML reports.

    Attributes:
        history (List[Dict[str, Any]]): Sequential log of all monitored tasks.
        start_mem (float): Initial memory baseline captured at initialization (MB).
        env (str): Execution environment name (e.g., PRODUCTION, DEVELOPMENT).
        threshold (int): Memory delta limit (MB) for task highlighting.
        django_overhead (float): Captured ecosystem initialization cost (MB).
    """

    def __init__(
        self,
        history: List[Dict[str, Any]],
        start_mem: float,
        env: str,
        threshold: int,
        django_overhead: float = 0.0,
    ):
        """Initializes the reporter with session data.

        Args:
            history (List[Dict[str, Any]]): Sequential task logs.
            start_mem (float): Initial memory baseline in MB.
            env (str): Environment name for branding and metadata.
            threshold (int): Memory delta in MB before triggering alerts.
            django_overhead (float): Framework load cost in MB.
        """
        self.history = history
        self.start_mem = start_mem
        self.env = env
        self.threshold = threshold
        self.django_overhead = django_overhead

    def _analyze_memory_trend(self, residual_leak: float) -> Dict[str, str]:
        """Analyzes cumulative memory pressure to detect persistent bloating.

        This algorithm evaluates the 'Memory Plateau' effect. If the process
        stays at a high RSS level without returning to baseline, or if it
        shows a linear growth, it flags a potential leak.

        Args:
            residual_leak (float): The final net memory delta after execution
                and reclamation (MB).

        Returns:
            Dict[str, str]: A dictionary containing:
                - verdict (str): Plain-English status (e.g., 'CRITICAL BLOAT').
                - desc (str): Technical explanation of the trend.
                - color (str): CSS text color class for the UI.
                - bg_base (str): Tailwind base color name for badges and icons.
        """

        logic_tasks = [t for t in self.history if t.get("type") != "system"]

        if len(logic_tasks) < 2:
            return {
                "verdict": "Awaiting Data",
                "desc": "Insufficient data points to establish a reliable trend.",
                "color": "text-slate-400",
                "bg_base": "slate",
            }

        if residual_leak < config.LEAK_MEDIUM_LIMIT:
            return {
                "verdict": "STABLE ENGINE",
                "desc": "Memory was successfully reclaimed. No persistent bloat detected.",
                "color": "text-emerald-600",
                "bg_base": "emerald",
            }

        # Calculate Cumulative Levels
        current_level = 0.0
        levels = []
        for t in logic_tasks:
            current_level += t["diff"]
            levels.append(current_level)

        # Calculate the overall pressure change
        pressure_slope = (levels[-1] - levels[0]) / len(levels)

        if levels[-1] > 50 and pressure_slope >= -1.0:
            return {
                "verdict": "CRITICAL BLOAT",
                "desc": "High memory plateau detected. Resources are locked.",
                "color": "text-rose-600",
                "bg_base": "rose",
            }
        elif pressure_slope > 2.0:
            return {
                "verdict": "WARNING: LEAKING",
                "desc": "Step-by-step accumulation detected. Review loops.",
                "color": "text-orange-600",
                "bg_base": "orange",
            }

        return {
            "verdict": "STABLE ENGINE",
            "desc": "Memory levels are returning to baseline safely.",
            "color": "text-emerald-600",
            "bg_base": "emerald",
        }

    def _get_summary_cards(self, residual_leak: float) -> str:
        """Generates the top summary cards (Bootstrap, Django, Integrity).

        This method orchestrates the high-level status grid. It evaluates the
        final process integrity and determines if the ecosystem bloat should
        be displayed based on the captured framework overhead.

        Args:
            residual_leak (float): The final net memory delta after execution
                and reclamation (MB). Used to trigger the SECURE/BLOATED status.

        Returns:
            str: A formatted HTML grid containing the key high-level status cards.
        """
        is_clean = residual_leak < config.LEAK_MEDIUM_LIMIT
        django_html = ""
        if self.django_overhead > 0:
            django_html = components.DJANGO_CARD.format(overhead=self.django_overhead)

        return components.SUMMARY_CARD_GRID.format(
            grid_cols="md:grid-cols-3"
            if self.django_overhead > 0
            else "md:grid-cols-2",
            start_mem=self.start_mem,
            django_card=django_html,
            border="border-emerald-500" if is_clean else "border-rose-500",
            color="text-emerald-500" if is_clean else "text-rose-500",
            status="SECURE" if is_clean else "BLOATED",
        )

    def _get_kpi_scorecard(self, residual_leak: float, peak_footprint: float) -> str:
        """Generates the main KPI grid with interactive tooltips.

        Calculates high-level metrics including host safety, process peak,
        allocation efficiency, and final integrity probability. Each card
        is enriched with technical explanations via tooltips.

        Args:
            residual_leak (float): The final net memory delta after execution
                and reclamation (MB).
            peak_footprint (float): The maximum Resident Set Size (RSS) reached
                during the entire process lifecycle (MB).

        Returns:
            str: A formatted HTML grid containing the four executive KPI cards
                with their respective icons, values, and help texts.
        """
        from .templates import components

        vm = psutil.virtual_memory()
        safety_margin = (vm.available / vm.total) * 100
        total_time = sum(t.get("duration", 0.0) for t in self.history)
        total_mem = sum(t["diff"] for t in self.history if t["diff"] > 0)
        efficiency = total_mem / total_time if total_time > 0 else 0.0

        if residual_leak < config.LEAK_MEDIUM_LIMIT:
            prob, color = "Low", "emerald"
        elif residual_leak < config.LEAK_HIGH_LIMIT:
            prob, color = "Medium", "orange"
        else:
            prob, color = "High", "rose"

        help_texts = {
            "safety": "RAM available on the host. Below 10% indicates critical OOM risk.",
            "footprint": "Maximum physical RAM (Peak RSS) used during the entire session.",
            "efficiency": "Allocation speed. High ratios indicate memory-greedy logic.",
            "leak": "Risk of unreleased memory based on the final audit delta.",
        }

        card_safety = components.KPI_CARD_WITH_HELP.format(
            border_color="border-blue-600",
            label="Safety Margin",
            info_icon=components.INFO_ICON.format(text=help_texts["safety"]),
            value=f"{safety_margin:.1f}",
            unit="%",
            val_size="text-3xl",
            unit_class="text-sm ml-0.5 text-slate-400",
            subtext="Host Available RAM",
        )

        card_footprint = components.KPI_CARD_WITH_HELP.format(
            border_color="border-blue-600",
            label="Process Footprint",
            info_icon=components.INFO_ICON.format(text=help_texts["footprint"]),
            value=f"{peak_footprint:.1f}",
            unit="MB",
            val_size="text-3xl",
            unit_class="text-sm ml-1 text-slate-400",
            subtext="Peak RSS Usage",
        )

        card_efficiency = components.KPI_CARD_WITH_HELP.format(
            border_color="border-blue-600",
            label="Efficiency Ratio",
            info_icon=components.INFO_ICON.format(text=help_texts["efficiency"]),
            value=f"{efficiency:.1f}",
            unit="MB/s",
            val_size="text-3xl",
            unit_class="text-sm ml-1 text-slate-400 italic",
            subtext="Allocation Speed",
        )

        card_leak = components.KPI_CARD_WITH_HELP.format(
            border_color=f"border-{color}-500",
            label="Leak Probability",
            info_icon=components.INFO_ICON.format(text=help_texts["leak"]),
            value=prob,
            unit="",
            val_size="text-2xl italic uppercase",
            unit_class="",
            subtext="Integrity Verdict",
        )

        return components.KPI_SCORECARD_GRID.format(
            card_safety=card_safety,
            card_footprint=card_footprint,
            card_efficiency=card_efficiency,
            card_leak=card_leak,
        )

    def _get_peak_analysis_html(self, peak_footprint: float) -> str:
        """Visual comparison of the memory expansion journey.

        Constructs a horizontal infographic comparing the initial infrastructure
        baseline to the maximum memory footprint reached. It applies dynamic
        branding based on the expansion multiplier.

        Args:
            peak_footprint (float): The maximum Resident Set Size (RSS) reached
                during the process lifecycle (MB).

        Returns:
            str: A formatted HTML component representing the memory growth journey.
        """
        start_total = self.start_mem + self.django_overhead
        multiplier = (peak_footprint / start_total) if start_total > 0 else 0.0

        txt_color = "text-blue-600"
        bar_accent = "bg-blue-600"

        if multiplier > 3:
            txt_color, bar_accent = "text-rose-600", "bg-rose-600"
        elif multiplier > 1.5:
            txt_color, bar_accent = "text-orange-600", "bg-orange-600"

        return components.PEAK_ANALYSIS_CHART.format(
            start_val=start_total,
            peak_val=peak_footprint,
            multiplier=multiplier,
            txt_color=txt_color,
            bar_accent=bar_accent,
            dot_border=bar_accent.split("-")[-2],
        )

    def _get_overview_diagnostics(self, residual_leak: float) -> str:
        """Assembles the executive dashboard content for the primary report tab.

        This method acts as the main orchestrator for the 'Overview' view. It
        calculates global process statistics, evaluates infrastructure impact,
        identifies the top 3 memory-consuming tasks, and aggregates all sub-components
        into a unified dashboard layout.

        Args:
            residual_leak (float): The final net memory delta after execution
                and reclamation (MB). Used for trend analysis and integrity check.

        Returns:
            str: The complete HTML content for the Executive Overview tab,
                integrating KPIs, trend cards, peak infographics, and consumer lists.
        """
        logic_tasks = [t for t in self.history if t.get("type") != "system"]
        max_task_delta = max([t["diff"] for t in logic_tasks]) if logic_tasks else 0.0
        peak_footprint = self.start_mem + self.django_overhead + max_task_delta

        infra_label = (
            "Infrastructure (Django + Bootstrap)"
            if self.django_overhead > 0
            else "Core Infrastructure"
        )
        infra_total = self.start_mem + self.django_overhead
        infra_ratio = (
            (infra_total / peak_footprint * 100) if peak_footprint > 0 else 0.0
        )

        trend_data = self._analyze_memory_trend(residual_leak)
        trend_html = components.TREND_BLOCK.format(**trend_data)

        kpi_html = self._get_kpi_scorecard(residual_leak, peak_footprint)
        peak_html = self._get_peak_analysis_html(peak_footprint)

        sorted_history = sorted(logic_tasks, key=lambda x: x["diff"], reverse=True)[:3]
        top_rows = "".join(
            [
                components.TOP_CONSUMER_ROW.format(label=t["label"], diff=t["diff"])
                for t in sorted_history
            ]
        )

        return components.OVERVIEW_WRAPPER.format(
            kpis=kpi_html,
            trend_block=trend_html,
            peak_chart=peak_html,
            top_consumers=top_rows,
            infra_label=infra_label,
            infra_ratio=infra_ratio,
        )

    def _generate_table_section(
        self, section_type: str, title: str, residual_leak: float = 0.0
    ) -> str:
        """Builds a structured table section for system or logic history.

        This method filters the execution history by type and transforms each
        entry into a visual timeline row. It applies conditional formatting
        (Rose color) for tasks exceeding the memory threshold and appends a
        reclamation audit footer for business logic sections.

        Args:
            section_type (str): The category of tasks to include.
                Expected values: 'system' or 'logic'.
            title (str): The display title for the section header.
            residual_leak (float, optional): The final memory delta in MB.
                Only used to render the footer in 'logic' sections. Defaults to 0.0.

        Returns:
            str: A complete HTML section containing the titled header, the
                operation counter, and the formatted table of events.
        """
        filtered = [t for t in self.history if t.get("type", "logic") == section_type]
        if not filtered:
            return ""

        rows_html = []

        for t in filtered:
            is_hot = t["diff"] > self.threshold
            rows_html.append(
                components.TIMELINE_ROW.format(
                    dot_color="bg-rose-500" if is_hot else "bg-blue-500",
                    bg_badge="bg-rose-50/50" if is_hot else "bg-slate-50/30",
                    color="text-rose-600 font-bold" if is_hot else "text-blue-700",
                    label=t["label"],
                    time=t.get("time", "--:--"),
                    extra=t.get("extra", ""),
                    diff=t["diff"],
                    dur=t["duration"],
                )
            )

        footer_html = ""
        if section_type == "logic":
            is_clean = residual_leak < config.LEAK_MEDIUM_LIMIT
            footer_html = components.RECLAMATION_FOOTER.format(
                dot_f="bg-emerald-400" if is_clean else "bg-rose-400",
                leak=residual_leak,
                color="text-emerald-500" if is_clean else "text-rose-500",
                status="Stabilized" if is_clean else "Bloated",
            )

        return components.TABLE_SECTION_WRAPPER.format(
            margin_class="mb-16" if section_type == "system" else "mb-8",
            title=title,
            count=len(filtered),
            unit="Operation" if len(filtered) == 1 else "Operations",
            rows="".join(rows_html),
            footer=footer_html,
        )

    def _get_metadata_html(self, residual_leak: float = 0.0) -> str:
        """Generates the dual-block system context (Host vs Config).

        This method assembles the technical background of the audit. It captures
        hardware specifications (CPU, RAM, OS) and maps them alongside the
        active RAM-FLOW configuration (Thresholds, Limits, Directories) to
        provide full transparency for post-mortem analysis.

        Args:
            residual_leak (float): The final net memory delta after execution
                and reclamation (MB). Used to determine the certification status.

        Returns:
            str: A formatted HTML footer containing the certification banner
                and the two-column technical specification grid.
        """

        is_certified = residual_leak < config.LEAK_MEDIUM_LIMIT

        return components.SYSTEM_CONTEXT_FOOTER.format(
            status="CERTIFIED LEAK-FREE" if is_certified else "MEMORY BLOAT DETECTED",
            color="emerald-500" if is_certified else "rose-500",
            bg="bg-emerald-50" if is_certified else "bg-rose-50",
            leak=residual_leak,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            host=socket.gethostname(),
            user=getpass.getuser(),
            cpu=psutil.cpu_count(logical=False),
            total_ram=psutil.virtual_memory().total / (1024**3),
            os=f"{platform.system()} ({platform.release()})",
            threshold=self.threshold,
            hard_limit=config.HARD_LIMIT,
            medium_limit=config.LEAK_MEDIUM_LIMIT,
            high_limit=config.LEAK_HIGH_LIMIT,
            reports_dir=config.REPORTS_DIR,
        )

    def render(
        self, output_path: str = "audit_report.html", residual_leak: float = 0.0
    ) -> None:
        """Orchestrates the final HTML assembly and writes it to disk.

        This method loads the base template and CSS, triggers the generation
        of all dashboard components (scorecards, tables, metadata), and
        prepares a raw JSON export for interoperability. It then performs
        placeholder substitution and saves a standalone, self-contained
        HTML report.

        Args:
            output_path (str): The target filesystem path where the HTML report
                will be saved. Defaults to "audit_report.html".
            residual_leak (float): The final net memory delta after execution
                and reclamation (MB).

        Returns:
            None
        """
        base_path = os.path.dirname(__file__)
        tmpl_path = os.path.join(base_path, "templates", "report_template.html")
        css_path = os.path.join(base_path, "templates", "assets", "style.css")

        with open(tmpl_path, "r", encoding="utf-8") as f:
            template = f.read()
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        system_table = self._generate_table_section("system", "Infrastructure & Setup")
        logic_table = self._generate_table_section(
            "logic", "Command Execution Flow", residual_leak
        )

        raw_export = {
            "metadata": {
                "env": self.env,
                "timestamp": datetime.now().isoformat(),
                "residual_leak_mb": residual_leak,
                "django_overhead_mb": self.django_overhead,
                "threshold_mb": self.threshold,
            },
            "history": self.history,
        }

        replacements = {
            "{{ custom_css }}": css_content,
            "{{ env }}": self.env,
            "{{ summary_cards }}": self._get_summary_cards(residual_leak),
            "{{ table_content }}": system_table + logic_table,
            "{{ metadata }}": self._get_metadata_html(residual_leak),
            "{{ overview_diagnostics }}": self._get_overview_diagnostics(residual_leak),
            "{{ raw_json_data }}": json.dumps(raw_export),
        }

        final_html = template
        for placeholder, value in replacements.items():
            final_html = final_html.replace(placeholder, str(value))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)
