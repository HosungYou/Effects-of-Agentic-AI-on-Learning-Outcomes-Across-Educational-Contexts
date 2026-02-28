# Paper Outline — Trust Calibration as the Missing Link in Educational AI Design

**Target**: International Journal of Educational Technology in Higher Education (IJETHE)
**Word count**: 8,000-10,000 words
**Format**: APA 7th edition

---

## Paper Structure

### 1. Introduction (800-1,000 words)

**Purpose**: Frame the trust problem in educational AI and motivate the paper.

**Key points**:
- Educational AI systems (especially generative AI and agentic AI) are being deployed rapidly
- The fundamental design question: How much autonomy should AI have vs. how much should human oversight control?
- Current approaches are insufficient: Bastani et al. (2025, PNAS) showed that unrestricted access to ChatGPT for math problem-solving led to overtrust and *harmed* learning
- Trust is the missing variable: whether an AI system helps or harms depends on whether learners calibrate their trust appropriately
- Purpose statement: This paper (a) maps how trust in AI is currently conceptualized in educational AI research through a scoping review, (b) identifies a critical gap (trust calibration as a system design target), and (c) proposes a two-level framework connecting individual trust calibration to oversight design

**Research questions** (state explicitly):
1. How is trust in AI conceptualized and measured in educational AI research?
2. What theoretical frameworks guide trust research in educational AI?
3. To what extent does existing research address trust calibration and human oversight design?
4. What does a two-level framework connecting learner trust to oversight design look like?

**Writing notes**:
- Open with a compelling example (Bastani et al. overtrust finding)
- Don't over-cite in introduction; save detailed literature for Section 2
- End with clear purpose statement and RQ list

---

### 2. Conceptual Foundation (1,500-2,000 words)

**Purpose**: Establish the theoretical basis before the scoping review.

**2.1 Trust in Automation: From Engineering to Education**
- Lee & See (2004): Trust as attitude toward reliance on automation; trust calibration = alignment between trust and automation capability
- Three trust failures: misuse (overtrust), disuse (distrust), abuse (design exploitation)
- de Visser et al. (2020): Longitudinal trust calibration; trust repair mechanisms; trust as dynamic, not static
- Application to educational AI: education has unique features (learning is the goal, not task completion)

**2.2 Trust Calibration: The Core Concept**
- Definition: Trust calibration = the degree to which a learner's trust in an AI system matches the system's actual capability and reliability
- Overtrust --> misuse: uncritical acceptance of AI outputs (Bastani et al., 2025)
- Distrust --> disuse: rejection of AI assistance even when beneficial
- Calibrated trust --> appropriate use: selective, critical engagement
- Why calibration matters more than trust level

**2.3 Wang et al. (2025): The Most Complete Empirical Model**
- S-O-R framework: Stimulus (AI characteristics) --> Organism (trust, reliance, resistance) --> Response (behavioral intention --> actual use)
- Key contribution: Distinguishes trust from reliance and resistance; models trust as mediating between AI characteristics and use behavior
- Limitation: Stops at individual use behavior; does not address system design or oversight

**2.4 Toward a Two-Level Framework**
- The gap: Wang et al. gives us Level 1 (individual trust --> use), but who ensures trust is calibrated?
- Two mechanisms for trust calibration:
  - Internal: Self-directed learning (SDL), metacognition, critical thinking (learner-driven)
  - External: Teacher interventions, system checkpoints, AI transparency features (system/instructor-driven)
- Preview of the framework (full detail in Section 5)

**Writing notes**:
- This section builds the theoretical scaffolding
- Move from general (automation trust) to specific (educational AI trust)
- Set up the gap that the scoping review will confirm

---

### 3. Scoping Review Method (800-1,000 words)

**Purpose**: Describe the systematic scoping review methodology.

**3.1 Protocol and Registration**
- JBI methodology for scoping reviews (Peters et al., 2020)
- PRISMA-ScR reporting guideline (Tricco et al., 2018)
- Pre-registration: [OSF link if applicable]

**3.2 Eligibility Criteria (PCC)**
- Population: Learners/educators in educational settings
- Concept: Trust in AI (trust, reliance, resistance, overtrust, distrust, calibration)
- Context: AI-based educational tools (ITS, chatbot, generative AI, AI agents)
- Additional: English, 2015-2026, peer-reviewed + full conference papers

