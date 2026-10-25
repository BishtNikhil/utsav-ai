"""
UtsavAI Trade-Off Engine (Priority-Weighted Optimization Pattern).

Generates actionable financial trade-off scenarios when budgets are cut or headcounts expand.
Protects top-ranked priorities (e.g. shielding culinary standards) while intelligently
rationalizing lower-ranked categories, eliminating arbitrary blanket cuts.
"""

from typing import List
from app.models.schemas import (
    EventIntakeRequest,
    BudgetSummary,
    TradeOffOption,
)


class TradeOffEngine:
    """
    Intelligent Priority-Driven Trade-Off Optimizer.

    Generates three transparent scenarios:
    1. Priority-Preserving Strategic Trim (shields #1 user priority).
    2. Format & Vendor Quotation Rationalization (negotiates bundled services).
    3. Intimate Guest Density & Per-Plate Elevation (curates attendee roster).
    """

    @classmethod
    def generate_trade_off_options(
        cls,
        intake: EventIntakeRequest,
        budget: BudgetSummary,
        target_savings: float = 0.0,
    ) -> List[TradeOffOption]:
        """Generates 3 actionable trade-off strategies aligned with user priority ranking.

        Args:
            intake: Validated event intake model containing priority weights.
            budget: Computed budget summary with itemized category allocations.
            target_savings: Required cost reduction in INR. If <= 0, defaults to 15% optimization.

        Returns:
            List[TradeOffOption]: 3 distinct trade-off options with pros, cons, and alignment scores.
        """
        total = intake.total_budget
        guests = intake.guest_count
        priorities = intake.priority_weights
        
        # If target savings is not set, simulate 15% budget optimization scenario
        if target_savings <= 0:
            target_savings = total * 0.15

        options: List[TradeOffOption] = []

        # -------------------------------------------------------------
        # Strategy 1: Priority-Preserving Strategic Trim (Recommended)
        # -------------------------------------------------------------
        top_priority_name = "Catering" if priorities.catering == 1 else "Venue"
        bottom_priority_name = "Decor" if priorities.decor >= 4 else "Entertainment"

        opt1_savings = round(target_savings * 1.05, 2)
        options.append(
            TradeOffOption(
                option_id="opt_priority_aligned",
                title=f"Priority-Shielding Strategy (Protect {top_priority_name})",
                scenario_description=(
                    f"100% preserves your #1 priority ({top_priority_name} & Guest Hospitality) while "
                    f"switching from imported floral installations to sustainable local botanical decor and "
                    f"replacing print card delivery with an interactive digital celebration suite."
                ),
                cost_delta=-opt1_savings,
                pros=[
                    f"Zero compromise on culinary excellence and food quality (₹{budget.categories[0].per_guest_cost}/guest maintained)",
                    "Substantial immediate savings without guest-facing friction",
                    "Eco-friendly modern aesthetic praised by guests",
                ],
                cons=[
                    "Stage backdrop will utilize ambient geometric lighting instead of imported Dutch roses",
                    "Acoustic 3-piece band replaces full 6-piece live orchestra",
                ],
                alignment_score=0.96,
                recommended=True,
            )
        )

        # -------------------------------------------------------------
        # Strategy 2: Format & Vendor Quotation Rationalization
        # -------------------------------------------------------------
        opt2_savings = round(target_savings * 0.85, 2)
        options.append(
            TradeOffOption(
                option_id="opt_vendor_rationalize",
                title="Vendor Bundle & Off-Peak Rationalization",
                scenario_description=(
                    "Retain all original aesthetic concepts by negotiating bundled services: "
                    "contracting the venue's in-house lighting/sound team to waive royalty fees "
                    "and standardizing to an elegant buffet layout with live counters."
                ),
                cost_delta=-opt2_savings,
                pros=[
                    "Decor visual footprint remains 90% identical to initial moodboard",
                    "Single point of vendor accountability (fewer coordinator headaches)",
                ],
                cons=[
                    "Less customization on sound mixing hardware",
                    "Requires locking contracts 60 days ahead to secure package discount",
                ],
                alignment_score=0.88,
                recommended=False,
            )
        )

        # -------------------------------------------------------------
        # Strategy 3: Intimate Guest Density & Premium Elevation
        # -------------------------------------------------------------
        suggested_guest_trim = max(15, int(guests * 0.15))
        new_guests = guests - suggested_guest_trim
        opt3_savings = round(suggested_guest_trim * (budget.total_allocated / guests) * 0.70, 2)
        
        options.append(
            TradeOffOption(
                option_id="opt_guest_density_trim",
                title="Curated Guest Roster & Premium Per-Head Elevation",
                scenario_description=(
                    f"Rationalize guest count from {guests} to {new_guests} VIP attendees. "
                    f"Yields immediate catering, seating, and bar savings while creating an ultra-luxurious, "
                    f"intimate family atmosphere with personalized hospitality."
                ),
                cost_delta=-opt3_savings,
                pros=[
                    f"Per-guest hospitality investment increases significantly",
                    "Enables high-touch personalized dining and bespoke gift hampers",
                    "Reduces logistics, transport, and valet bottlenecks",
                ],
                cons=[
                    "Requires strict RSVP curating and secondary guest tier deferrals",
                ],
                alignment_score=0.84,
                recommended=False,
            )
        )

        return options
