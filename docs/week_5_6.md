# Week 3–6 Progress Report – 3D Printed Portable AI Quantum Machine

## Timeline: 23 May – 4 June 2025  
Prepared by: Eddie Moualek

---

## Project Overview

This project aims to develop a 3D Printed Portable AI Quantum Machine — a Raspberry Pi-powered educational tool that combines IBM’s RasQberry framework, watsonx AI interfaces, and Qiskit-based quantum games. The objective is to demystify quantum computing for non-specialist audiences through interactive demonstrations and natural-language guidance.

---

## Key Progress Highlights

### 1. Quantum Game Expansion & Interaction Modes
- Developed new games to explore:
  - Quantum Entanglement
  - Tunnelling
  - Deutsch's Algorithm
  - Shor’s Algorithm (for prime factorisation)
- Games now support multiple interaction types:
  - Physical buttons (Sense HAT / GPIO)
  - Command-line interaction
- Designed for broader accessibility and engagement across demos and environments.

### 2. Simulator Challenges & Transition
- Encountered performance issues using the Fakemanilla simulator for large circuit execution.
- Migrated to the noiseless `AerSimulator`, improving responsiveness and stability.
- Simulator change documented in line with IBM guidance on “idealised” environments.

### 3. Platform Integration & UI Alignment
- Worked on integrating quantum games into the RasQberry interface, using shell call structures and JSON-based menu definitions.
- Created logic to allow games to run:
  - Passively in loop mode
  - Interactively based on user selection

### 4. LED Hardware Testing
- Connected LEDs to the Raspberry Pi and verified response to live audio input.
- Used this as a test case before linking visual feedback to quantum game output.
- Confirmed GPIO responsiveness and timing stability.

### 5. Chatbot and Animation Layer Setup
- Began implementing chatbot scaffolding using watsonx-compatible logic.
- Early animation routines were created to enhance user interface feedback and engagement.
- Final integration pending AI access resolution.

### 6. Tie Game Reimplementation
- Reintroduced the original Tie Game demo with updated architecture.
- Adjusted UI and logic flow based on external input to match intended interaction behaviour.
- Ensured seamless reintegration into the platform menu system.

### 7. Leaflet Finalisation
- Finalised and submitted project leaflet.
- Balanced IBM branding use with Imperial College’s design and communication guidelines.
- Designed for a non-technical audience — layout, tone, and visuals optimised for accessibility.

### 8. Video Rework & Voiceover
- Original biweekly video was submitted with incorrect format and lacked narration.
- Replaced low-quality footage, edited in correct game walkthroughs, and added voiceover narration explaining project progress.
- Included a final live clip for authenticity and personal engagement.

---

## IBM SkillsBuild Learning Progress

- Completed:
  - Classifying Data Using IBM Granite
- RAG Analysis updated to reflect progress and reprioritised courses based on ongoing project needs.

---

## Key Notes from Internal Meeting – 03 June 2025

- Introduced “Claude Code” tool for productivity (corrected from “Cloud Code”).
- Discussed simulator architecture, update strategies, and GitHub-linked deployment methods.
- Dynamic Raspberry Pi update scripting proposed for smoother rollouts.
- UI integration and game flexibility approved across command-line, touch, and passive modes.

---

## Key Takeaways

- Simulator flexibility is essential for live demos — switching to stable environments early paid off.
- Ownership of communication tasks (e.g. video fix, minutes, clarification) strengthened project delivery.
- Multi-modal input options improved potential for audience engagement during outreach.

---

## Next Steps

- Finalise chatbot interaction and complete AI integration testing.
- Expand LED-driven game feedback and animation layers.
- Prepare mid-project OIC presentation.
- Continue Jira and GitHub structuring for traceable, collaborative development.

---

## Reference Links

- [Project Minutes – 03/06/2025 (PDF):](https://1drv.ms/b/c/1772c53d76259fc4/EXuCs8A4DbhCuAW8g1zfctYBbxj7GsIyjUK4-_qUwMNh_w?e=f5GYdg)
- [Week 3–6 Video Update:](https://1drv.ms/v/c/1772c53d76259fc4/EUK-lWt6yeRLuQLRQlDd9acBM8vOAQppoUycONMfOCWMKw?e=OLRzbD)
- [Learning Journal / RAG Analysis:](https://docs.google.com/spreadsheets/d/1sF9Oc2OouF73Z6AvovJ69b6G2dEbBKRIfdPd3dAS7XI/edit?usp=sharing)
- [GitHub Repository:](https://github.com/EddieMoualek2003/ibm_imperial_qc)
- [Jira Board:](https://team9ibmquantum.atlassian.net/jira/software/projects/AQMP/summary?atlOrigin=eyJpIjoiN2IwNmVlOTcwNTMwNGExOTk2MTJkYjA2Y2VlOTk2OGUiLCJwIjoiaiJ9)

---

Thank you for following our progress. We're excited to continue building out this platform into a fully interactive, portable, and intelligent quantum computing demo suite.
