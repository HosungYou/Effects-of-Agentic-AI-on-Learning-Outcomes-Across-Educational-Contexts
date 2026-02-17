# Appendix A: Systematic Search Strategy

## Complete Database Search Strings and Execution Log

**Study**: Effects of Agentic AI on Learning Outcomes Across Educational Contexts: A Meta-Analysis with Implications for Human-AI Learning Orchestration

**Authors**: Hosung You & Dr. Yang

**Reporting standard**: PRISMA 2020 (Page et al., 2021)

---

## A1. Overview

This appendix provides the complete, verbatim search strings used in each database, execution dates, and result counts. This information enables replication of the systematic search and satisfies PRISMA 2020 Item #8 (Search Strategy).

---

## A2. Database Search Strings

### A2.1 Web of Science (Core Collection)

**Interface**: Web of Science Core Collection
**Search Field**: Topic (TS) — searches title, abstract, author keywords, and Keywords Plus
**Execution Date**: [DATE TBD]
**Results Retrieved**: [N TBD]

```
TS=(("AI agent*" OR "intelligent agent*" OR "virtual agent*" OR "agentic AI"
     OR "intelligent tutoring system*" OR "AI-powered agent*"
     OR "pedagogical agent*" OR "conversational agent*" OR "AI chatbot*"
     OR "multi-agent system*" OR "AI assistant*" OR "AI tutor*"
     OR "virtual tutor*" OR "embodied conversational agent*"
     OR "autonomous agent*" OR "dialogue system*" OR "chatbot*" OR "AI coach*")
    AND
    ("learning outcome*" OR "academic achievement" OR "academic performance"
     OR "learning performance" OR "knowledge gain*" OR "skill acquisition"
     OR "skill development" OR "learning gain*" OR "test score*"
     OR "exam score*" OR "assessment" OR "performance measure*"
     OR "mastery" OR "competence" OR "engagement" OR "motivation"
     OR "self-efficacy" OR "learning effect*" OR "educational outcome*")
    AND
    ("education*" OR "training" OR "learning" OR "instruction" OR "teaching"
     OR "workplace" OR "professional development" OR "K-12" OR "higher education"
     OR "university" OR "college" OR "online learning" OR "e-learning"
     OR "blended learning" OR "workforce training" OR "continuing education"))
```

**Filters applied**:
- Publication Years: 2018-2025
- Language: English
- Document Types: Article; Proceedings Paper; Review Article

**Actual results count**: [To be recorded after search execution]
**Export filename**: `wos_search_[DATE].ris`
**Export format**: RIS (Reference Manager format)

**Search screenshot**: [Attach or reference screenshot file]

---

### A2.2 Scopus

**Interface**: Scopus (Elsevier)
**Search Field**: TITLE-ABS-KEY — searches title, abstract, and author keywords
**Execution Date**: [DATE TBD]
**Results Retrieved**: [N TBD]

```
TITLE-ABS-KEY(("AI agent*" OR "intelligent agent*" OR "virtual agent*"
               OR "agentic AI" OR "intelligent tutoring system*"
               OR "AI-powered agent*" OR "pedagogical agent*"
               OR "conversational agent*" OR "AI chatbot*"
               OR "multi-agent system*" OR "AI assistant*" OR "AI tutor*"
               OR "virtual tutor*" OR "embodied conversational agent*"
               OR "autonomous agent*" OR "dialogue system*" OR "chatbot*"
               OR "AI coach*")
              AND
              ("learning outcome*" OR "academic achievement"
               OR "academic performance" OR "learning performance"
               OR "knowledge gain*" OR "skill acquisition"
               OR "skill development" OR "learning gain*" OR "test score*"
               OR "exam score*" OR "assessment" OR "performance measure*"
               OR "mastery" OR "competence" OR "engagement" OR "motivation"
               OR "self-efficacy" OR "learning effect*" OR "educational outcome*")
              AND
              ("education*" OR "training" OR "learning" OR "instruction"
               OR "teaching" OR "workplace" OR "professional development"
               OR "K-12" OR "higher education" OR "university" OR "college"
               OR "online learning" OR "e-learning" OR "blended learning"
               OR "workforce training" OR "continuing education"))
AND PUBYEAR > 2017 AND PUBYEAR < 2026
AND LANGUAGE(english)
AND DOCTYPE(ar OR cp OR re)
```

**Filters applied**:
- Publication Years: 2018-2025 (>2017 AND <2026)
- Language: English
- Document Types: ar (Article), cp (Conference Paper), re (Review)

**Actual results count**: [To be recorded]
**Export filename**: `scopus_search_[DATE].ris`
**Export format**: RIS

---