**3.3 Information Sources and Search Strategy**
- 6 databases: Web of Science, Scopus, ERIC, PsycINFO, Semantic Scholar, OpenAlex
- 2-block search structure (trust concept AND educational AI context)
- Supplementary: Citation tracking, hand search of key journals
- Search dates: [FILL]
- Full search strings in Appendix B

**3.4 Study Selection**
- AI-assisted title/abstract screening with human verification
- Full-text assessment by lead author
- Selection process reported in PRISMA-ScR flow diagram (Figure 1)

**3.5 Data Charting**
- Charting form aligned with research questions (see Appendix C)
- Key variables: trust construct, definition, framework, measurement, role in model, calibration, oversight
- AI-assisted extraction with human verification for all entries

**3.6 Synthesis**
- Descriptive numerical summary of study characteristics
- Thematic analysis of trust conceptualizations
- Gap analysis mapping findings to two-level framework

**Writing notes**:
- Keep methods concise; details in appendices
- Emphasize transparency of AI-assisted screening
- Follow PRISMA-ScR checklist items

---

### 4. Results (1,500-2,000 words)

**Purpose**: Report scoping review findings.

**4.1 Search Results and Study Selection**
- PRISMA-ScR flow diagram (Figure 1)
- Records identified, deduplicated, screened, included

**4.2 Study Characteristics**
- Table 1: Summary of included studies
- Distribution by: year, country, study type, educational level, AI system type, sample size range

