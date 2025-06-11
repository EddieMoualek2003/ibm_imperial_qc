# Week 1–2 Progress Blog – 3D Printed Portable AI Quantum Machine

## Project Overview

This project aims to develop a **3D Printed Portable AI Quantum Machine** - a Raspberry Pi-powered platform integrating IBM’s RasQberry framework, watsonx AI, and interactive Qiskit-based games. The goal is to provide an engaging educational tool that demystifies quantum computing for a general audience using natural language interfaces and gamified learning.

---

## Key Progress Areas (Weeks 1–2)

### 1. **IBM Platform Setup**

- Registered for IBM SkillsBuild and created the IBM Cloud account
- Initiated core AI learning pathway:
  - [Getting Started with AI](https://www.credly.com/badges/e693dfd6-4c73-472f-9917-c46db637d4d4/public_url)
  - [Granite for Software Development](https://skills.yourlearning.ibm.com/activity/MDL-567)
- Reviewed access requirements and constraints for Watsonx Assistant and identified platform limitations with the standard tier

### 2. **Qiskit Demo Migration and Compatibility Work**

- Updated and refactored several of the existing RasQberry demo games
- Migrated the codebase to the **latest Qiskit SDK**, replacing deprecated calls and adapting circuit syntax for stability
- Transitioned all games to use the modern `aer_simulator` backend to ensure long-term compatibility
- Conducted test runs and verified that the updated demos perform consistently across local and Raspberry Pi environments

### 3. **Raspberry Pi Deployment and Emulator Testing**

- Deployed the newly updated quantum demo suite to a Raspberry Pi system
- Configured and tested the Sense HAT emulator to simulate final user interaction experience
- Verified end-to-end functionality in the absence of physical hardware, ensuring seamless migration once devices are connected

---

## Additional Team Contributions

- Successfully 3D printed the base model for the RasQberry enclosure using open-source design files
- Preliminary exploration of alternatives to Watsonx for the voice/AI interface, based on current access constraints

---

## Key Takeaways

- **Technical Adaptation**:
  - Migrating legacy quantum circuits to new Qiskit versions revealed the importance of long-term maintenance for educational software
- **Emulation First**:
  - The emulator-first approach enabled productive parallel development while awaiting final hardware components
- **Platform Planning**:
  - Early identification of cloud-tier limitations has helped steer decisions around scalable and accessible AI integration

---

## Next Steps

- Identify and implement an accessible AI assistant solution (with or without Watsonx, depending on access resolution)
- Begin LED feedback integration into the 3D housing for dynamic response to game outputs
- Finalize Sense HAT hardware testing and user interaction validation once hardware arrives
- Expand project Jira structure and assign task-based ownership for collaborative execution

---

## Certifications & Resources

- [IBM SkillsBuild AI Pathway](https://www.credly.com/badges/e693dfd6-4c73-472f-9917-c46db637d4d4/public_url)
- [Granite for Software Development](https://skills.yourlearning.ibm.com/activity/MDL-567)
- [Learning Journal / RAG Analysis](https://docs.google.com/spreadsheets/d/1sF9Oc2OouF73Z6AvovJ69b6G2dEbBKRIfdPd3dAS7XI/edit?usp=sharing)
- [Jira Board](https://team9ibmquantum.atlassian.net/jira/software/projects/SCRUM/list?filter=updatedDate+%3E%3D+-1w&atlOrigin=eyJpIjoiZmNlMzgzNWFkNThjNDMzYjk1MmUwMTAzNDE0OGI2MWEiLCJwIjoiaiJ9)
- [GitHub Repo](https://github.com/NightRaven3142/Team9-IBMQuantumAIMachine/tree/main)
- [Video Update (Week 1–2)](https://github.com/NightRaven3142/Team9-IBMQuantumAIMachine/tree/main)

---

Thank you for following our project’s early progress. We're excited to continue building on this foundation over the coming weeks.
