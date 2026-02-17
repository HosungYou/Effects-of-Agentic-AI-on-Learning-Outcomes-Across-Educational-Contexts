# Literature Search Strategy

## Overview

This document provides the comprehensive search strategy for the systematic review and meta-analysis of Agentic AI effects on learning outcomes across educational contexts. The strategy follows PRISMA 2020 guidelines and is designed to ensure comprehensive coverage while maintaining precision.

---

## 1. Databases

### 1.1 Primary Databases

| Database | Coverage | Rationale | Expected Hits |
|----------|----------|-----------|---------------|
| **Web of Science (Core Collection)** | Multidisciplinary, SSCI/SCI indexed journals | Gold standard for systematic reviews; citation tracking capabilities | 2,000-3,000 |
| **Scopus** | Broader coverage than WoS; includes more conference proceedings | Captures technical implementations; broader journal coverage | 3,000-5,000 |
| **ERIC (Education Resources Information Center)** | Education-specific database | Core education research; U.S. Department of Education | 500-1,000 |
| **PsycINFO** | Psychology & behavioral sciences | Learning psychology, educational psychology, cognitive science | 500-1,000 |
| **IEEE Xplore** | Engineering & computer science | AI/ML technical implementations, educational technology | 1,000-2,000 |
| **ACM Digital Library** | Computing & information technology | Computer-supported learning, HCI in education, intelligent systems | 500-1,000 |

**Total estimated hits before deduplication**: 7,500-13,000
**Estimated after deduplication**: 4,000-8,000

### 1.2 Supplementary Sources

- **Google Scholar**: Limited systematic search; used for citation tracking only
- **SSRN**: Educational research pre-prints and working papers
- **EdArXiv**: Education research pre-prints
- **ProQuest Dissertations & Theses**: Dissertation research (grey literature)

---

## 2. Search Terms

### 2.1 Concept Blocks

The search strategy uses three concept blocks combined with AND operators:

```
(AI AGENT BLOCK) AND (LEARNING OUTCOME BLOCK) AND (EDUCATIONAL CONTEXT BLOCK)
```

### 2.2 Block 1: AI Agent (Intervention)

**Core terms** (high precision):
- "AI agent*"
- "intelligent agent*"
- "agentic AI"
- "autonomous agent*"
- "AI-powered agent*"

**Related terms** (expanded coverage):
- "virtual agent*"
- "pedagogical agent*"
- "conversational agent*"
- "intelligent tutoring system*"
- "ITS"
- "AI chatbot*"
- "AI tutor*"
- "AI assistant*"
- "multi-agent system*"
- "AI teaching assistant*"
- "virtual tutor*"
- "embodied conversational agent*"
- "dialogue system*" (when combined with education/learning)

**Exclusions** (NOT operators):
- NOT "travel agent*"
- NOT "real estate agent*"
- NOT "software agent*" (unless combined with educational terms)

### 2.3 Block 2: Learning Outcome (Dependent Variable)

**Achievement terms**:
- "learning outcome*"
- "academic achievement"
- "academic performance"
- "learning performance"
- "test score*"
- "exam score*"
- "grade*"

**Knowledge/skill terms**:
- "knowledge gain*"
- "skill acquisition"
- "skill development"
- "learning gain*"
- "mastery"
- "competence"
- "proficiency"

**Measurement terms**:
- "assessment"
- "evaluation"
- "achievement test*"
- "performance measure*"
- "learning effect*"

**Affective/motivational terms**:
- "motivation"
- "engagement"
- "self-efficacy"
- "attitude*"

### 2.4 Block 3: Educational Context (Setting)

**General education terms**:
- "education*"
- "learning"
- "instruction"
- "teaching"
- "pedagogy"
- "curriculum"

**Level-specific terms**:
- "K-12"
- "primary education"
- "secondary education"
- "higher education"
- "university"
- "college"
- "undergraduate"
- "graduate"

**Workplace/professional terms**:
- "workplace training"
- "professional development"
- "workforce training"
- "corporate training"
- "continuing education"
- "professional education"
- "vocational training"
- "on-the-job training"

---

## 3. Database-Specific Search Strings

### 3.1 Web of Science Search String

