# Theoretical Foundation — Trust Calibration in Educational AI

## Purpose

This document synthesizes the theoretical basis for the two-level trust-calibrated oversight framework. It serves as source material for Sections 2 and 5 of the paper.

---

## 1. Wang et al. (2025) — Anchor Model for Level 1

### Citation
Wang, H., et al. (2025). Understanding trust and reliance in generative AI in education: A stimulus-organism-response framework. *[Journal TBD]*.

### Model: S-O-R Framework Applied to Trust in GenAI Education

```
STIMULUS (S)                    ORGANISM (O)                RESPONSE (R)
├─ System quality          ──>  ├─ Trust               ──>  ├─ Behavioral intention
├─ Information quality     ──>  ├─ Reliance            ──>  └─ Actual use behavior
├─ Service quality         ──>  └─ Resistance
├─ AI anthropomorphism     ──>
└─ Perceived intelligence  ──>
```

### Key Contributions
1. **Distinguishes three constructs**: Trust (belief/attitude), Reliance (behavioral acceptance), Resistance (behavioral rejection)
   - Trust and reliance are positively related but distinct
   - Trust and resistance are negatively related
   - A learner can trust AI yet resist it (or vice versa)
2. **S-O-R mediational model**: AI characteristics (S) shape trust/reliance/resistance (O), which shape use behavior (R)
3. **Educational context**: Specifically models trust in GenAI for education (not general trust)

### Limitations (for our framework)
- **Stops at individual use behavior**: Does not address whether use is *appropriate* (calibrated)
- **No calibration mechanism**: Does not model how trust becomes calibrated or miscalibrated
- **Static snapshot**: Does not model trust change over time (longitudinal calibration)
- **No system design level**: Does not connect individual trust to system oversight design
- **No SDL/metacognition**: Does not include internal calibration mechanisms

### Our Extension
Wang et al. (2025) provides the most complete empirical model for **Level 1** of our framework. We extend it by:
- Adding the calibration dimension (is trust appropriate, not just present?)
- Adding internal calibration mechanisms (SDL, metacognition)
- Connecting to Level 2 (system-mediated calibration)

---

## 2. Lee & See (2004) — Foundation for Trust Calibration

### Citation
Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. *Human Factors, 46*(1), 50-80.

### Key Concepts

**Trust defined as**: "The attitude that an agent will help achieve an individual's goals in a situation characterized by uncertainty and vulnerability" (p. 54).

**Trust calibration**: The degree to which a person's trust matches the actual capability and reliability of the automation.

**Three trust failures**:
| Failure | Definition | Educational AI Example |
|---------|-----------|----------------------|
| **Misuse** | Overtrust --> uncritical reliance on automation | Student copies ChatGPT answer without checking; Bastani et al. (2025) |
| **Disuse** | Distrust --> fails to use beneficial automation | Student refuses to use AI tutor despite evidence it helps |
| **Abuse** | Designer exploits trust asymmetry | AI system designed to maximize engagement over learning |

**Trust formation factors**:
- Performance-based: reliability, competence
- Process-based: transparency, explainability
- Purpose-based: intentions, benevolence

### Relevance to Our Framework
- Lee & See provide the conceptual vocabulary (calibration, misuse, disuse, abuse)
- But their work is in automation/HCI, not education
- We translate these concepts to the educational context where *learning* is the goal

---

## 3. de Visser et al. (2020) — Longitudinal Trust Calibration

### Citation
de Visser, E. J., et al. (2020). Towards a theory of longitudinal trust calibration in human-robot teams. *International Journal of Social Robotics, 12*, 459-478.

### Key Concepts

**Longitudinal calibration**: Trust is not a one-time judgment; it evolves through experience.

**Trust repair**: After trust violations, trust can be restored through:
- Explanations (why the failure occurred)
- Apologies (acknowledgment of error)
- Demonstrations (showing corrected behavior)
- Promise (commitment to improvement)

**Trust dynamics**:
- Initial trust formation (first encounter)
- Trust consolidation (repeated positive experiences)
- Trust violation (unexpected failure)
- Trust repair (recovery mechanisms)
- Calibrated trust (stable, appropriate level)

### Relevance to Our Framework
- Trust calibration is a *process*, not a state
- Educational AI needs to support the full cycle: formation --> violation --> repair --> calibration
- Level 2 mechanisms (checkpoints) should be designed to facilitate this cycle
- de Visser's work is in human-robot teams; we translate to human-AI educational teams

---

## 4. Bastani et al. (2025) — Empirical Evidence for Overtrust Harm

### Citation
Bastani, H., et al. (2025). Generative AI can harm learning. *Proceedings of the National Academy of Sciences (PNAS)*.

### Key Finding
- Turkish high school students given unrestricted GPT-4 access for math practice
- **Result**: Students who used GPT-4 performed WORSE on subsequent math exams
- **Mechanism**: Students over-relied on GPT-4 (overtrust) instead of engaging in productive struggle
- **Mitigation**: When GPT-4 access was paired with "tutoring" prompts (Socratic questioning), the harm was reduced

### Relevance to Our Framework
- **Direct evidence** that uncalibrated trust (overtrust) harms learning
- The "tutoring prompt" intervention is an example of a **Level 2 checkpoint**: it forced the AI to not give direct answers, acting as a calibration mechanism
- Demonstrates that the *same* AI tool can help or harm depending on the trust calibration design
- Strongest empirical motivation for why the field needs the two-level framework

---

