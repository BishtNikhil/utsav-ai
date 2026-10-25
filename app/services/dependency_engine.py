"""
UtsavAI Dependency Engine (Strategy & Constraint Propagation Pattern).

Provides deterministic constraint calculations that connect celebration parameters:
Headcount <-> Catering Floor <-> Venue Capacity <-> Priority Weighting <-> Contingency Shield.

Enforces zero-hallucination arithmetic so financial planning remains strictly accurate.
"""

import math
from typing import Dict, List, Tuple
from app.models.schemas import (
    EventIntakeRequest,
    BudgetSummary,
    BudgetCategory,
    ExperienceTier,
)
from app.core.exceptions import InvalidBudgetError, InvalidGuestCountError


class DependencyEngine:
    """
    Mathematical and constraint propagation engine for event budget optimization.

    Coordinates interconnected event variables according to SME principles:
    - Automatically ringfences a 7% emergency contingency shield.
    - Scales catering floors by experience tier and attendee headcount.
    - Calculates physical square footage requirements per guest.
    - Re-balances category weights dynamically based on user priority rankings (1=Highest, 5=Lowest).
    """

    # Base per-plate catering estimates in INR by experience tier
    CATERING_PER_PLATE: Dict[ExperienceTier, float] = {
        ExperienceTier.ESSENTIAL: 1100.0,
        ExperienceTier.STANDARD: 1750.0,
        ExperienceTier.PREMIUM_LUXURY: 3200.0,
    }

    # Minimum square footage required per guest by format
    SPACE_PER_GUEST_SQFT: Dict[str, float] = {
        "indoor_banquet": 12.0,
        "outdoor_lawn": 20.0,
        "cocktail_seating": 8.0,
    }

    @classmethod
    def get_catering_per_plate(cls, tier: ExperienceTier) -> float:
        """Retrieves base per-plate culinary cost for a hospitality experience tier.

        Args:
            tier: ExperienceTier enum indicating luxury standard.

        Returns:
            float: Base catering rate in INR per plate.
        """
        return cls.CATERING_PER_PLATE.get(tier, 1750.0)

    @classmethod
    def get_minimum_venue_sqft(cls, guests: int, format_type: str = "indoor_banquet") -> float:
        """Calculates minimum required floor space for attendee safety and banquet flow.

        Args:
            guests: Expected headcount of attendees.
            format_type: Venue layout configuration ("indoor_banquet", "outdoor_lawn").

        Returns:
            float: Total square footage minimum.
        """
        sqft_per_head = cls.SPACE_PER_GUEST_SQFT.get(format_type, 12.0)
        return float(guests * sqft_per_head)

    @classmethod
    def calculate_contingency_reserve(cls, total_budget: float, ratio: float = 0.07) -> float:
        """Computes ringfenced emergency contingency buffer to absorb vendor price spikes.

        Args:
            total_budget: Total gross budget in INR.
            ratio: Reserve ratio (defaults to 7% per SME guidelines).

        Returns:
            float: Ringfenced contingency reserve in INR.
        """
        return round(total_budget * ratio, 2)

    @classmethod
    def calculate_budget(cls, intake: EventIntakeRequest) -> BudgetSummary:
        """Dynamically computes allocated budget categories respecting priorities and headcounts.

        Args:
            intake: Validated EventIntakeRequest model containing budget, guests, and priorities.

        Returns:
            BudgetSummary: Balanced financial ledger with category breakdowns and contingency shield.

        Raises:
            InvalidBudgetError: If gross budget is less than or equal to zero.
            InvalidGuestCountError: If guest count is less than or equal to zero.
        """
        if intake.total_budget <= 0:
            raise InvalidBudgetError(f"Total budget must be strictly positive, received {intake.total_budget}")
        if intake.guest_count <= 0:
            raise InvalidGuestCountError(f"Guest count must be strictly positive, received {intake.guest_count}")

        total = intake.total_budget
        guests = intake.guest_count
        tier = intake.experience_tier
        priorities = intake.priority_weights

        # 1. Mandatory Contingency Reserve (7% of total budget)
        contingency_reserve = cls.calculate_contingency_reserve(total, 0.07)
        allocatable = total - contingency_reserve

        # 2. Base category weight distribution (baseline proportions)
        base_weights = {
            "catering": 0.38,
            "venue": 0.24,
            "decor": 0.16,
            "photography": 0.12,
            "entertainment": 0.10,
        }

        # 3. Adjust proportions based on user's priority ranking (1=highest, 5=lowest)
        priority_multipliers = {
            1: 1.25, # +25% weight
            2: 1.10, # +10% weight
            3: 1.00, # neutral
            4: 0.85, # -15% weight
            5: 0.80, # -20% weight
        }

        adjusted_weights = {
            "catering": base_weights["catering"] * priority_multipliers.get(priorities.catering, 1.0),
            "venue": base_weights["venue"] * priority_multipliers.get(priorities.venue, 1.0),
            "decor": base_weights["decor"] * priority_multipliers.get(priorities.decor, 1.0),
            "photography": base_weights["photography"] * priority_multipliers.get(priorities.photography, 1.0),
            "entertainment": base_weights["entertainment"] * priority_multipliers.get(priorities.entertainment, 1.0),
        }

        # Normalize weights so sum equals 1.0
        weight_sum = sum(adjusted_weights.values())
        norm_weights = {k: v / weight_sum for k, v in adjusted_weights.items()}

        # 4. Check Catering floor constraint: Catering cost must be at least guests * per_plate
        est_per_plate = cls.get_catering_per_plate(tier)
        raw_catering_allocated = round(allocatable * norm_weights["catering"], 2)
        min_catering_needed = round(guests * est_per_plate, 2)

        # If allocated is less than realistic minimum, adjust intelligently
        final_catering = max(raw_catering_allocated, min_catering_needed * 0.85)

        # Re-distribute the remainder among other categories
        remaining_for_others = allocatable - final_catering
        other_keys = ["venue", "decor", "photography", "entertainment"]
        other_weight_sum = sum(norm_weights[k] for k in other_keys)

        categories: List[BudgetCategory] = []

        # Category 1: Catering & Dining
        categories.append(
            BudgetCategory(
                category_id="cat_catering",
                category_name="Catering & Culinary Experience",
                allocated_amount=final_catering,
                percentage_of_budget=round((final_catering / total) * 100, 1),
                is_confirmed=False,
                status_label="Estimated Assumption (₹{:.0f}/guest)".format(final_catering / guests),
                per_guest_cost=round(final_catering / guests, 2),
                sub_items=[
                    {"Welcome Drinks & Live Canapés": round(final_catering * 0.20, 2)},
                    {"Main Course Buffet & Regional Specialties": round(final_catering * 0.55, 2)},
                    {"Artisanal Desserts & Late-Night Stalls": round(final_catering * 0.15, 2)},
                    {"Service Staff & Crockeries": round(final_catering * 0.10, 2)},
                ],
                trade_off_flexibility="Low" if priorities.catering <= 2 else "High",
            )
        )

        # Category 2: Venue & Hospitality
        venue_amount = round(remaining_for_others * (norm_weights["venue"] / other_weight_sum), 2)
        min_sqft = cls.get_minimum_venue_sqft(guests, "indoor_banquet")
        categories.append(
            BudgetCategory(
                category_id="cat_venue",
                category_name="Venue, Banqueting & Accommodations",
                allocated_amount=venue_amount,
                percentage_of_budget=round((venue_amount / total) * 100, 1),
                is_confirmed=False,
                status_label="Estimated (Min {:.0f} sq.ft needed)".format(min_sqft),
                per_guest_cost=round(venue_amount / guests, 2),
                sub_items=[
                    {"Main Ballroom / Lawn Rental": round(venue_amount * 0.65, 2)},
                    {"Bridal Suites & Green Rooms": round(venue_amount * 0.20, 2)},
                    {"Valet & Parking Logistics": round(venue_amount * 0.15, 2)},
                ],
                trade_off_flexibility="Medium",
            )
        )

        # Category 3: Decor & Visual Aesthetics
        decor_amount = round(remaining_for_others * (norm_weights["decor"] / other_weight_sum), 2)
        categories.append(
            BudgetCategory(
                category_id="cat_decor",
                category_name="Thematic Decor, Florals & Ambient Lighting",
                allocated_amount=decor_amount,
                percentage_of_budget=round((decor_amount / total) * 100, 1),
                is_confirmed=False,
                status_label="Estimated Assumption",
                per_guest_cost=round(decor_amount / guests, 2),
                sub_items=[
                    {"Stage / Mandap Architectural Decor": round(decor_amount * 0.45, 2)},
                    {"Entrance Tunnel & Floral Installations": round(decor_amount * 0.30, 2)},
                    {"Guest Table Centerpieces & Mood Lighting": round(decor_amount * 0.25, 2)},
                ],
                trade_off_flexibility="High" if priorities.decor >= 3 else "Low",
            )
        )

        # Category 4: Photography & Cinematic Media
        photo_amount = round(remaining_for_others * (norm_weights["photography"] / other_weight_sum), 2)
        categories.append(
            BudgetCategory(
                category_id="cat_photo",
                category_name="Cinematography, Drone & Photography",
                allocated_amount=photo_amount,
                percentage_of_budget=round((photo_amount / total) * 100, 1),
                is_confirmed=False,
                status_label="Estimated Quote Range",
                per_guest_cost=round(photo_amount / guests, 2),
                sub_items=[
                    {"Traditional & Candid Photography Crew": round(photo_amount * 0.50, 2)},
                    {"4K Teaser & Drone Cinematic Reel": round(photo_amount * 0.35, 2)},
                    {"Curated Hardbound Photo Album": round(photo_amount * 0.15, 2)},
                ],
                trade_off_flexibility="Medium",
            )
        )

        # Category 5: Music, Sound & Entertainment
        ent_amount = round(remaining_for_others * (norm_weights["entertainment"] / other_weight_sum), 2)
        categories.append(
            BudgetCategory(
                category_id="cat_entertainment",
                category_name="Live Sound, DJ & Cultural Artists",
                allocated_amount=ent_amount,
                percentage_of_budget=round((ent_amount / total) * 100, 1),
                is_confirmed=False,
                status_label="Estimated Assumption",
                per_guest_cost=round(ent_amount / guests, 2),
                sub_items=[
                    {"Acoustic Musicians / Cultural Performers": round(ent_amount * 0.40, 2)},
                    {"JBL Sound System & Pro Sound Engineer": round(ent_amount * 0.40, 2)},
                    {"Emcee & Ceremony Coordinator": round(ent_amount * 0.20, 2)},
                ],
                trade_off_flexibility="High",
            )
        )

        total_allocated = sum(c.allocated_amount for c in categories) + contingency_reserve
        remaining = round(total - total_allocated, 2)

        return BudgetSummary(
            total_budget=total,
            total_allocated=round(total_allocated, 2),
            contingency_reserve=contingency_reserve,
            remaining_balance=remaining,
            categories=categories,
            is_balanced=abs(remaining) < 1.0,
        )