```
TS=(("AI agent*" OR "intelligent agent*" OR "virtual agent*" OR "agentic AI"
     OR "intelligent tutoring system*" OR "ITS" OR "AI-powered agent*"
     OR "pedagogical agent*" OR "conversational agent*" OR "AI chatbot*"
     OR "multi-agent system*" OR "AI assistant*" OR "AI tutor*"
     OR "virtual tutor*" OR "embodied conversational agent*")
    AND
    ("learning outcome*" OR "academic achievement" OR "academic performance"
     OR "learning performance" OR "knowledge gain*" OR "skill acquisition"
     OR "skill development" OR "learning gain*" OR "test score*"
     OR "exam score*" OR "assessment" OR "performance measure*"
     OR "mastery" OR "competence" OR "engagement" OR "motivation"
     OR "self-efficacy")
    AND
    ("education*" OR "training" OR "learning" OR "instruction" OR "teaching"
     OR "workplace" OR "professional development" OR "K-12"
     OR "higher education" OR "university" OR "college"))
```

**Filters**:
- Publication years: 2018-2025
- Language: English
- Document types: Article, Proceedings Paper

### 3.2 Scopus Search String

```
TITLE-ABS-KEY(("AI agent*" OR "intelligent agent*" OR "virtual agent*"
               OR "agentic AI" OR "intelligent tutoring system*" OR "ITS"
               OR "AI-powered agent*" OR "pedagogical agent*"
               OR "conversational agent*" OR "AI chatbot*"
               OR "multi-agent system*" OR "AI assistant*" OR "AI tutor*"
               OR "virtual tutor*" OR "embodied conversational agent*")
              AND
              ("learning outcome*" OR "academic achievement"
               OR "academic performance" OR "learning performance"
               OR "knowledge gain*" OR "skill acquisition"
               OR "skill development" OR "learning gain*" OR "test score*"
               OR "exam score*" OR "assessment" OR "performance measure*"
               OR "mastery" OR "competence" OR "engagement" OR "motivation"
               OR "self-efficacy")
              AND
              ("education*" OR "training" OR "learning" OR "instruction"
               OR "teaching" OR "workplace" OR "professional development"
               OR "K-12" OR "higher education" OR "university" OR "college"))
```

**Filters**:
- Publication years: 2018-2025
- Language: English
- Document types: Article, Conference Paper

### 3.3 ERIC Search String

ERIC uses controlled vocabulary (descriptors) combined with free-text search:

```
(DE="Intelligent Tutoring Systems" OR DE="Computer Assisted Instruction"
 OR DE="Artificial Intelligence" OR DE="Educational Technology"
 OR TX="AI agent*" OR TX="intelligent agent*" OR TX="virtual agent*"
 OR TX="agentic AI" OR TX="pedagogical agent*" OR TX="conversational agent*"
 OR TX="AI chatbot*" OR TX="AI tutor*" OR TX="virtual tutor*")
AND
(DE="Academic Achievement" OR DE="Learning Outcomes" OR DE="Student Performance"
 OR TX="learning outcome*" OR TX="academic achievement" OR TX="test score*"
 OR TX="knowledge gain*" OR TX="skill acquisition")
AND
(DE="Education" OR DE="Instruction" OR DE="Teaching" OR DE="Workplace Learning"
 OR TX="education*" OR TX="learning" OR TX="training" OR TX="instruction")
```

**Filters**:
- Publication years: 2018-2025
- Language: English
- Publication types: Journal Articles, Reports - Research

### 3.4 PsycINFO Search String

PsycINFO uses thesaurus terms (DE) combined with free-text (TX):

```
(DE="Intelligent Tutoring Systems" OR DE="Computer Assisted Instruction"
 OR DE="Artificial Intelligence" OR DE="Human Computer Interaction"
 OR TX="AI agent*" OR TX="intelligent agent*" OR TX="virtual agent*"
 OR TX="agentic AI" OR TX="pedagogical agent*" OR TX="conversational agent*"
 OR TX="AI chatbot*" OR TX="AI tutor*")
AND
(DE="Academic Achievement" OR DE="Learning" OR DE="Skill Learning"
 OR TX="learning outcome*" OR TX="academic achievement" OR TX="test score*"
 OR TX="knowledge gain*" OR TX="skill acquisition" OR TX="performance")
AND
(DE="Education" OR DE="Teaching" OR DE="Educational Programs"
 OR DE="Workplace Learning"
 OR TX="education*" OR TX="learning" OR TX="training" OR TX="instruction")
```

**Filters**:
- Publication years: 2018-2025
- Language: English
- Publication types: Journal Article, Dissertation Abstract

### 3.5 IEEE Xplore Search String

IEEE uses simpler Boolean syntax:

