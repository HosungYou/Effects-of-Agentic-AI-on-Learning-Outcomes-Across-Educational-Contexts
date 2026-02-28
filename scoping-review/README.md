# Trust Calibration as the Missing Link in Educational AI Design: A Critical Review with Scoping Review

## Project Overview

This directory contains all materials for the scoping review paper preceding the main meta-analysis on "Effects of Agentic AI on Learning Outcomes Across Educational Contexts."

**Paper title**: Trust Calibration as the Missing Link in Educational AI Design: A Critical Review with Scoping Review
**Target journal**: International Journal of Educational Technology in Higher Education (IF ~8.6, Open Access)
**Estimated length**: 8,000-10,000 words

## Core Thesis

In educational AI systems, optimal human oversight design depends on learners' trust calibration state. Trust calibration is achieved through internal mechanisms (self-directed learning) or external mechanisms (teacher/system checkpoints). This two-level framework bridges the micro-level trust literature (Wang et al., 2025) with the macro-level oversight design literature (Lee & See, 2004; de Visser et al., 2020).

## Research Questions

1. How is trust in AI conceptualized and measured in educational AI research?
2. What theoretical frameworks guide trust research in educational AI?
3. To what extent does existing research address trust calibration and human oversight design?
4. What does a two-level framework connecting learner trust to oversight design look like?

## Directory Structure

```
scoping-review/
  README.md                          # This file
  docs/
    search_strategy.md               # Complete DB-specific search strings (copy-pasteable)
    screening_criteria.md            # PCC inclusion/exclusion criteria
    charting_form.md                 # Data charting form specification
    paper_outline.md                 # Full paper structure with section-by-section notes
    theoretical_foundation.md        # Wang et al. (2025) analysis + 2-level framework
    execution_plan.md                # Step-by-step execution plan
  data/
    00_search_results/               # Raw exports from each DB
    01_deduplicated/                 # After dedup
    02_screened/                     # Screening decisions
    03_charted/                      # Data charting spreadsheet
  scripts/
    scr_dedup_merge.py               # Dedup adapted for scoping review
    scr_ai_screening.py             # AI screening with PCC criteria
    scr_generate_prisma.py          # PRISMA-ScR flow diagram generator
    scr_dedup_config.json           # Dedup configuration
  manuscript/
    draft.md                         # Full paper draft
  figures/
    (generated during analysis)
```

## Methodology

- **Framework**: JBI methodology for scoping reviews (Peters et al., 2020)
- **Reporting**: PRISMA-ScR (PRISMA Extension for Scoping Reviews)
- **Search scope**: 2015-2026, English, 6 databases
- **Databases**: Web of Science, Scopus, ERIC, PsycINFO, Semantic Scholar (API), OpenAlex (API)

## Quick Start (for the machine with DB access)

1. Clone or pull this repo
2. Open `docs/search_strategy.md` for copy-pasteable search strings
3. Run manual searches in WoS, Scopus, ERIC, PsycINFO
4. Export results to `data/00_search_results/` (CSV or RIS format)
5. Run `python scripts/scr_dedup_merge.py --config scripts/scr_dedup_config.json`
6. Follow `docs/execution_plan.md` for remaining steps

## Key References

- Wang, H., et al. (2025). Trust in generative AI in education: S-O-R model.
- Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. *Human Factors*.
- de Visser, E. J., et al. (2020). Towards a theory of longitudinal trust calibration in human-robot teams. *IJSR*.
- Bastani, H., et al. (2025). Generative AI can harm learning. *PNAS*.
- Peters, M. D. J., et al. (2020). Updated methodological guidance for the conduct of scoping reviews. *JBI Evidence Synthesis*.

## Relationship to Main Meta-Analysis

This scoping review is a **preceding publication** that establishes the theoretical and methodological groundwork for the meta-analysis. It:
- Maps the trust landscape in educational AI research
- Identifies the gap (trust calibration --> oversight design link is absent)
- Proposes a two-level framework that the meta-analysis will empirically test
- Demonstrates that the field needs systematic quantitative synthesis (motivating the meta-analysis)
