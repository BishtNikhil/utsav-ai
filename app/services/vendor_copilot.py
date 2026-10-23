from typing import List
from app.models.schemas import VendorQuote, VendorComparison

class VendorCopilotService:
    """
    Vendor Management & Quotation Analysis Copilot.
    Structures vendor negotiations, uncovers hidden charges (taxes, overtime, generator),
    and equips organizers with sharp qualification questions.
    """

    @classmethod
    def get_curated_comparisons(cls, guest_count: int, city: str) -> List[VendorComparison]:
        """
        Generates realistic, comparative quotation intelligence across core event categories.
        """
        comparisons: List[VendorComparison] = []

        # -------------------------------------------------------------
        # 1. Catering Quotation Analysis
        # -------------------------------------------------------------
        caterer_a = VendorQuote(
            vendor_id="cat_vendor_01",
            vendor_name="The Royal Rasoi Collective",
            category="Catering",
            base_quote=float(guest_count * 1650),
            tax_and_fees=float(guest_count * 1650 * 0.18),
            total_cost=round(guest_count * 1650 * 1.18, 2),
            per_plate_or_unit=1650.0,
            inclusions=[
                "4 Live Starters + 8 Main Course curries",
                "Artisanal Tandoor + Bread station",
                "Bone china crockery, cutlery & linen setup",
                "1 Dedicated Captain per 25 guests",
            ],
            exclusions=[
                "Mocktail / Fresh juice bar counter (+₹250/head)",
                "Post-midnight tea / coffee counter",
            ],
            hidden_costs_flagged=[
                "18% GST not included in initial verbal quote",
                "Fuel surcharge for mobile gas tandoor (₹6,500)",
                "Crockery breakage deposit of ₹15,000 required",
            ],
            verified=True,
        )

        caterer_b = VendorQuote(
            vendor_id="cat_vendor_02",
            vendor_name="Himalayan Gourmet & Heritage Kitchen",
            category="Catering",
            base_quote=float(guest_count * 1450),
            tax_and_fees=float(guest_count * 1450 * 0.05), # Composite 5% GST
            total_cost=round(guest_count * 1450 * 1.05, 2),
            per_plate_or_unit=1450.0,
            inclusions=[
                "Authentic Kumaoni / Pahadi organic specialty counter",
                "Unlimited welcome mocktails and hot kahwa",
                "Eco-friendly brass & terracotta serving ware",
                "Includes all gas fuel & logistics within 50 km",
            ],
            exclusions=[
                "Continental dessert station",
                "Uniformed valet water servers",
            ],
            hidden_costs_flagged=[
                "Overtime fee of ₹3,000/hr if dinner extends past 11:30 PM",
            ],
            verified=True,
        )

        comparisons.append(
            VendorComparison(
                category="Catering & Hospitality",
                quotes=[caterer_a, caterer_b],
                recommended_vendor_id="cat_vendor_02",
                key_trade_offs=[
                    "Himalayan Gourmet is ₹44,000 cheaper with lower 5% composite GST.",
                    "The Royal Rasoi offers a larger continental dessert spread but charges 18% GST + crockery deposit.",
                ],
                negotiation_questions=[
                    "Is service staff tipping included or will captain demand cash tips day-of?",
                    "What is your exact per-plate discount if guest count crosses 250?",
                    "Do you provide a formal food safety license and kitchen hygiene certificate?",
                ],
            )
        )

        # -------------------------------------------------------------
        # 2. Cinematography & Drone Quotation Analysis
        # -------------------------------------------------------------
        photo_a = VendorQuote(
            vendor_id="photo_vendor_01",
            vendor_name="Lumière Heritage Studio",
            category="Photography",
            base_quote=85000.0,
            tax_and_fees=15300.0,
            total_cost=100300.0,
            per_plate_or_unit=None,
            inclusions=[
                "2 Traditional Photographers + 1 Candid Specialist",
                "1 Drone 4K Operator for outdoor baraat",
                "3-minute Cinematic Highlight Teaser Reel",
                "All unedited RAW images provided within 48 hours",
            ],
            exclusions=[
                "Printed hardbound coffee table album (+₹18,000)",
                "Same-day teaser edit for social media (+₹10,000)",
            ],
            hidden_costs_flagged=[
                "Travel & hotel stay reimbursement mandatory if outside Delhi NCR",
                "Extra fee if drone flying requires special local police permissions",
            ],
            verified=True,
        )

        photo_b = VendorQuote(
            vendor_id="photo_vendor_02",
            vendor_name="Katha Moments Visuals",
            category="Photography",
            base_quote=68000.0,
            tax_and_fees=0.0, # Inclusive
            total_cost=68000.0,
            per_plate_or_unit=None,
            inclusions=[
                "2 Candid Photographers + 1 Cinematographer",
                "1 Premium 40-page Hardbound Leather Album included",
                "Instagram Reels vertical cut delivered within 24 hours",
                "Covers up to 10 hours of shoot",
            ],
            exclusions=[
                "Drone aerial filming (+₹12,000)",
                "Pre-wedding studio portrait shoot",
            ],
            hidden_costs_flagged=[
                "Overtime charged at ₹4,000 per hour beyond 10-hour mark",
            ],
            verified=True,
        )

        comparisons.append(
            VendorComparison(
                category="Photography & Media",
                quotes=[photo_a, photo_b],
                recommended_vendor_id="photo_vendor_02",
                key_trade_offs=[
                    "Katha Moments includes the physical album and 24h social reel at ₹68,000 flat.",
                    "Lumière includes drone aerials but album is an extra ₹18,000.",
                ],
                negotiation_questions=[
                    "Will the same senior cinematographers shown in the portfolio personally shoot our event?",
                    "What is the exact penalty clause if the final video is delayed past 45 days?",
                    "Can you bundle the drone operator at a 50% discount if we book this week?",
                ],
            )
        )

        return comparisons
