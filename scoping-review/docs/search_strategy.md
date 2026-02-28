# Search Strategy — Trust in Educational AI Scoping Review

## Overview

- **Search design**: 2-block PCC structure (no outcome filter to maximize sensitivity)
- **Date range**: 2015-2026
- **Language**: English
- **Last search date**: [TO BE FILLED]

## Search Blocks

### Block 1 — Trust Concept

```
"trust in AI" OR "AI trust" OR "trust calibration" OR "calibrated trust"
OR "overtrust" OR "over-reliance" OR "distrust" OR "undertrust"
OR "reliance on AI" OR "resistance to AI" OR "human-AI trust"
OR "appropriate trust" OR "trust in generative AI" OR "trust in ChatGPT"
OR "trustworthiness" AND ("AI" OR "artificial intelligence")
```

### Block 2 — Educational AI Context

```
"education*" OR "learning" OR "teaching" OR "higher education"
OR "university" OR "K-12" OR "intelligent tutoring" OR "AI tutor*"
OR "ChatGPT" OR "generative AI" OR "LLM" OR "edtech"
OR "AI-assisted learning" OR "AI chatbot" OR "conversational agent"
```

### Combined

```
(Block 1) AND (Block 2)
```

Filters: 2015-2026, English language

---

## Database-Specific Search Strings (Copy-Paste Ready)

### 1. Web of Science (Core Collection)

**Search field**: TS (Topic Search = title, abstract, author keywords, Keywords Plus)

```
TS=(("trust in AI" OR "AI trust" OR "trust calibration" OR "overtrust"
     OR "over-reliance" OR "distrust" OR "reliance on AI" OR "resistance to AI"
     OR "human-AI trust" OR "appropriate trust" OR "trustworthiness")
    AND
    ("education*" OR "learning" OR "teaching" OR "higher education"
     OR "university" OR "K-12" OR "intelligent tutoring" OR "AI tutor*"
     OR "ChatGPT" OR "generative AI" OR "LLM" OR "edtech"))
```

**Filters to apply manually**:
- Publication Years: 2015-2026
- Language: English
- Document Types: Article, Review Article, Proceedings Paper, Early Access

**Export format**: Plain text (Full Record and Cited References) or CSV

**Expected yield**: 100-250 records

---

### 2. Scopus

**Search field**: TITLE-ABS-KEY

```
TITLE-ABS-KEY(("trust in AI" OR "AI trust" OR "trust calibration"
               OR "overtrust" OR "over-reliance" OR "distrust"
               OR "reliance on AI" OR "resistance to AI"
               OR "human-AI trust" OR "appropriate trust")
              AND
              ("education*" OR "learning" OR "teaching"
               OR "higher education" OR "intelligent tutoring"
               OR "ChatGPT" OR "generative AI" OR "LLM" OR "edtech"))
AND PUBYEAR > 2014 AND LANGUAGE(english)
```

**Filters to apply manually**:
- Document type: Article, Conference Paper, Review
- Source type: Journal, Conference Proceeding

**Export format**: CSV (all fields including abstract)

**Expected yield**: 150-350 records

---

### 3. ERIC (via EBSCOhost)

**Search mode**: Boolean/Phrase

```
(TX "trust in AI" OR TX "AI trust" OR TX "trust calibration"
 OR TX "overtrust" OR TX "reliance on AI" OR TX "distrust")
AND
(DE "Artificial Intelligence" OR TX "educational AI" OR TX "ChatGPT"
 OR TX "generative AI" OR TX "intelligent tutoring" OR TX "AI tutor")
```

**Limiters**:
- Published Date: 2015-01 to 2026-12
- Language: English
- Source Types: Academic Journals, Reports, Conference Materials

**Export format**: RIS or CSV (include abstract)

**Expected yield**: 30-80 records

---

### 4. PsycINFO (via EBSCOhost or Ovid)

#### EBSCOhost version:

```
(TX "trust in AI" OR TX "AI trust" OR TX "trust calibration"
 OR TX "overtrust" OR TX "reliance" OR TX "distrust")
AND
(TX "education*" OR TX "learning" OR TX "ChatGPT" OR TX "generative AI"
 OR TX "intelligent tutoring" OR DE "Artificial Intelligence")
```

#### Ovid version:

```
("trust in AI" OR "AI trust" OR "trust calibration"
 OR overtrust OR "over-reliance" OR distrust).tw.
AND
(education* OR learning OR teaching OR "higher education"
 OR "ChatGPT" OR "generative AI" OR "intelligent tutoring").tw.
```

**Limiters**:
- Publication Year: 2015-2026
- Language: English
- Document Type: Journal Article, Dissertation Abstract

**Export format**: RIS or CSV

**Expected yield**: 50-120 records

---

### 5. Semantic Scholar (API — Claude executes)

**API endpoint**: `https://api.semanticscholar.org/graph/v1/paper/search`

**Query parameters**:
```json
{
  "query": "trust calibration educational AI",
  "year": "2015-2026",
  "fieldsOfStudy": "Education,Computer Science,Psychology",
  "fields": "title,abstract,authors,year,externalIds,citationCount,journal,url",
  "limit": 100
}
```

**Additional queries** (run all):
1. `"trust in AI" education learning`
2. `"overtrust" OR "distrust" educational AI`
3. `"human-AI trust" education`
4. `"trust calibration" learning`
5. `"reliance on AI" education`

**Expected yield**: 80-200 unique records

---

### 6. OpenAlex (API — Claude executes)

**API endpoint**: `https://api.openalex.org/works`

**Query parameters**:
```
filter=default.search:"trust in AI" AND "education",from_publication_date:2015-01-01,language:en
select=id,doi,title,display_name,publication_year,authorships,abstract_inverted_index,primary_location,cited_by_count,concepts,type
per_page=100
```

**Additional filter queries**:
1. `"trust calibration" AND "learning"`
2. `"overtrust" AND "education"`
3. `"human-AI trust" AND "educational"`

**Expected yield**: 100-250 unique records

---

## Supplementary Search

### Backward citation tracking

From included studies, check reference lists for additional relevant studies.

### Forward citation tracking

Run forward citation search on these seed papers:
- Wang, H., et al. (2025) — Trust in generative AI in education
- Lee, J. D., & See, K. A. (2004) — Trust in automation
- de Visser, E. J., et al. (2020) — Longitudinal trust calibration
- Bastani, H., et al. (2025) — Generative AI can harm learning

### Hand search journals (latest 3 issues)

- *Computers & Education*
- *International Journal of AI in Education*
- *British Journal of Educational Technology*
- *Internet and Higher Education*

---

## Search Documentation Template

Complete after each database search:

| Field | Value |
|-------|-------|
| Database | |
| Date searched | |
| Search string used | (copy exact string) |
| Filters applied | |
| Records retrieved | |
| Export filename | |
| Notes | |

---

## Yield Estimates

| Source | Estimated Raw | After Dedup (est.) |
|--------|--------------|-------------------|
| Web of Science | 100-250 | — |
| Scopus | 150-350 | — |
| ERIC | 30-80 | — |
| PsycINFO | 50-120 | — |
| Semantic Scholar | 80-200 | — |
| OpenAlex | 100-250 | — |
| **Total raw** | **510-1250** | — |
| **After dedup** | — | **250-600** |
| **After title/abstract screening** | — | **40-80** |
| **After full-text** | — | **15-40** |

## Contingency

- **If > 600 after dedup**: Tighten by requiring "trust" in title; narrow to 2019+
- **If < 30 after dedup**: Broaden by adding "acceptance" and "adoption" to Block 1
