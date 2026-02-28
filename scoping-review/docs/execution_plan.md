# Execution Plan — Trust in Educational AI Scoping Review

## Prerequisites

- Machine with access to Web of Science, Scopus, ERIC, PsycINFO
- Python 3.9+ with: pandas, numpy, matplotlib, anthropic
- ANTHROPIC_API_KEY environment variable set (for AI-assisted screening)

---

## Phase 1: Search Execution (1.5 hours)

### Step 1.1: Manual Database Searches (YOU do this)

Open each database and execute the search strings from `docs/search_strategy.md`.

**Order**: WoS --> Scopus --> ERIC --> PsycINFO

For each database:
1. Navigate to the database
2. Copy-paste the exact search string from `docs/search_strategy.md`
3. Apply filters (2015-2026, English)
4. Note the total hits
5. Export ALL results:
   - **WoS**: Export as "Plain Text File" or CSV, select "Full Record"
   - **Scopus**: Export as CSV, select all fields including Abstract
   - **ERIC**: Export as RIS or CSV
   - **PsycINFO**: Export as RIS or CSV
6. Save exports to `data/00_search_results/` with naming convention:
   - `wos_trust_education_YYYYMMDD.csv`
   - `scopus_trust_education_YYYYMMDD.csv`
   - `eric_trust_education_YYYYMMDD.ris`
   - `psycinfo_trust_education_YYYYMMDD.ris`

**Fill in this table after each search**:

| Database | Date | Records | Export Filename | Notes |
|----------|------|---------|-----------------|-------|
| Web of Science | | | | |
| Scopus | | | | |
| ERIC | | | | |
| PsycINFO | | | | |

### Step 1.2: API Searches (Claude does this)

Claude will execute:
- Semantic Scholar API search
- OpenAlex API search

Outputs saved to:
- `data/00_search_results/semantic_scholar_YYYYMMDD.csv`
- `data/00_search_results/openalex_YYYYMMDD.csv`

### Step 1.3: Citation Tracking (after initial search)

Forward citation search on seed papers:
- Wang et al. (2025) — Trust in GenAI education (S-O-R)
- Bastani et al. (2025) — GenAI can harm learning

Use Google Scholar "Cited by" or Semantic Scholar API.

---

## Phase 2: Deduplication + Screening (2.5 hours)

### Step 2.1: Configure Dedup (10 min)

Edit `scripts/scr_dedup_config.json` to point to your actual export files:

```json
{
  "search_files": [
    {
      "filepath": "data/00_search_results/wos_trust_education_YYYYMMDD.csv",
      "source_label": "Web_of_Science",
      "column_map": {"TI": "title", "AB": "abstract", "AU": "authors", "PY": "year", "DI": "doi", "SO": "journal"}
    },
    {
      "filepath": "data/00_search_results/scopus_trust_education_YYYYMMDD.csv",
      "source_label": "Scopus",
      "column_map": {"Title": "title", "Abstract": "abstract", "Authors": "authors", "Year": "year", "DOI": "doi", "Source title": "journal"}
    }
  ]
}
```

### Step 2.2: Run Dedup (20 min)

```bash
cd scoping-review
python scripts/scr_dedup_merge.py --config scripts/scr_dedup_config.json --output data/01_deduplicated
```

Output: `data/01_deduplicated/merged_deduplicated.csv`

### Step 2.3: AI-Assisted Screening (1.5 hours)

```bash
python scripts/scr_ai_screening.py --input data/01_deduplicated/merged_deduplicated.csv --output data/02_screened
```

Output:
- `data/02_screened/screening_decisions.jsonl`
- `data/02_screened/screening_decisions.csv`
- `data/02_screened/screening_summary.json`

### Step 2.4: Human Verification (30 min)

1. Open `data/02_screened/screening_decisions.csv`
2. Review all UNCERTAIN records --> decide INCLUDE or EXCLUDE
3. Spot-check 10% random sample of EXCLUDE decisions
4. Check all records citing Wang et al. (2025), Lee & See (2004), de Visser et al. (2020)
5. Save verified decisions to `data/02_screened/screening_verified.csv`

---

## Phase 3: Full-Text Assessment + Data Charting (2.5 hours)

### Step 3.1: Retrieve Full Texts

