#!/usr/bin/env python3
"""
Generate PRISMA-ScR (Scoping Review) flow diagram.

Adapted from parent project's generate_prisma.py with scoping-review-specific
labels and stages.

Usage:
    python scr_generate_prisma.py --counts ../data/prisma_counts.json \
                                   --output ../figures/prisma_scr_flow.png
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch
except ImportError:
    raise ImportError("matplotlib required: pip install matplotlib")


class PRISMAScRDiagram:
    """Generates PRISMA-ScR compliant flow diagram for scoping reviews."""

    COLOURS = {
        "identification": "#D6EAF8",
        "screening": "#D5F5E3",
        "included": "#FCF3CF",
        "excluded": "#FDEDEC",
        "border": "#2C3E50",
        "arrow": "#2C3E50",
        "text": "#1A252F"
    }

    def __init__(self, counts: Dict[str, int]):
        self.counts = counts

    def _draw_box(self, ax, x, y, width, height, text, colour, fontsize=9):
        box = FancyBboxPatch(
            (x - width / 2, y - height / 2),
            width, height,
            boxstyle="round,pad=0.02",
            facecolor=colour,
            edgecolor=self.COLOURS["border"],
            linewidth=1.2,
            zorder=2
        )
        ax.add_patch(box)
        ax.text(
            x, y, text,
            ha="center", va="center",
            fontsize=fontsize,
            color=self.COLOURS["text"],
            wrap=True,
            zorder=3
        )

    def _draw_arrow(self, ax, x1, y1, x2, y2):
        ax.annotate(
            "",
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color=self.COLOURS["arrow"], lw=1.5),
            zorder=1
        )

    def _draw_side_arrow(self, ax, x1, y1, x2, y2):
        ax.annotate(
            "",
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color=self.COLOURS["arrow"],
                            lw=1.2, connectionstyle="arc3,rad=0"),
            zorder=1
        )

    def generate(self, output_path: str, dpi: int = 300):
        c = self.counts

        fig, ax = plt.subplots(figsize=(11, 14))
        ax.set_xlim(0, 11)
        ax.set_ylim(0, 14)
        ax.axis("off")
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        # Phase labels
        phase_x = 0.6
        ax.text(phase_x, 12.5, "Identification", fontsize=10, fontweight="bold",
                color=self.COLOURS["text"], ha="center", rotation=90, va="center")
        ax.text(phase_x, 8.5, "Screening", fontsize=10, fontweight="bold",
                color=self.COLOURS["text"], ha="center", rotation=90, va="center")
        ax.text(phase_x, 4.0, "Included", fontsize=10, fontweight="bold",
                color=self.COLOURS["text"], ha="center", rotation=90, va="center")

        # Separators
        for y_line in [10.8, 5.5]:
            ax.axhline(y=y_line, xmin=0.1, xmax=0.9, color="#BDC3C7",
                        linewidth=0.8, linestyle="--")

        # ---- IDENTIFICATION ----
        n_db = c.get("records_databases", 0)
        n_api = c.get("records_api", 0)
        n_other = c.get("records_other", 0)
        n_total = n_db + n_api + n_other
        n_dedup = c.get("records_after_dedup", 0)
        n_dup_removed = n_total - n_dedup

        # DB sources
        db_text = (
            f"Records from databases\n"
            f"(WoS, Scopus, ERIC, PsycINFO)\n"
            f"(n = {n_db:,})"
        )
        self._draw_box(ax, 3.0, 13.0, 3.2, 1.0, db_text,
                        self.COLOURS["identification"], fontsize=8)

        # API sources
        api_text = (
            f"Records from APIs\n"
            f"(Semantic Scholar, OpenAlex)\n"
            f"(n = {n_api:,})"
        )
        self._draw_box(ax, 6.8, 13.0, 3.0, 1.0, api_text,
                        self.COLOURS["identification"], fontsize=8)

        # Other sources
        if n_other > 0:
            other_text = f"Citation tracking\n& hand search\n(n = {n_other:,})"
            self._draw_box(ax, 9.8, 13.0, 2.0, 1.0, other_text,
                            self.COLOURS["identification"], fontsize=7)

        # Arrows down
        self._draw_arrow(ax, 3.0, 12.5, 4.5, 11.8)
        self._draw_arrow(ax, 6.8, 12.5, 4.5, 11.8)

        # Dedup
        dedup_text = (
            f"Records after duplicates removed\n"
            f"(n = {n_dedup:,})\n"
            f"Duplicates removed: {n_dup_removed:,}"
        )
        self._draw_box(ax, 4.5, 11.3, 3.5, 0.9, dedup_text,
                        self.COLOURS["identification"])

        # ---- SCREENING ----
        n_screened = c.get("records_screened", n_dedup)
        n_excl_screen = c.get("records_excluded_screening", 0)
        n_uncertain = c.get("records_uncertain", 0)

        self._draw_arrow(ax, 4.5, 10.85, 4.5, 10.25)
        screen_text = (
            f"Title/abstract screened\n"
            f"(AI-assisted with human verification)\n"
            f"(n = {n_screened:,})"
        )
        self._draw_box(ax, 4.5, 9.8, 3.5, 0.9, screen_text,
                        self.COLOURS["screening"], fontsize=8)

        # Exclusion box
        excl_text = (
            f"Records excluded\n"
            f"(title/abstract)\n"
            f"(n = {n_excl_screen:,})"
        )
        self._draw_side_arrow(ax, 6.25, 9.8, 7.5, 9.8)
        self._draw_box(ax, 9.0, 9.8, 2.5, 0.9, excl_text,
                        self.COLOURS["excluded"], fontsize=8)

        # Uncertain
        if n_uncertain > 0:
            unc_text = f"Uncertain records\nfor human review\n(n = {n_uncertain:,})"
            self._draw_box(ax, 9.0, 8.5, 2.5, 0.7, unc_text,
                            self.COLOURS["excluded"], fontsize=7)

        # Full-text
        n_fulltext = c.get("full_text_sought", 0)
        n_ft_not_retrieved = c.get("full_text_not_retrieved", 0)
        n_ft_assessed = c.get("full_text_assessed", 0)
        n_ft_excluded = c.get("full_text_excluded", 0)

        self._draw_arrow(ax, 4.5, 9.35, 4.5, 8.65)
        ft_text = (
            f"Full-text sources sought\n"
            f"for retrieval\n"
            f"(n = {n_fulltext:,})"
        )
        self._draw_box(ax, 4.5, 8.2, 3.5, 0.8, ft_text,
                        self.COLOURS["screening"], fontsize=8)

        if n_ft_not_retrieved > 0:
            nr_text = f"Not retrieved\n(n = {n_ft_not_retrieved:,})"
            self._draw_side_arrow(ax, 6.25, 8.2, 7.5, 8.2)
            self._draw_box(ax, 9.0, 8.2, 2.5, 0.6, nr_text,
                            self.COLOURS["excluded"], fontsize=8)

        self._draw_arrow(ax, 4.5, 7.8, 4.5, 7.2)
        assessed_text = (
            f"Full-text sources assessed\n"
            f"for eligibility\n"
            f"(n = {n_ft_assessed:,})"
        )
        self._draw_box(ax, 4.5, 6.8, 3.5, 0.8, assessed_text,
                        self.COLOURS["screening"], fontsize=8)

        # Full-text exclusion reasons
        excl_reasons = c.get("full_text_exclusion_reasons", {})
        ft_excl_lines = [f"Full-text excluded (n = {n_ft_excluded:,}):"]
        for reason, count in excl_reasons.items():
            ft_excl_lines.append(f"  {reason}: {count:,}")

        if ft_excl_lines:
            self._draw_side_arrow(ax, 6.25, 6.8, 7.5, 6.5)
            self._draw_box(ax, 9.0, 6.5, 2.5, 1.5,
                            "\n".join(ft_excl_lines),
                            self.COLOURS["excluded"], fontsize=7)

        # ---- INCLUDED ----
        n_included = c.get("sources_included", 0)

        self._draw_arrow(ax, 4.5, 6.4, 4.5, 5.0)
        included_text = (
            f"Sources included in\n"
            f"scoping review\n"
            f"(n = {n_included:,})"
        )
        self._draw_box(ax, 4.5, 4.5, 3.5, 1.0, included_text,
                        self.COLOURS["included"])

        # Breakdown
        n_empirical = c.get("included_empirical", 0)
        n_conceptual = c.get("included_conceptual", 0)
        n_reviews = c.get("included_reviews", 0)

        if n_empirical or n_conceptual or n_reviews:
            breakdown = []
            if n_empirical:
                breakdown.append(f"Empirical: {n_empirical}")
            if n_conceptual:
                breakdown.append(f"Conceptual: {n_conceptual}")
            if n_reviews:
                breakdown.append(f"Reviews: {n_reviews}")

            self._draw_box(ax, 4.5, 3.2, 3.5, 0.8,
                            "Study types:\n" + " | ".join(breakdown),
                            self.COLOURS["included"], fontsize=8)

        # Title
        fig.suptitle(
            "PRISMA-ScR Flow Diagram\n"
            "Trust Calibration in Educational AI: Scoping Review",
            fontsize=11, fontweight="bold", y=0.99,
            color=self.COLOURS["text"]
        )

        plt.tight_layout(rect=[0, 0, 1, 0.96])

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=dpi, bbox_inches="tight", facecolor="white")
        plt.close()

        logger.info(f"PRISMA-ScR diagram saved: {output}")
        print(f"PRISMA-ScR flow diagram saved: {output}")


def main():
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(
        description="Generate PRISMA-ScR flow diagram for scoping review"
    )
    parser.add_argument("--counts", type=str,
                        help="JSON file with PRISMA-ScR stage counts")
    parser.add_argument("--output", default="../figures/prisma_scr_flow.png",
                        help="Output path (.png or .pdf)")

    args = parser.parse_args()

    if args.counts:
        with open(args.counts) as f:
            counts = json.load(f)
    else:
        # Placeholder counts for demonstration
        counts = {
            "records_databases": 0,
            "records_api": 0,
            "records_other": 0,
            "records_after_dedup": 0,
            "records_screened": 0,
            "records_excluded_screening": 0,
            "records_uncertain": 0,
            "full_text_sought": 0,
            "full_text_not_retrieved": 0,
            "full_text_assessed": 0,
            "full_text_excluded": 0,
            "full_text_exclusion_reasons": {},
            "sources_included": 0,
            "included_empirical": 0,
            "included_conceptual": 0,
            "included_reviews": 0
        }
        print("Using placeholder counts. Provide --counts with actual data.")

    output = Path(args.output)
    if not output.is_absolute():
        output = Path(__file__).resolve().parent.parent / args.output

    diagram = PRISMAScRDiagram(counts)
    diagram.generate(str(output))


if __name__ == "__main__":
    main()
