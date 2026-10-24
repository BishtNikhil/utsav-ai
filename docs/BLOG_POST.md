# 🔱 Beyond Chatbots: Engineering UtsavAI for PromptWars Virtual Challenge 05
### How I Built an Autonomous Celebration & Event Orchestrator with Google Gemini 2.5 Flash & Dynamic Constraint Graphs

*By Nikhil Singh Bisht | PromptWars Double-Award Champion & MCA (Cloud Systems & AI)*

---

When Hack2skill and Google for Developers unveiled **Main Challenge 05: Celebration & Event Planner** for PromptWars Virtual, Subject Matter Expert Srinivas laid down a gauntlet in the live explainer session:

> *"Event planning is not one single problem; it is a collection of connected smaller problems. Generating ideas is easy. Turning those ideas into an execution plan that dynamically balances budget, guest dependencies, vendor trade-offs, and deadlines is the real challenge."*

Most hackathon participants jump straight into wrapping an LLM in a basic chat UI that responds with: *"Here are 10 wedding ideas and a generic checklist!"* 

I wanted to build something fundamentally different: **UtsavAI (उत्सव AI)** — an autonomous event planner that models celebrations as a **dynamic constraint graph**, passing the SME's rigorous **"Change Test"** with zero friction.

Here is the architectural deep dive into how I built it.

---

## 🎯 1. The Core Engineering Challenge: Connected Dependencies

In real-world celebrations, changes never happen in isolation:
- If your **guest headcount rises from 200 to 250**, your catering budget must immediately expand, your venue minimum square footage must jump from 2,400 to 3,000 sq.ft, and your seating layout must adapt.
- If your **budget is cut by 10%**, the AI should **never** just blindly slash every category equally. It must suggest **priority-aligned trade-offs** (e.g. protecting gourmet food while switching from imported floral arches to local botanical decor).
- If your **event is advanced by 2 weeks**, downstream milestones (tasting, invitations, RSVP lock) must automatically compress without violating critical lead times.

To solve this, I designed a hybrid architecture: **Deterministic Constraint Engines for precision mathematics + Google Gemini 2.5 Flash for cultural synthesis and contextual reasoning.**

### 🏛️ The UtsavAI Architectural Pipeline:
* **1. Deterministic Dependency Engine:** Dynamic headcount-to-catering scaling, venue minimum checks (12 sq.ft/guest), and automatic 7% contingency reserve.
* **2. Priority-Shielding Trade-Off Engine:** Contextual cost rationalization protecting top user-ranked priorities during budget cuts (no blind uniform slashing).
* **3. Milestone DAG Scheduler:** Directed Acyclic Graph enforcing strict topological prerequisites and auto-cascading schedule compression.
* **4. Google Gemini 2.5 Flash Generative Core:** Cultural atmosphere moodboards, vendor contract auditing (uncovering undisclosed 18% GST & overtime levies), and targeted negotiation scripts.

---

## 🤖 2. What GenAI Handled vs. What Custom Code Handled

A core requirement from the PromptWars jury is distinguishing genuine engineering from superficial prompt wrapping:

### What Custom Code Handled (Zero-Hallucination Core):
1. **Budget Constraint Mathematics (`DependencyEngine`):** Accurate per-plate calculations, floor limits, and automatic ringfencing of a 7% contingency reserve (₹56,000 on an ₹8L budget).
2. **Topological Milestone Scheduling (`TimelineDAGService`):** Directed Acyclic Graph enforcing that venue contracts must be signed before catering tastings or invitations can be dispatched.
3. **The "Change Test" Re-anchoring:** Dynamically recalculated parameters in memory without session loss.

### What Google Gemini 2.5 Flash Handled:
1. **Aesthetic & Theme Synthesis:** Synthesizing rich multi-ceremony schedules (*Shubh Haldi, Mehendi Soirée, Vedic Pheras, Grand Reception*) with dress codes and acoustic vibes.
2. **Vendor Quotation Intelligence:** Analyzing competing vendor quotes, uncovering undisclosed 18% GST surcharges, fuel levies, and late-night overtime penalties.
3. **Negotiation Copilot:** Equipping organizers with sharp, contextual questions before signing vendor contracts.

---

## 💥 3. The Live "Change Test" Benchmark

During the live explainer, Srinivas challenged teams with a specific test scenario:
> *"A user creates an ₹8 Lakh, 200-guest wedding plan 4 months away, and then returns saying: 'Actually, we have 50 more guests, the budget is cut by 10%, and the event is 2 weeks earlier.' Does your app handle this or does the user start over?"*

In UtsavAI, clicking the **"Execute Live Change Test"** button triggers an instantaneous live re-anchoring:
- **Headcount:** 200 ➔ 250 (+50 attendees accommodated).
- **Budget:** ₹8,00,000 ➔ ₹7,20,000 (-10% reduction absorbed).
- **Catering:** Re-balanced to maintain ₹1,750/plate quality by applying the Priority-Shielding strategy (trimming non-essential decor).
- **Milestone DAG:** Squeezed by 14 days, with invitations and digital RSVPs promoted to critical priority.

All without resetting user inputs or losing context!

---

## 🧪 4. Zero-Secret Law & Automated Testing

Maintaining high code quality and security is paramount:
- **Zero-Secret Compliance:** Strict `.gitignore` enforcement; all Gemini API keys live in environment variables.
- **Automated Test Suite:** 14 unit and integration tests passing in **2.74 seconds** using `pytest` and `httpx`.
- **Repository Size:** Fully optimized under **10 MB**, packaged with a production [Dockerfile](file:///e:/Promptwars2026/utsav_ai/Dockerfile) ready for Google Cloud Run.

---

## 🔱 Reflection & Next Steps

Participating in PromptWars Virtual has been an incredible opportunity to push the boundaries of vibe-coding into robust, reliable software architecture. Thank you to Hack2skill and Google for Developers for organizing this challenge!

🔗 **Live Application:** https://utsav-ai-alpha.vercel.app  
🔗 **GitHub Repo:** https://github.com/BishtNikhil/utsav-ai  
🔗 **Demo Video Stream:** [Google Drive 1080p Stream](https://drive.google.com/file/d/15M74Su34BJiH71e9uMq9b0ZS7RQC802Z/view?usp=sharing)  

#GoogleForDevelopers #PromptWars #PromptWarsVirtual #GenAI #Gemini #FastAPI #CloudRun #Python #AIHackathon #SoftwareEngineering
