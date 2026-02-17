# Search Strategy & Inclusion/Exclusion Criteria

## 1. Protocol

- **Guideline**: PRISMA 2020 (Page et al., 2021)
- **Pre-registration**: PROSPERO or OSF Pre-registration
- **Effect Size Metric**: Hedges' g (standardized mean difference)

---

## 2. Databases

| Database | Coverage | Rationale |
|----------|----------|-----------|
| **Web of Science** | Multidisciplinary, SSCI/SCI indexed | Gold standard for systematic reviews |
| **Scopus** | Broader coverage than WoS | Captures conference proceedings, broader journal set |
| **ERIC** | Education-specific | Core education research database |
| **PsycINFO** | Psychology & behavioral sciences | Learning psychology, educational psychology |
| **IEEE Xplore** | Engineering & computer science | AI/ML technical implementations in education |
| **ACM Digital Library** | Computing & information technology | Computer-supported learning, HCI in education |

### Supplementary Sources
- Backward citation tracking from included studies
- Forward citation tracking of key seed articles (Dai et al., 2024; Ma et al., 2014; Yang, 2025; Yan, 2025)
- Hand search of key journals: *Computers & Education*, *Educational Psychology Review*, *International Journal of AI in Education*

---

## 3. Search Terms

### Block 1: AI Agent (Intervention)

```
"AI agent*" OR "intelligent agent*" OR "virtual agent*" OR "agentic AI"
OR "intelligent tutoring system*" OR "AI-powered agent*"
OR "pedagogical agent*" OR "conversational agent*"
OR "AI chatbot" OR "multi-agent system*" OR "AI assistant*"
```

### Block 2: Learning Outcome (Dependent Variable)

```
"learning outcome*" OR "academic achievement" OR "performance"
OR "knowledge gain" OR "skill acquisition" OR "learning gain*"
OR "test score*" OR "assessment"
```

### Block 3: Educational Context (Setting)

```
"education*" OR "training" OR "learning" OR "instruction"
OR "workplace" OR "professional development" OR "workforce"
```

### Combined Search String

```
(Block 1) AND (Block 2) AND (Block 3)
```

### Database-Specific Adaptations

Each database has unique syntax requirements. Below are notes for adaptation:

| Database | Notes |
|----------|-------|
| **Web of Science** | Use TS= (Topic Search); adjust wildcards (*) |
| **Scopus** | Use TITLE-ABS-KEY; adjust Boolean syntax |
| **ERIC** | Use descriptors (DE=) and free-text (TX=); map to ERIC thesaurus terms |
| **PsycINFO** | Map to PsycINFO thesaurus; use DE= for descriptors |
| **IEEE Xplore** | Use "Full Text & Metadata" search; may need simplified query |
| **ACM Digital Library** | Use ACM Guide to Computing Literature; adjust syntax |

---

## 4. Publication Period

**2018 to 2025**

### Rationale
- 2018 marks the beginning of the transformer era (Vaswani et al., 2017 published; practical implementations began 2018+)
- Captures the shift from rule-based to AI/ML-powered agent systems
- Includes the GPT era (2020+) and Agentic AI emergence (2023+)
- Excludes older ITS studies that are pre-agentic (covered by Ma et al., 2014)

---

## 5. Inclusion Criteria

| Criterion | Description |
|-----------|-------------|
| **IC1: Study Design** | Experimental, quasi-experimental, or pre-post comparison designs that allow quantitative effect size calculation |
| **IC2: Intervention** | AI agent system with autonomous action capabilities (e.g., adaptive responses, recommendation generation, automated feedback, proactive interventions) |
| **IC3: Comparison** | Includes a comparison condition: (a) no AI agent, (b) non-agentic AI, or (c) different levels of AI agency |
| **IC4: Outcome** | Reports at least one learning outcome (cognitive, skill-based, affective, or performance) |
| **IC5: Context** | Set in an educational context: K-12, higher education, workplace training, professional education, or continuing education |
| **IC6: Data** | Reports sufficient quantitative data to compute or estimate Hedges' g (means + SDs, F/t statistics, or other convertible statistics) |
| **IC7: Language** | Published in English |
| **IC8: Publication Type** | Peer-reviewed journal articles, conference proceedings with full-text peer review |

