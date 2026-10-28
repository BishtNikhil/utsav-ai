# Contributing to UtsavAI (उत्सव AI)

Thank you for your interest in contributing to **UtsavAI**, the autonomous dynamic celebration and event orchestrator built for the **PromptWars Virtual 2026** Challenge (Hack2skill × Google for Developers).

---

## 🏛️ Architecture & Core Principles

1. **Deterministic Constraint Invariance:**
   - Financial mathematics (catering floor minimums, square footage calculations, and 7% ringfenced contingency shields) are calculated deterministically via `DependencyEngine`.
   - Never replace mathematical rules with unconstrained generative AI prompts.
2. **Topological Milestone DAG:**
   - Milestones are organized as a Directed Acyclic Graph (`TimelineDAGService`). Schedule shifts must cascade topological compressions downstream without circular dependencies.
3. **Zero-Secret Law:**
   - Never commit API keys, secrets, or bearer tokens to Git. All credentials must be read from environment variables via `app.config.AppConfig`.

---

## 🛠️ Development Setup & Quality Standards

1. **Virtual Environment & Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install pytest httpx
   ```

2. **Automated Testing Protocol:**
   Every contribution must pass the complete automated test matrix:
   ```bash
   python -m pytest tests/ -v
   ```

3. **Code Style & Type Annotations:**
   - Strict Python 3.11+ type hints (`typing.Dict`, `typing.List`, `typing.Optional`, `typing.Tuple`).
   - Google-style docstrings with `Args:`, `Returns:`, and `Raises:` clauses.
   - Pydantic v2 schemas for all intake, output, and domain data models.

4. **Accessibility (WCAG 2.4.1 Compliance):**
   - All interactive controls must support full keyboard navigation (`tabindex`, skip links).
   - Dynamic real-time metrics must have `aria-live="polite"` and `aria-atomic="true"`.
   - High-contrast visual focus rings (`:focus-visible`) must be preserved.

---

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