```
("AI agent*" OR "intelligent agent*" OR "virtual agent*" OR "agentic AI"
 OR "intelligent tutoring system*" OR "pedagogical agent*"
 OR "conversational agent*" OR "AI chatbot*" OR "multi-agent system*"
 OR "AI tutor*" OR "educational AI")
AND
("learning outcome*" OR "academic achievement" OR "learning performance"
 OR "knowledge gain*" OR "skill acquisition" OR "test score*"
 OR "assessment" OR "learning effectiveness")
AND
("education*" OR "learning" OR "training" OR "instruction" OR "teaching"
 OR "e-learning" OR "online learning" OR "educational technology")
```

**Filters**:
- Publication years: 2018-2025
- Content types: Conference Publications, Journals

### 3.6 ACM Digital Library Search String

ACM uses structured query syntax:

```
[[All: "AI agent"] OR [All: "intelligent agent"] OR [All: "virtual agent"]
 OR [All: "agentic AI"] OR [All: "intelligent tutoring system"]
 OR [All: "pedagogical agent"] OR [All: "conversational agent"]
 OR [All: "AI chatbot"] OR [All: "AI tutor"] OR [All: "educational AI"]]
AND
[[All: "learning outcome"] OR [All: "academic achievement"]
 OR [All: "learning performance"] OR [All: "knowledge gain"]
 OR [All: "skill acquisition"] OR [All: "test score"] OR [All: "assessment"]]
AND
[[All: education] OR [All: learning] OR [All: training] OR [All: instruction]
 OR [All: teaching] OR [All: "e-learning"] OR [All: "educational technology"]]
```

**Filters**:
- Publication years: 2018-2025
- Content types: Research Article, Review Article, Conference Paper

---

## 4. Search Execution Protocol

### 4.1 Pre-Search Preparation

1. **Pilot search** (Week 3):
   - Execute simplified search in Web of Science and Scopus
   - Review first 100 results for relevance
   - Identify missed relevant papers
   - Adjust search terms if precision <50% or recall appears low

2. **Register search protocol** (Week 4):
   - Document finalized search strings in PROSPERO
   - Lock search strategy before full execution

### 4.2 Search Execution Order

| Database | Search Date | Estimated Time | Documentation |
|----------|-------------|----------------|---------------|
| Web of Science | Week 5, Day 1 | 2 hours | Screenshot results, export .ris |
| Scopus | Week 5, Day 2 | 2 hours | Screenshot results, export .ris |
| ERIC | Week 5, Day 3 | 1 hour | Screenshot results, export .ris |
| PsycINFO | Week 5, Day 4 | 1 hour | Screenshot results, export .ris |
| IEEE Xplore | Week 5, Day 5 | 1 hour | Screenshot results, export .csv |
| ACM Digital Library | Week 6, Day 1 | 1 hour | Screenshot results, export .bib |

### 4.3 Search Documentation

For each database search, document:
- Exact search string used (copy-paste from database)
- Date and time of search
- Number of results retrieved
- Any filters applied
- Screenshot of search interface with results count
- Export file name and format

**Template**:
```
Database: [Name]
Date: [YYYY-MM-DD HH:MM timezone]
Search String: [exact copy-paste]
Filters Applied: [list]
Results Retrieved: [N]
Export File: [filename.extension]
Notes: [any issues, adjustments]
```

### 4.4 Alert Setup

Set up search alerts in Web of Science and Scopus to capture newly published studies during the review process (Months 1-7).

---

## 5. Deduplication Strategy

### 5.1 Software

**Primary tool**: Covidence (or Rayyan if Covidence unavailable)
- Automatic deduplication based on DOI, title, author
- Manual review of potential duplicates

**Backup**: Zotero with duplicate detection

### 5.2 Deduplication Process

1. Import all database exports into Covidence
2. Run automatic deduplication (based on DOI, title match)
3. Review flagged potential duplicates (author + year + title similarity)
4. Document deduplication decisions
5. Export deduplicated set for screening

**Expected deduplication rate**: ~40-50% (based on database overlap patterns)

### 5.3 Database Overlap Expectations

| Database Pair | Expected Overlap |
|---------------|------------------|
| Web of Science ↔ Scopus | 60-70% |
| ERIC ↔ PsycINFO | 30-40% |
| IEEE ↔ ACM | 20-30% |
| WoS/Scopus ↔ ERIC/PsycINFO | 40-50% |
| All technical ↔ All education | 15-25% |

---

## 6. Grey Literature Search

### 6.1 Sources

| Source | Strategy | Expected Yield |
|--------|----------|----------------|
| **Google Scholar** | Citation tracking of included studies | 5-10 studies |
| **Conference proceedings** | Hand search ACM CHI, AIED, EDM, LAK, EC-TEL | 3-8 studies |
| **Dissertation databases** | ProQuest search with same terms | 2-5 dissertations |
| **Pre-print servers** | EdArXiv, SSRN, arXiv (cs.CY, cs.AI with education keywords) | 1-3 pre-prints |