---

## 6. Exclusion Criteria

| Criterion | Description |
|-----------|-------------|
| **EC1: Study Design** | Purely qualitative studies, case studies, surveys without intervention, design-based research without quantitative outcomes |
| **EC2: Intervention** | Simple search tools, static content delivery systems, calculator-like tools without adaptive/autonomous behavior |
| **EC3: Comparison** | No comparison condition (descriptive use of AI only) |
| **EC4: Outcome** | Reports only satisfaction/usability metrics without learning outcomes; reports only system performance metrics (e.g., AI accuracy) |
| **EC5: Context** | Pure laboratory experiments without learning context; AI agent used for non-educational purposes |
| **EC6: Data** | Insufficient statistical data to compute effect size, even after contacting authors |
| **EC7: Language** | Non-English publications |
| **EC8: Publication Type** | Editorials, commentaries, book reviews, abstracts-only, dissertations without peer review |

---

## 7. Operationalizing "Agentic AI"

A system qualifies as "Agentic AI" if it demonstrates **at least one** of the following autonomous capabilities:

| Capability | Description | Examples |
|-----------|-------------|---------|
| **Adaptive Response** | Adjusts behavior based on learner input/performance | ITS that modifies difficulty; chatbot that adjusts explanation level |
| **Proactive Intervention** | Initiates interaction without explicit learner request | Agent that detects confusion and offers help; system that suggests next steps |
| **Automated Assessment** | Independently evaluates learner work and provides feedback | Automated essay scoring with feedback; code review agents |
| **Recommendation Generation** | Suggests learning paths, resources, or strategies | Personalized learning path agents; resource recommendation systems |
| **Dialogue Management** | Maintains multi-turn conversation with contextual awareness | Conversational tutoring systems; Socratic dialogue agents |
| **Multi-Agent Coordination** | Multiple AI agents collaborating on learning support | Team of specialized agents (tutor + assessor + coach) |

### NOT Agentic (Excluded)
- Static quiz generators without adaptation
- Simple keyword-based FAQ systems
- Pre-programmed linear tutorials
- Search engines without recommendation
- Generic chatbots without domain/pedagogical knowledge

---

## 8. Screening Process

### Stage 1: Title and Abstract Screening
- Two independent reviewers screen all records
- Use Covidence (or equivalent) for systematic screening
- Resolve conflicts through discussion
- Calculate inter-rater agreement (percent agreement + Cohen's kappa)
- Target: kappa >= 0.80

### Stage 2: Full-Text Screening
- Two independent reviewers assess full texts
- Apply all inclusion/exclusion criteria
- Document exclusion reasons for each excluded study
- Resolve conflicts through discussion (third reviewer if needed)
- Calculate inter-rater agreement

### Stage 3: Data Extraction Verification
- Cross-check all extracted effect size data
- Contact original authors for missing data (allow 2-week response window)
- Document all author contacts and responses

---

## 9. Expected Results

### Estimated Study Pool

| Source | Estimated Hits |
|--------|---------------|
| Web of Science | 2,000-3,000 |
| Scopus | 3,000-5,000 |
| ERIC | 500-1,000 |
| PsycINFO | 500-1,000 |
| IEEE Xplore | 1,000-2,000 |
| ACM Digital Library | 500-1,000 |
| **Total before deduplication** | **7,500-13,000** |
| **After deduplication** | **4,000-8,000** |
| **After title/abstract screening** | **200-400** |
| **After full-text screening** | **40-80 studies** |
| **Effect sizes extracted** | **100-200** |

### Rationale for Expected k
- Dai et al. (2024): k=22 for AI agents in simulations only
- Ma et al. (2014): k=107 effect sizes for ITS only
- Our broader scope (all educational contexts + all agentic AI types) justifies higher expected k
- The 2018-2025 window captures rapid growth in AI education research

---

## 10. Search Documentation

All search activities will be documented following PRISMA 2020 requirements:

- Exact search strings used per database
- Date of each search
- Number of results per database
- Deduplication method and count
- Screening decisions with reasons
- PRISMA flow diagram

---

*Note: Search strings will be adapted and pilot-tested before the formal search. Refinements based on pilot search results will be documented.*