### A2.3 ERIC (Education Resources Information Center)

**Interface**: ERIC (https://eric.ed.gov/)
**Search Field**: Combination of descriptors (DE) and free-text (any field)
**Execution Date**: [DATE TBD]
**Results Retrieved**: [N TBD]

```
(DE:"Intelligent Tutoring Systems" OR DE:"Computer Assisted Instruction"
 OR DE:"Artificial Intelligence" OR DE:"Educational Technology"
 OR DE:"Intelligent Agents" OR DE:"Computer Mediated Communication"
 OR "AI agent*" OR "intelligent agent*" OR "virtual agent*"
 OR "agentic AI" OR "pedagogical agent*" OR "conversational agent*"
 OR "AI chatbot*" OR "AI tutor*" OR "virtual tutor*" OR "AI assistant*"
 OR "multi-agent system*")
AND
(DE:"Academic Achievement" OR DE:"Learning Outcomes" OR DE:"Student Performance"
 OR DE:"Educational Objectives" OR DE:"Achievement Gains"
 OR "learning outcome*" OR "academic achievement" OR "test score*"
 OR "knowledge gain*" OR "skill acquisition" OR "learning performance"
 OR "engagement" OR "motivation" OR "self-efficacy")
AND
(DE:"Education" OR DE:"Instruction" OR DE:"Teaching Methods"
 OR DE:"Electronic Learning" OR DE:"Distance Education"
 OR DE:"Higher Education" OR DE:"Elementary Education"
 OR DE:"Secondary Education" OR DE:"Workplace Learning"
 OR "education*" OR "learning" OR "training" OR "instruction")
```

**Filters applied**:
- Publication Date: 2018-2025
- Language: English
- Source Type: Journal Articles; Reports-Research

**Actual results count**: [To be recorded]
**Export filename**: `eric_search_[DATE].ris`

**ERIC Thesaurus note**: ERIC uses controlled vocabulary. Key descriptors mapped:
- "Intelligent Tutoring Systems" → Primary AI intervention descriptor
- "Computer Assisted Instruction" → Broader AI tool descriptor
- "Academic Achievement" → Primary outcome descriptor

---

### A2.4 PsycINFO (via APA PsycNet or EBSCOhost)

**Interface**: APA PsycNet or EBSCOhost PsycINFO
**Search Field**: Combination of thesaurus terms (DE) and free-text (TX or AB/TI)
**Execution Date**: [DATE TBD]
**Results Retrieved**: [N TBD]

**Via EBSCOhost**:
```
(DE "Intelligent Tutoring Systems" OR DE "Computer Assisted Learning"
 OR DE "Artificial Intelligence" OR DE "Human Computer Interaction"
 OR DE "Tutoring" OR DE "Educational Software"
 OR TX "AI agent*" OR TX "intelligent agent*" OR TX "virtual agent*"
 OR TX "agentic AI" OR TX "pedagogical agent*" OR TX "conversational agent*"
 OR TX "AI chatbot*" OR TX "AI tutor*" OR TX "AI assistant*"
 OR TX "multi-agent system*")
AND
(DE "Academic Achievement" OR DE "Learning" OR DE "Skill Learning"
 OR DE "Knowledge Level" OR DE "Academic Performance"
 OR TX "learning outcome*" OR TX "academic achievement" OR TX "test score*"
 OR TX "knowledge gain*" OR TX "skill acquisition" OR TX "learning gain*"
 OR TX "engagement" OR TX "motivation" OR TX "self-efficacy" OR TX "performance")
AND
(DE "Education" OR DE "Teaching" OR DE "Educational Programs"
 OR DE "Workplace Learning" OR DE "Training" OR DE "Computer Assisted Instruction"
 OR TX "education*" OR TX "learning" OR TX "training" OR TX "instruction"
 OR TX "workplace" OR TX "professional development" OR TX "higher education")
```

**Filters applied**:
- Publication Year: 2018-2025
- Language: English
- Document Type: Journal Article; Dissertation Abstract

**Actual results count**: [To be recorded]
**Export filename**: `psycinfo_search_[DATE].ris`

---

### A2.5 IEEE Xplore

**Interface**: IEEE Xplore Digital Library (https://ieeexplore.ieee.org/)
**Search Field**: Full Text & Metadata
**Execution Date**: [DATE TBD]
**Results Retrieved**: [N TBD]

```
("AI agent" OR "intelligent agent" OR "virtual agent" OR "agentic AI"
 OR "intelligent tutoring system" OR "pedagogical agent"
 OR "conversational agent" OR "AI chatbot" OR "multi-agent system"
 OR "AI tutor" OR "educational AI" OR "AI-powered tutor"
 OR "dialogue system" OR "virtual tutor" OR "AI learning system")
AND
("learning outcome" OR "academic achievement" OR "learning performance"
 OR "knowledge gain" OR "skill acquisition" OR "test score"
 OR "assessment" OR "learning effectiveness" OR "educational outcome"
 OR "learning gain" OR "student performance")
AND
("education" OR "learning" OR "training" OR "instruction" OR "teaching"
 OR "e-learning" OR "online learning" OR "educational technology"
 OR "computer-supported learning" OR "intelligent learning environment")
```

**Note on wildcards**: IEEE Xplore supports limited wildcard usage; exact phrases preferred.

**Filters applied**:
- Year Range: 2018-2025
- Content Types: Conference Publications, Journals, Magazines

**Actual results count**: [To be recorded]
**Export filename**: `ieee_search_[DATE].csv`

---

### A2.6 ACM Digital Library

**Interface**: ACM Digital Library (https://dl.acm.org/)
**Search Field**: The ACM Guide to Computing Literature
**Execution Date**: [DATE TBD]
**Results Retrieved**: [N TBD]

```
[[All: "AI agent"] OR [All: "intelligent agent"] OR [All: "virtual agent"]
 OR [All: "agentic AI"] OR [All: "intelligent tutoring system"]
 OR [All: "pedagogical agent"] OR [All: "conversational agent"]
 OR [All: "AI chatbot"] OR [All: "AI tutor"] OR [All: "educational AI"]
 OR [All: "multi-agent system"] OR [All: "dialogue system"]
 OR [All: "virtual tutor"] OR [All: "AI assistant"]]
AND
[[All: "learning outcome"] OR [All: "academic achievement"]
 OR [All: "learning performance"] OR [All: "knowledge gain"]
 OR [All: "skill acquisition"] OR [All: "test score"] OR [All: "assessment"]
 OR [All: "learning gain"] OR [All: "educational outcome"]]
AND
[[All: education] OR [All: learning] OR [All: training] OR [All: instruction]
 OR [All: teaching] OR [All: "e-learning"] OR [All: "online learning"]
 OR [All: "educational technology"] OR [All: "computer-supported learning"]]
```

**Filters applied**:
- Publication Year: 2018-2025
- Content Type: Research Article, Review Article, Conference Paper

**Actual results count**: [To be recorded]
**Export filename**: `acm_search_[DATE].bib`

---

## A3. Search Results Summary

| Database | Date Searched | Raw Results | After Language Filter | Notes |
|----------|:---:|:---:|:---:|-------|
| Web of Science | [TBD] | [TBD] | [TBD] | |
| Scopus | [TBD] | [TBD] | [TBD] | |
| ERIC | [TBD] | [TBD] | [TBD] | |
| PsycINFO | [TBD] | [TBD] | [TBD] | |
| IEEE Xplore | [TBD] | [TBD] | [TBD] | |
| ACM Digital Library | [TBD] | [TBD] | [TBD] | |
| **Total** | | **[TBD]** | **[TBD]** | |

---

## A4. Deduplication Results

| Stage | N Records |
|-------|:---------:|
| Total retrieved across all databases | [TBD] |
| Removed as duplicates (automatic) | [TBD] |
| Removed as duplicates (manual review) | [TBD] |
| **Records for title/abstract screening** | **[TBD]** |

**Deduplication method**: Covidence automatic detection (DOI match, title + author match) followed by manual review of flagged probable duplicates.

---

## A5. Supplementary Source Results

| Source | Strategy | Results |
|--------|----------|:-------:|
| Google Scholar — citation tracking | Backward/forward citations of 5 seed articles | [TBD] |
| Hand search — Computers & Education | Issues 2023-2025 | [TBD] |
| Hand search — IJAIED | Issues 2023-2025 | [TBD] |
| Hand search — Educational Psychology Review | Issues 2023-2025 | [TBD] |
| ProQuest Dissertations | Same search terms | [TBD] |
| **Total supplementary** | | **[TBD]** |

---

## A6. Search Strategy Refinement History

| Version | Date | Changes Made | Rationale |
|---------|------|-------------|-----------|
| 1.0 | [TBD] | Initial draft | Based on research proposal and Dai et al. (2024) |
| 1.1 | [TBD] | Pilot search adjustments | [To be completed after pilot] |
| 2.0 | [TBD] | Final locked version | [To be completed before full search] |

---

*This appendix will be submitted as Supplementary Material with the manuscript. All search strings are provided verbatim to enable replication. Searches were conducted by Hosung You.*

*Reference: Page, M. J., et al. (2021). The PRISMA 2020 statement. BMJ, 372, n71.*