### 6.2 Citation Tracking

**Backward citation tracking**:
- Review reference lists of all included studies
- Target: 100% coverage of included studies

**Forward citation tracking**:
- Use Web of Science "Cited by" feature for seed articles:
  - Dai et al. (2024)
  - Ma et al. (2014)
  - Yang (2025)
  - Yan (2025)
  - Kulik & Fletcher (2016)

**Estimated additional studies from citation tracking**: 10-20

### 6.3 Hand Search of Key Journals

**Journals** (2023-2025 issues):
- *Computers & Education*
- *International Journal of Artificial Intelligence in Education*
- *Educational Psychology Review*
- *Journal of Educational Psychology*
- *British Journal of Educational Technology*

**Rationale**: Recent studies may not yet be indexed; captures in-press articles

---

## 7. Inclusion/Exclusion Criteria (Applied During Search)

### 7.1 Initial Screening Filters

At the search stage, apply these broad filters:
- **Publication date**: 2018-2025
- **Language**: English
- **Publication type**: Peer-reviewed journal articles, peer-reviewed conference proceedings

### 7.2 Quick Exclusion Criteria (Title/Abstract Screening)

Exclude if clearly:
- No AI agent (e.g., human teacher only, static software)
- No learning outcome (e.g., usability study only, system development only)
- No educational context (e.g., pure lab study, medical diagnosis AI)
- Not empirical (e.g., opinion piece, conceptual framework only)
- Wrong study design (e.g., purely qualitative interview study)

**Detailed inclusion/exclusion criteria applied in Phase 2-3 (see `02_study_selection/inclusion_exclusion_criteria.md`)**

---

## 8. Search Strategy Validation

### 8.1 Sensitivity Checks

**Known inclusion test**: Identify 5-10 highly relevant studies published 2018-2025 (from pilot search or known sources). Verify all are captured by search strategy.

**Test set**:
1. Dai et al. (2024) - AI virtual agents meta-analysis
2. [Additional studies identified during pilot]

If any are missed, revise search terms.

### 8.2 Precision Estimation

From pilot search, estimate precision:
- **Precision** = (Relevant results in first 100) / 100
- **Target**: >30% precision (acceptable for systematic reviews)

If precision <30%, consider adding restrictive terms or adjusting concept blocks.

---

## 9. Search Timeline

| Week | Activity | Deliverable |
|------|----------|-------------|
| Week 3 | Pilot search (WoS, Scopus) | Pilot search report |
| Week 4 | Finalize search strings, register protocol | Registered PROSPERO protocol |
| Week 5-6 | Execute systematic search across all 6 databases | 6 database export files |
| Week 7 | Deduplication in Covidence | Deduplicated reference set |
| Week 8 | Citation tracking, grey literature search | Supplementary reference set |

---

## 10. Search Strategy Reporting (PRISMA 2020)

The following elements will be reported in the final manuscript:

| PRISMA Item | Description | Location |
|-------------|-------------|----------|
| #7: Search strategy | Full search strategies for all databases | Methods section + Supplementary Appendix |
| #8: Study selection | Date ranges, filters, grey literature strategy | Methods section |
| Database list | All 6 databases with coverage rationale | Methods section |
| Search dates | Exact dates each database was searched | Methods section |
| Search strings | Full Boolean strings for each database | Supplementary Appendix |
| Deduplication | Method and counts | PRISMA flow diagram |

---

## 11. Search String Refinement Log

**Version 1.0** (Initial):
- Date: [To be completed during pilot]
- Changes: Initial draft based on Dai et al. (2024) and Ma et al. (2014)

**Version 1.1** (Post-pilot):
- Date: [To be completed after pilot]
- Changes: [Adjustments based on pilot search results]

**Version 2.0** (Final):
- Date: [To be locked before systematic search]
- Changes: [Final refinements]

All refinements will be documented with rationale.

---

## 12. Contact Information for Database Access Issues

| Database | Access Method | Contact for Issues |
|----------|---------------|-------------------|
| Web of Science | Institutional subscription | University library |
| Scopus | Institutional subscription | University library |
| ERIC | Free (IES) | No login required |
| PsycINFO | Institutional subscription via EBSCOhost | University library |
| IEEE Xplore | Institutional subscription | University library |
| ACM Digital Library | Institutional subscription | University library |

---

*This search strategy follows PRISMA 2020 guidelines and will be registered on PROSPERO prior to search execution. Any deviations from this protocol will be documented with justification.*