**4.3 Trust Conceptualizations Across Studies (RQ1)**
- How studies define trust (or don't)
- Trust construct labels used: trust, reliance, resistance, etc.
- Explicit vs. implicit definitions
- Table 2: Trust definitions across studies

**4.4 Theoretical Frameworks (RQ2)**
- Distribution of frameworks used
- Clusters: (a) Trust as attitude (Mayer et al.), (b) Trust as behavior (Lee & See), (c) Trust as acceptance factor (TAM/UTAUT), (d) Trust calibration (de Visser), (e) Trust as S-O-R mediator (Wang et al.)
- Table 3: Theoretical frameworks

**4.5 Trust Measurement Approaches**
- Survey-based vs. behavioral vs. qualitative
- Scales used and their origins
- Reliability/validity reporting

**4.6 Trust Calibration and Oversight Coverage (RQ3)**
- **Expected finding**: Very few studies (<5) explicitly discuss calibration
- **Expected finding**: Almost none connect trust to oversight design
- This gap is the paper's core contribution
- Table 4: Studies addressing calibration and/or oversight

**Writing notes**:
- Present findings neutrally
- Use tables extensively to stay within word count
- The gap finding (4.6) should be clearly quantified
- Save interpretation for Section 5

---

### 5. Critical Synthesis: The Two-Level Trust-Calibrated Oversight Framework (1,500-2,000 words)

**Purpose**: Present the paper's main contribution -- the framework.

**THIS IS THE MOST IMPORTANT SECTION. WRITE FIRST.**

**5.1 Synthesizing the Evidence: From Fragmented Trust to Integrated Framework**
- Summary of scoping review gap: trust is studied predominantly at individual level (Level 1) with theoretical fragmentation
- Wang et al. (2025) provides the most complete empirical model but stops at individual use behavior
- Trust calibration as a system design target (Level 2) is absent from educational AI literature despite being established in automation research
- This is the missing link

**5.2 Level 1 (Micro): Learner Trust Dynamics**
```
Learner --> [Trust/Distrust] --> [Reliance/Resistance] --> [AI Use Behavior]
```
- Based on Wang et al. (2025) S-O-R model
- Trust antecedents: AI system quality, transparency, prior experience, digital literacy
- Trust outcomes: reliance (accepting AI output), resistance (rejecting/modifying AI output)
- Behavioral outcomes: continuation, deepening use, appropriate use, avoidance
- **Internal calibration mechanism**: SDL, metacognition, critical thinking
  - When learners self-regulate, they can calibrate trust internally
  - Evidence from scoping review [cite specific studies]

**5.3 Level 2 (Macro): System-Mediated Trust Calibration**
```
Designer --> [Checkpoint Design] --> [Trust Calibration Intervention] --> Modifies Level 1
```
- External calibration mechanisms:
  - Teacher checkpoints (guided reflection, trust assessment)
  - System checkpoints (forced pauses, confidence prompts, AI uncertainty display)
  - Transparency features (explainability, confidence scores)
  - Friction design (deliberate slowdowns to prevent automatic acceptance)
- This level is what's missing from the literature
- Evidence from adjacent fields: automation trust repair (de Visser et al., 2020), friction design (Meier et al., 2019)

**5.4 Connecting the Levels: Trust Calibration as the Design Variable**
- Figure 2: The Two-Level Trust-Calibrated Oversight Framework
- Key insight: The optimal oversight level is not fixed -- it depends on learner trust calibration state
  - High trust calibration --> less oversight needed (more autonomous AI)
  - Low trust calibration (overtrust OR distrust) --> more oversight needed (more checkpoints)
- This is a *dynamic* model: oversight should adapt as trust calibrates over time
- Connection to Bastani et al. (2025): The harm occurred because there was NO Level 2 (no oversight, no calibration mechanism)

**5.5 Mapping Scoping Review Evidence to the Framework**
- Table 5: How each included study maps (or fails to map) to Level 1 and Level 2
- Expected: Most studies map to Level 1 only; Level 2 is the gap
- This mapping justifies the framework's contribution

**Writing notes**:
- Use clear, visual framework description
- Anchor every claim to scoping review evidence OR adjacent field evidence
- This section IS the paper's contribution
- Figure 2 should be clear and publishable

---

### 6. Implications for Practice and Design (800-1,000 words)

**6.1 For AI Agent Designers**
- Design trust-calibrated checkpoints into educational AI systems
- Display AI confidence/uncertainty to support calibration
- Implement progressive autonomy: start with more oversight, reduce as trust calibrates
- Avoid the "Bastani trap": unrestricted access without calibration mechanisms

**6.2 For Educators**
- Recognize trust calibration as a learning objective, not just a side effect
- Monitor learner trust states (overtrust/distrust indicators)
- Teach critical AI evaluation skills (internal calibration)
- Design trust calibration activities into curriculum

**6.3 For Researchers**
- Measure trust calibration, not just trust level
- Study trust longitudinally (calibration is a process)
- Investigate Level 2 mechanisms (what checkpoints work?)
- Future meta-analysis needed (groundwork laid by this paper)
- Specific research agenda:
  1. What checkpoint designs best support trust calibration?
  2. How does trust calibration develop over time?
  3. What learner characteristics moderate trust calibration?
  4. How should AI transparency features be designed for educational contexts?

---

### 7. Limitations and Conclusion (500-700 words)

**Limitations**:
- Scoping review (not systematic): breadth over depth, no formal quality appraisal
- Single reviewer with AI assistance (acknowledged and mitigated)
- English-only (may miss non-English trust literature, especially East Asian)
- Framework is conceptual (needs empirical testing)
- Rapid growth of field means some very recent studies may be missed

**Conclusion**:
- Restate the core argument: trust calibration is the missing link
- The field has Level 1 knowledge (individual trust processes) but lacks Level 2 (system-level oversight design)
- The two-level framework provides a roadmap for both design and research
- Closing: As educational AI becomes more autonomous, the question is not "do learners trust it?" but "is their trust calibrated?" -- and "who or what calibrates it?"

---

## Figures

1. **Figure 1**: PRISMA-ScR flow diagram (generated from `scripts/scr_generate_prisma.py`)
2. **Figure 2**: Two-Level Trust-Calibrated Oversight Framework (create in Figma or draw.io)
3. **Figure 3** (optional): Trust conceptualization theme map from thematic analysis

## Tables

1. **Table 1**: Summary characteristics of included studies
2. **Table 2**: Trust definitions across included studies
3. **Table 3**: Theoretical frameworks used in included studies
4. **Table 4**: Trust calibration and oversight coverage
5. **Table 5**: Framework mapping (Level 1 vs Level 2 evidence)

## Appendices

- **Appendix A**: PRISMA-ScR 22-item checklist
- **Appendix B**: Complete search strings for all databases
- **Appendix C**: Data charting form
- **Appendix D**: Characteristics of all included studies (full table)

---

## Writing Priority Order

1. Section 5 (core contribution) -- write first
2. Section 2 (conceptual foundation) -- write second
3. Section 4 (results) -- write after data available
4. Section 1 (introduction) -- write after 2 and 5 are solid
5. Sections 3, 6, 7 -- write last
