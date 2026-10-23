import json
import logging
from typing import Dict, Any, Optional
import httpx
from app.config import config
from app.models.schemas import EventIntakeRequest

logger = logging.getLogger(__name__)

class GeminiService:
    """
    Client for Google Gemini 2.5 Flash / 1.5 Flash.
    Provides generative reasoning for event aesthetics, customized trade-offs,
    and prompt evolution while maintaining deterministic offline fallback.
    """

    SYSTEM_PROMPT = """
You are UtsavAI, an elite event planner and architectural budget optimizer collaborating with Google for Developers.
You never output vague advice. You analyze connected event constraints:
Guest Count <-> Catering Per Plate <-> Venue Minimum SqFt <-> Decor Scale <-> Timeline Milestones.
Given event specifications, produce structured, highly personalized strategic recommendations.
Highlight explicit trade-offs when budgets or deadlines tighten, rather than suggesting blanket cuts.
"""

    @classmethod
    async def generate_ai_narrative(cls, intake: EventIntakeRequest, budget_summary_dict: Dict[str, Any]) -> str:
        """
        Calls Gemini API if GEMINI_API_KEY is available, or generates a deterministic synthesis.
        """
        if not config.has_gemini_key:
            return cls._generate_offline_synthesis(intake, budget_summary_dict)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.gemini_model}:generateContent?key={config.gemini_api_key}"
        
        prompt = f"""
Event: {intake.title} ({intake.category.value})
Target Date: {intake.target_date} in {intake.location_city}
Guests: {intake.guest_count} attendees | Budget: ₹{intake.total_budget:,.2f} INR
Experience Tier: {intake.experience_tier.value}
Priorities: Catering={intake.priority_weights.catering}, Venue={intake.priority_weights.venue}, Decor={intake.priority_weights.decor}, Photography={intake.priority_weights.photography}
Must Haves: {', '.join(intake.must_haves)}
Special Notes: {intake.special_notes}

Provide an executive 3-paragraph strategy:
1. Architectural Theme & Atmosphere Synthesis
2. Key Budget Allocation Justification (explaining why priority #{intake.priority_weights.catering} was favored)
3. Risk Mitigation & Timeline Acceleration Strategy
"""

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": cls.SYSTEM_PROMPT},
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 600,
            }
        }

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"].strip()
                logger.warning(f"Gemini API returned status {res.status_code}, using fallback narrative.")
        except Exception as e:
            logger.warning(f"Gemini API call failed ({e}), falling back to deterministic engine.")

        return cls._generate_offline_synthesis(intake, budget_summary_dict)

    @classmethod
    def _generate_offline_synthesis(cls, intake: EventIntakeRequest, budget_summary_dict: Dict[str, Any]) -> str:
        """
        Deterministic, domain-rich fallback narrative ensuring 100% uptime without an external API key.
        """
        top_p = "Catering" if intake.priority_weights.catering == 1 else "Venue"
        secondary_p = "Decor" if intake.priority_weights.decor <= 2 else "Photography"
        per_head = intake.total_budget / intake.guest_count

        return (
            f"**Strategic Event Blueprint for {intake.title}:**\n\n"
            f"1. **Atmosphere & Aesthetic Synthesis:** Tailored for a {intake.experience_tier.value.replace('_', ' ').title()} celebration "
            f"in {intake.location_city}, designed around {intake.guest_count} valued guests. "
            f"The experience blends modern elegance with cultural intimacy, with ₹{per_head:,.0f} invested per attendee.\n\n"
            f"2. **Constraint & Budget Rationale:** In accordance with your priority ranking, **{top_p}** and **{secondary_p}** "
            f"receive protective capital allocation. We anchored catering with a dedicated per-guest buffer while ringfencing a "
            f"7% contingency reserve (₹{budget_summary_dict.get('contingency_reserve', 0):,.2f}) to absorb last-minute vendor price escalations.\n\n"
            f"3. **Dynamic Execution & Change-Resilience:** The timeline enforces critical path dependencies: Venue & Date locking "
            f"must conclude before invitation distribution. If dates or headcounts shift, UtsavAI's DAG engine automatically "
            f"recalculates milestones and suggests priority-shielded trade-offs."
        )