## 5. The Two-Level Trust-Calibrated Oversight Framework

### Level 1: Micro (Individual Trust Dynamics)

```
┌─────────────────────────────────────────────────────────┐
│ LEVEL 1: Learner Trust Dynamics                         │
│                                                         │
│ AI System      Trust/Distrust     Reliance/Resistance   │
│ Characteristics ───────────────> ─────────────────────> │
│ (Wang et al.)                                           │
│                                    AI Use Behavior      │
│                        ┌────────> (appropriate/          │
│                        │          inappropriate)         │
│                        │                                │
│ Internal Calibration   │                                │
│ Mechanisms:            │                                │
│ - SDL                  │                                │
│ - Metacognition       ─┘                                │
│ - Critical thinking                                     │
│ - AI literacy                                           │
└─────────────────────────────────────────────────────────┘
```

**Internal calibration mechanisms** (learner-driven):
1. **Self-directed learning (SDL)**: Learners with high SDL autonomously evaluate AI outputs
2. **Metacognition**: Learners monitor their own understanding and question AI when uncertain
3. **Critical thinking**: Systematic evaluation of AI-generated content
4. **AI literacy**: Understanding AI capabilities and limitations

### Level 2: Macro (System-Mediated Trust Calibration)

```
┌─────────────────────────────────────────────────────────┐
│ LEVEL 2: System-Mediated Calibration                    │
│                                                         │
│ Designer/        Checkpoint        Trust Calibration    │
│ Educator    ──>  Design       ──>  Intervention    ──>  │
│                                                         │
│                                    Modifies Level 1     │
│                                    (adjusts trust,      │
│                                     reliance,           │
│                                     resistance)         │
│                                                         │
│ External Calibration Mechanisms:                        │
│ - Teacher checkpoints (guided reflection)               │
│ - System checkpoints (forced pauses, prompts)           │
│ - AI transparency (confidence scores, uncertainty)      │
│ - Friction design (deliberate slowdowns)                │
│ - Socratic mode (Bastani et al. tutoring prompt)        │
│ - Progressive autonomy (start restricted, open up)      │
└─────────────────────────────────────────────────────────┘
```

**External calibration mechanisms** (system/instructor-driven):
1. **Teacher checkpoints**: Instructor-led reflection on AI use quality
2. **System checkpoints**: Built-in pauses requiring learner to verify AI output
3. **AI transparency features**: Confidence scores, explainability, uncertainty indicators
4. **Friction design**: Deliberate UI friction to prevent automatic acceptance (e.g., delay before showing answer, require written reflection before next query)
5. **Socratic mode**: AI withholds direct answers, asks guiding questions instead
6. **Progressive autonomy**: System starts with high oversight, gradually reduces as trust calibrates

### Level Connection: Trust Calibration as the Design Variable

```
Trust Calibration State          Optimal Oversight Level
─────────────────────────────    ────────────────────────
High calibration (appropriate)   Low oversight (more AI autonomy)
Low calibration (overtrust)      High oversight (more checkpoints, friction)
Low calibration (distrust)       Moderate oversight (trust-building, demonstration)
Unknown calibration              Start high, adapt based on monitoring
```

**Key insight**: The optimal oversight level is NOT fixed. It is a function of the learner's current trust calibration state. The framework is dynamic and adaptive.

---

## 6. Evidence Mapping (Expected from Scoping Review)

### Level 1 Evidence (Expected: most studies)
- Wang et al. (2025): Full S-O-R model
- TAM/UTAUT studies: Trust as acceptance predictor
- Studies measuring trust and learning outcomes
- Studies examining reliance/resistance behaviors

### Level 2 Evidence (Expected: very few or none)
- Bastani et al. (2025): Tutoring prompt as calibration mechanism (partial)
- AI transparency/explainability studies in education (if any discuss calibration)
- Teacher intervention studies that monitor trust (unlikely to find)

### The Gap
- **Level 1 is well-studied** (with theoretical fragmentation)
- **Level 2 is almost entirely absent** from educational AI literature
- **The connection between levels** has not been theorized
- **This paper fills this gap**

---

## 7. Adjacent Field Support

These fields have Level 2 thinking but not in educational AI context:

| Field | Relevant Work | Translation to Education |
|-------|--------------|------------------------|
| Automation trust | Lee & See (2004), de Visser et al. (2020) | Trust calibration concepts |
| Human-robot interaction | Hancock et al. (2011), Muir (1994) | Trust measurement, trust repair |
| Clinical decision support | Choudhury et al. (2020) | AI as decision aid, appropriate reliance |
| Explainable AI (XAI) | Miller (2019), Ribeiro et al. (2016) | Transparency as calibration mechanism |
| Friction design | Meier et al. (2019), Cox et al. (2016) | Deliberate friction to improve decisions |
| Nudge theory | Thaler & Sunstein (2008) | Choice architecture for trust |

---

## 8. Synthesis: Why This Matters

1. **Educational AI is different**: Unlike factory automation, the goal is *learning*. Overtrust doesn't just cause task failure -- it prevents learning (Bastani et al., 2025).

2. **Trust calibration is teachable**: Unlike general intelligence or personality, trust calibration can be developed through education and system design.

3. **The field is stuck at Level 1**: Research keeps measuring trust without asking whether it's calibrated, and without designing for calibration.

4. **Level 2 is actionable**: The framework gives designers and educators concrete mechanisms to implement.

5. **Meta-analysis groundwork**: This framework defines what the subsequent meta-analysis should test empirically.
