"""
UtsavAI Data Models and Schemas.

Defines Pydantic v2 data models for event intake, dynamic budget summaries,
milestone DAG networks, vendor quotation intelligence, and the SME Change Test.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class EventCategory(str, Enum):
    """Supported celebration and event archetypes."""
    WEDDING = "wedding"
    BIRTHDAY = "birthday"
    COMMUNITY_GALA = "community_gala"
    CORPORATE_FESTIVAL = "corporate_festival"
    ANNIVERSARY = "anniversary"

class ExperienceTier(str, Enum):
    """Quality and hospitality execution tiers."""
    ESSENTIAL = "essential"
    STANDARD = "standard"
    PREMIUM_LUXURY = "premium_luxury"

class PriorityRanking(BaseModel):
    """
    User-defined priority hierarchy (1 = highest protection, 5 = lowest).
    Directly guides the Trade-Off Engine during budget cuts or overruns.
    """
    catering: int = Field(default=1, ge=1, le=5, description="Priority rank (1=highest, 5=lowest)")
    venue: int = Field(default=2, ge=1, le=5, description="Priority rank (1=highest, 5=lowest)")
    decor: int = Field(default=3, ge=1, le=5, description="Priority rank (1=highest, 5=lowest)")
    photography: int = Field(default=4, ge=1, le=5, description="Priority rank (1=highest, 5=lowest)")
    entertainment: int = Field(default=5, ge=1, le=5, description="Priority rank (1=highest, 5=lowest)")

class EventIntakeRequest(BaseModel):
    """
    Primary user intake payload capturing event constraints and priorities.
    """
    title: str = Field(..., json_schema_extra={"example": "Saurav & Saumya Royal Vivah"})
    category: EventCategory = Field(default=EventCategory.WEDDING)
    guest_count: int = Field(..., ge=10, le=10000, json_schema_extra={"example": 200})
    total_budget: float = Field(..., ge=10000, description="Total budget in INR", json_schema_extra={"example": 800000.0})
    target_date: str = Field(..., description="Target date in YYYY-MM-DD", json_schema_extra={"example": "2027-02-28"})
    location_city: str = Field(default="Nainital / Delhi NCR", json_schema_extra={"example": "Delhi NCR"})
    experience_tier: ExperienceTier = Field(default=ExperienceTier.STANDARD)
    priority_weights: PriorityRanking = Field(default_factory=PriorityRanking)
    must_haves: List[str] = Field(default_factory=lambda: ["Gourmet Himalayan Dining", "Live Shehnai / Acoustic Music"])
    special_notes: Optional[str] = Field(default="Intimate family celebration with deep cultural aesthetics.")

class BudgetCategory(BaseModel):
    """
    Itemized budget allocation with transparent estimation labels.
    """
    category_id: str
    category_name: str
    allocated_amount: float
    percentage_of_budget: float
    is_confirmed: bool = False
    status_label: str = "Estimated Assumption"
    per_guest_cost: Optional[float] = None
    sub_items: List[Dict[str, float]] = Field(default_factory=list)
    trade_off_flexibility: str = "Medium"

class BudgetSummary(BaseModel):
    """
    Synthesized high-level financial health statement.
    """
    total_budget: float
    total_allocated: float
    contingency_reserve: float
    remaining_balance: float
    categories: List[BudgetCategory]
    is_balanced: bool

class Milestone(BaseModel):
    """
    Milestone node in the Timeline Directed Acyclic Graph (DAG).
    """
    milestone_id: str
    title: str
    category: str
    deadline_date: str
    days_before_event: int
    is_critical_path: bool = False
    status: str = "pending" # pending, in_progress, completed, delayed
    dependencies: List[str] = Field(default_factory=list, description="IDs of prerequisite milestones")
    description: str
    contingency_action: str

class TimelineDAG(BaseModel):
    """
    Complete Directed Acyclic Graph representing the event timeline.
    """
    target_date: str
    total_milestones: int
    critical_path_milestones: List[str]
    milestones: List[Milestone]

class TradeOffOption(BaseModel):
    """
    Actionable trade-off scenario generated during budget constraints.
    """
    option_id: str
    title: str
    scenario_description: str
    cost_delta: float
    pros: List[str]
    cons: List[str]
    alignment_score: float = Field(default=0.9, ge=0.0, le=1.0)
    recommended: bool = False

class VendorQuote(BaseModel):
    """
    Normalized vendor proposal with hidden fees flagged.
    """
    vendor_id: str
    vendor_name: str
    category: str
    base_quote: float
    tax_and_fees: float
    total_cost: float
    per_plate_or_unit: Optional[float] = None
    inclusions: List[str]
    exclusions: List[str]
    hidden_costs_flagged: List[str]
    verified: bool = False

class VendorComparison(BaseModel):
    """
    Side-by-side comparative analysis of competing vendors.
    """
    category: str
    quotes: List[VendorQuote]
    recommended_vendor_id: str
    key_trade_offs: List[str]
    negotiation_questions: List[str]

class CeremonyScheduleItem(BaseModel):
    """
    Schedule item for multi-day celebration sequences.
    """
    ceremony_name: str
    date_label: str
    time_window: str
    venue_type: str
    dress_code: str
    music_vibe: str
    key_highlights: List[str]

class DigitalInvitationTheme(BaseModel):
    """
    Aesthetic styling, color palette, and audio mood for invitations.
    """
    theme_name: str
    aesthetic_style: str
    palette: Dict[str, str]
    typography_heading: str
    typography_body: str
    ambient_audio_track: str
    ceremonies: List[CeremonyScheduleItem]
    rsvp_link_slug: str

class EventPlanResponse(BaseModel):
    """
    Complete synthesized event architecture response.
    """
    plan_id: str
    intake: EventIntakeRequest
    budget_summary: BudgetSummary
    timeline: TimelineDAG
    vendor_comparisons: List[VendorComparison]
    trade_off_options: List[TradeOffOption]
    digital_theme: DigitalInvitationTheme
    ai_reasoning_narrative: str
    created_at: str

class ChangeTestRequest(BaseModel):
    """
    Payload for the official SME Change Test benchmark.
    """
    current_plan: EventPlanResponse
    guest_count_delta: int = Field(default=50, description="+50 or -30 guests", json_schema_extra={"example": 50})
    budget_delta_pct: float = Field(default=-0.10, description="-0.10 means 10% budget cut", json_schema_extra={"example": -0.10})
    date_shift_days: int = Field(default=-14, description="-14 means 2 weeks earlier", json_schema_extra={"example": -14})
    user_instruction: Optional[str] = Field(default="50 more guests added, budget cut by 10%, event moved 2 weeks earlier.")

class ChangeTestResponse(BaseModel):
    """
    Re-anchored plan response proving dynamic adaptation without restarting.
    """
    recalculated_plan: EventPlanResponse
    changes_detected: List[str]
    cascading_adjustments: List[str]
    priority_trade_offs_applied: List[str]
    timeline_shift_summary: List[str]
    change_test_passed: bool = True