For each INCLUDED record from screening:
1. Try DOI link first
2. If not open access, use university library proxy
3. Save PDFs to a local folder (not tracked in git -- too large)
4. Note accessibility in a tracking spreadsheet

### Step 3.2: Data Charting

Use the charting form from `docs/charting_form.md`.

For each included paper:
1. Read abstract + introduction + methods + results + discussion
2. Fill in all charting variables
3. Pay special attention to:
   - Trust definition (exact quote if provided)
   - Theoretical framework
   - Whether calibration is discussed
   - Whether oversight is discussed
4. Save to `data/03_charted/charting_data.csv`

**Time estimate**: 5-8 min per paper = 1.5-5 hours for 15-40 papers

### Step 3.3: Verify Charting

Review each charted entry for:
- Completeness (no empty required fields)
- Accuracy (spot-check against source text)
- Consistency (same coding conventions across papers)

---

## Phase 4: Analysis + Synthesis (2 hours)

### Step 4.1: Descriptive Mapping (30 min)

Generate frequency tables for:
- Publication year distribution
- AI system type distribution
- Trust construct distribution
- Theoretical framework distribution
- Trust measurement approach distribution
- Trust calibration coverage (Yes/No)
- Oversight coverage (Yes/No)

### Step 4.2: Thematic Analysis (30 min)

Identify trust conceptualization themes:
1. Trust as belief/attitude (Mayer et al. tradition)
2. Trust as behavioral reliance (Lee & See tradition)
3. Trust as acceptance factor (TAM/UTAUT tradition)
4. Trust calibration (de Visser et al. tradition)
5. Trust as S-O-R mediator (Wang et al. tradition)

### Step 4.3: Gap Analysis + Framework Mapping (30 min)

Map each study to the two-level framework:
- Level 1 evidence count
- Level 2 evidence count
- Level 1+2 combined count
- Create Table 5 (framework mapping)

### Step 4.4: Write Synthesis Narrative (30 min)

Three claims to support:
1. Trust is studied predominantly at individual level (Level 1) with theoretical fragmentation
2. Wang et al. (2025) provides the most complete empirical model but stops at individual use behavior
3. Trust calibration as a system design target (Level 2) is absent --> the missing link

---

## Phase 5: Paper Writing (3-4 hours)

### Priority order:
1. Section 5: Two-Level Framework (core contribution)
2. Section 2: Conceptual Foundation
3. Section 4: Results (requires data)
4. Section 1: Introduction
5. Sections 3, 6, 7: Methods, Implications, Conclusion

### See `docs/paper_outline.md` for detailed section-by-section guidance.

### Writing workspace: `manuscript/draft.md`

---

## Phase 6: Finalization

### Figures
1. Generate PRISMA-ScR flow: `python scripts/scr_generate_prisma.py --counts data/prisma_counts.json`
2. Create Two-Level Framework diagram (Figma or draw.io)
3. Create trust theme map (if applicable)

### Appendices
- [ ] Appendix A: PRISMA-ScR 22-item checklist
- [ ] Appendix B: Complete search strings (copy from `docs/search_strategy.md`)
- [ ] Appendix C: Data charting form (copy from `docs/charting_form.md`)
- [ ] Appendix D: Characteristics of included studies (from `data/03_charted/`)

### Final Checks
- [ ] PRISMA-ScR 22-item checklist all addressed
- [ ] All search strings documented with dates and counts
- [ ] AI-assisted screening transparently reported
- [ ] Every framework claim maps to scoping review evidence
- [ ] Word count: 8,000-10,000
- [ ] APA 7th edition formatting
- [ ] All figures high resolution (300 DPI)
- [ ] References complete and consistent

---

## File Checklist

After execution, these files should exist:

```
data/00_search_results/
  wos_trust_education_YYYYMMDD.csv
  scopus_trust_education_YYYYMMDD.csv
  eric_trust_education_YYYYMMDD.ris
  psycinfo_trust_education_YYYYMMDD.ris
  semantic_scholar_YYYYMMDD.csv
  openalex_YYYYMMDD.csv

data/01_deduplicated/
  merged_deduplicated.csv
  dedup_report.json

data/02_screened/
  screening_decisions.jsonl
  screening_decisions.csv
  screening_summary.json
  screening_verified.csv

data/03_charted/
  charting_data.csv

manuscript/
  draft.md

figures/
  prisma_scr_flow.png
  two_level_framework.png
```
