#!/usr/bin/env python3
"""
Generate PRISMA 2020 flow diagram for the systematic review.
Produces a publication-ready figure using matplotlib.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
except ImportError:
    raise ImportError("matplotlib required: pip install matplotlib")


class PRISMADiagram:
    """Generates PRISMA 2020 compliant flow diagram."""

    # PRISMA 2020 box colours
    COLOURS = {
        'identification': '#D6EAF8',
        'screening':      '#D5F5E3',
        'included':       '#FCF3CF',
        'excluded':       '#FDEDEC',
        'border':         '#2C3E50',
        'arrow':          '#2C3E50',
        'text':           '#1A252F'
    }

    def __init__(self, counts: Dict[str, int]):
        """
        Initialize with study counts.

        Args:
            counts: Dictionary with counts for each PRISMA stage. Expected keys:
                - records_identified_databases
                - records_identified_other (grey lit, handsearch, etc.)
                - records_after_dedup
                - records_screened
                - records_excluded_screening
                - full_text_assessed
                - full_text_excluded
                - full_text_excluded_no_effect_size (optional detail)
                - full_text_excluded_no_learning_outcome (optional detail)
                - full_text_excluded_wrong_design (optional detail)
                - full_text_excluded_other (optional detail)
                - studies_included
                - effect_sizes_included
        """
        self.counts = counts

    def _draw_box(self, ax, x: float, y: float, width: float, height: float,
                  text: str, colour: str, fontsize: int = 9):
        """Draw a rounded rectangle box with centred text."""
        box = FancyBboxPatch(
            (x - width / 2, y - height / 2),
            width, height,
            boxstyle="round,pad=0.02",
            facecolor=colour,
            edgecolor=self.COLOURS['border'],
            linewidth=1.2,
            zorder=2
        )
        ax.add_patch(box)
        ax.text(
            x, y, text,
            ha='center', va='center',
            fontsize=fontsize,
            color=self.COLOURS['text'],
            wrap=True,
            zorder=3
        )

    def _draw_arrow(self, ax, x1: float, y1: float, x2: float, y2: float):
        """Draw a downward arrow between boxes."""
        ax.annotate(
            '',
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='->', color=self.COLOURS['arrow'],
                lw=1.5
            ),
            zorder=1
        )

    def _draw_side_arrow(self, ax, x1: float, y1: float, x2: float, y2: float):
        """Draw a horizontal side arrow to exclusion box."""
        ax.annotate(
            '',
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='->', color=self.COLOURS['arrow'],
                lw=1.2, connectionstyle='arc3,rad=0'
            ),
            zorder=1
        )

    def generate(self, output_path: str, dpi: int = 300,
                 title: str = "PRISMA 2020 Flow Diagram"):
        """
        Generate and save the PRISMA flow diagram.

        Args:
            output_path: Path to save the figure (PNG or PDF)
            dpi: Resolution for raster output
            title: Figure title
        """
        c = self.counts

        fig, ax = plt.subplots(figsize=(10, 14))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')

        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        # Phase labels
        phase_x = 0.6
        ax.text(phase_x, 13.2, "Identification", fontsize=10, fontweight='bold',
                color=self.COLOURS['text'], ha='center', rotation=90, va='center')
        ax.text(phase_x, 9.5, "Screening", fontsize=10, fontweight='bold',
                color=self.COLOURS['text'], ha='center', rotation=90, va='center')
        ax.text(phase_x, 5.5, "Eligibility", fontsize=10, fontweight='bold',
                color=self.COLOURS['text'], ha='center', rotation=90, va='center')
        ax.text(phase_x, 2.0, "Included", fontsize=10, fontweight='bold',
                color=self.COLOURS['text'], ha='center', rotation=90, va='center')

        # Phase separators
        for y_line in [11.6, 7.7, 3.3]:
            ax.axhline(y=y_line, xmin=0.1, xmax=0.9, color='#BDC3C7',
                       linewidth=0.8, linestyle='--')

        # ---- IDENTIFICATION ----
        n_db = c.get('records_identified_databases', 0)
        n_other = c.get('records_identified_other', 0)
        n_dedup = c.get('records_after_dedup', 0)
        n_dup_removed = (n_db + n_other) - n_dedup

        self._draw_box(
            ax, 4.0, 13.0, 3.5, 0.9,
            f"Records identified from databases\n(n = {n_db:,})",
            self.COLOURS['identification']
        )
        self._draw_box(
            ax, 7.5, 13.0, 2.5, 0.9,
            f"Records from other sources\n(grey lit, handsearch)\n(n = {n_other:,})",
            self.COLOURS['identification'], fontsize=8
        )
        self._draw_arrow(ax, 4.0, 12.55, 4.0, 12.05)
        self._draw_box(
            ax, 4.0, 11.75, 3.5, 0.9,
            f"Records after duplicates removed\n(n = {n_dedup:,})\n"
            f"Duplicates removed: {n_dup_removed:,}",
            self.COLOURS['identification']
        )

        # ---- SCREENING ----
        n_screened = c.get('records_screened', n_dedup)
        n_excl_screen = c.get('records_excluded_screening', 0)
        n_full_text = c.get('full_text_assessed', 0)

        self._draw_arrow(ax, 4.0, 11.3, 4.0, 10.75)
        self._draw_box(
            ax, 4.0, 10.45, 3.5, 0.9,
            f"Records screened\n(n = {n_screened:,})",
            self.COLOURS['screening']
        )
        self._draw_side_arrow(ax, 5.75, 10.45, 6.3, 10.45)
        self._draw_box(
            ax, 7.8, 10.45, 2.8, 0.9,
            f"Records excluded\n(title/abstract screen)\n(n = {n_excl_screen:,})",
            self.COLOURS['excluded'], fontsize=8
        )
        self._draw_arrow(ax, 4.0, 10.0, 4.0, 9.3)
        self._draw_box(
            ax, 4.0, 9.0, 3.5, 0.9,
            f"Full-text articles assessed\nfor eligibility\n(n = {n_full_text:,})",
            self.COLOURS['screening']
        )

        # ---- ELIGIBILITY (full-text exclusions) ----
        n_ft_excl = c.get('full_text_excluded', 0)
        n_no_es = c.get('full_text_excluded_no_effect_size', 0)
        n_no_lo = c.get('full_text_excluded_no_learning_outcome', 0)
        n_wrong_d = c.get('full_text_excluded_wrong_design', 0)
        n_other_excl = c.get('full_text_excluded_other', 0)

        excl_lines = [f"Full-text excluded (n = {n_ft_excl:,}):"]
        if n_no_es:
            excl_lines.append(f"  No extractable effect size: {n_no_es:,}")
        if n_no_lo:
            excl_lines.append(f"  No learning outcome: {n_no_lo:,}")
        if n_wrong_d:
            excl_lines.append(f"  Wrong design: {n_wrong_d:,}")
        if n_other_excl:
            excl_lines.append(f"  Other: {n_other_excl:,}")

        self._draw_side_arrow(ax, 5.75, 9.0, 6.3, 7.5)
        self._draw_box(
            ax, 7.8, 7.5, 2.8, 2.5,
            '\n'.join(excl_lines),
            self.COLOURS['excluded'], fontsize=7.5
        )

        # ---- INCLUDED ----
        n_included = c.get('studies_included', 0)
        n_effects = c.get('effect_sizes_included', 0)

        self._draw_arrow(ax, 4.0, 8.55, 4.0, 7.75)
        self._draw_box(
            ax, 4.0, 6.5, 3.5, 2.5,
            f"Studies included in meta-analysis\n(n = {n_included:,})\n\n"
            f"Effect sizes (Hedges' g) included\n(n = {n_effects:,})",
            self.COLOURS['included']
        )

        # Title
        fig.suptitle(title, fontsize=12, fontweight='bold', y=0.98,
                     color=self.COLOURS['text'])

        plt.tight_layout(rect=[0, 0, 1, 0.97])

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=dpi, bbox_inches='tight', facecolor='white')
        plt.close()

        logger.info(f"PRISMA diagram saved: {output}")
        print(f"PRISMA 2020 flow diagram saved: {output}")


def generate_prisma_diagram(counts: Dict[str, int],
                            output_path: str = "figures/prisma_flow.png",
                            title: str = "PRISMA 2020 Flow Diagram — "
                                         "Effects of Agentic AI on Learning Outcomes"):
    """
    Convenience function to generate the PRISMA flow diagram.

    Args:
        counts: Dictionary with PRISMA stage counts
        output_path: Output file path (.png or .pdf)
        title: Figure title
    """
    diagram = PRISMADiagram(counts)
    diagram.generate(output_path, dpi=300, title=title)


if __name__ == "__main__":
    import argparse
    import json

    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(
        description="Generate PRISMA 2020 flow diagram"
    )
    parser.add_argument('--counts', type=str,
                        help='JSON file with PRISMA stage counts')
    parser.add_argument('--output', default='figures/prisma_flow.png',
                        help='Output path (.png or .pdf)')

    args = parser.parse_args()

    if args.counts:
        with open(args.counts) as f:
            counts = json.load(f)
    else:
        # Example counts for demonstration
        counts = {
            'records_identified_databases': 3847,
            'records_identified_other': 142,
            'records_after_dedup': 2913,
            'records_screened': 2913,
            'records_excluded_screening': 2541,
            'full_text_assessed': 372,
            'full_text_excluded': 289,
            'full_text_excluded_no_effect_size': 124,
            'full_text_excluded_no_learning_outcome': 88,
            'full_text_excluded_wrong_design': 51,
            'full_text_excluded_other': 26,
            'studies_included': 83,
            'effect_sizes_included': 217
        }

    generate_prisma_diagram(counts, args.output)
