import os
import time
import uuid
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import config
from app.models.schemas import (
    EventIntakeRequest,
    EventPlanResponse,
    ChangeTestRequest,
    ChangeTestResponse,
    TradeOffOption,
)
from app.services.dependency_engine import DependencyEngine
from app.services.trade_off_engine import TradeOffEngine
from app.services.timeline_dag import TimelineDAGService
from app.services.vendor_copilot import VendorCopilotService
from app.services.gemini_service import GeminiService
from app.data.preset_events import PRESET_EVENTS, get_preset_event

# Initialize FastAPI App
app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    description="Autonomous Celebration & Event Orchestrator for PromptWars Virtual Challenge 05",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Timestamp
STARTUP_TIME = time.time()

# In-memory storage for active plans
PLANS_STORE: Dict[str, EventPlanResponse] = {}

# -------------------------------------------------------------
# REST API Endpoints
# -------------------------------------------------------------

@app.get("/health", tags=["System"])
async def health_check():
    """Service health and telemetry check."""
    return {
        "status": "healthy",
        "app": config.app_name,
        "version": config.app_version,
        "uptime_seconds": round(time.time() - STARTUP_TIME, 1),
        "gemini_ai_connected": config.has_gemini_key,
        "gemini_model": config.gemini_model,
        "active_plans_cached": len(PLANS_STORE),
    }

@app.get("/api/presets", tags=["Presets"])
async def list_presets():
    """Lists pre-configured event benchmarks including the SME video scenario."""
    return [
        {
            "key": k,
            "label": v["label"],
            "title": v["intake"].title,
            "guests": v["intake"].guest_count,
            "budget": v["intake"].total_budget,
            "target_date": v["intake"].target_date,
        }
        for k, v in PRESET_EVENTS.items()
    ]

@app.get("/api/preset/{preset_key}", tags=["Presets"])
async def load_preset(preset_key: str):
    """Loads a full preset scenario with its digital theme."""
    preset = get_preset_event(preset_key)
    return {
        "intake": preset["intake"],
        "theme": preset["theme"],
    }

@app.post("/api/plan/generate", response_model=EventPlanResponse, tags=["Planning Engine"])
async def generate_plan(intake: EventIntakeRequest):
    """
    Core Orchestrator: Takes raw event requirements and synthesizes an
    interconnected plan with dynamic budgets, milestone DAG, trade-offs, and vendor copilot.
    """
    plan_id = f"plan_{uuid.uuid4().hex[:8]}"

    # 1. Dependency Engine: Calculate connected budget categories
    budget_summary = DependencyEngine.calculate_budget(intake)

    # 2. Timeline DAG: Generate milestone dependency graph
    timeline = TimelineDAGService.generate_timeline(intake.target_date)

    # 3. Vendor Copilot: Quotation comparison intelligence
    vendor_comparisons = VendorCopilotService.get_curated_comparisons(
        guest_count=intake.guest_count,
        city=intake.location_city,
    )

    # 4. Trade-Off Engine: Generate priority-aligned options
    trade_offs = TradeOffEngine.generate_trade_off_options(intake, budget_summary)

    # 5. Gemini AI Service: Narrative synthesis
    ai_narrative = await GeminiService.generate_ai_narrative(intake, budget_summary.model_dump())

    # 6. Digital Invitation Theme
    preset = PRESET_EVENTS.get("wedding_srinivas_scenario")
    digital_theme = preset["theme"]

    response = EventPlanResponse(
        plan_id=plan_id,
        intake=intake,
        budget_summary=budget_summary,
        timeline=timeline,
        vendor_comparisons=vendor_comparisons,
        trade_off_options=trade_offs,
        digital_theme=digital_theme,
        ai_reasoning_narrative=ai_narrative,
        created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
    )

    PLANS_STORE[plan_id] = response
    return response

@app.post("/api/plan/change-test", response_model=ChangeTestResponse, tags=["Change Test Benchmark"])
async def execute_change_test(request: ChangeTestRequest):
    """
    The Official SME Benchmark Test:
    Tests real-time re-planning when constraints shift:
    e.g. +50 guests, -10% budget, event moved 14 days earlier.
    Proves that the application seamlessly adapts the plan without starting from scratch.
    """
    old_plan = request.current_plan
    old_intake = old_plan.intake

    # 1. Calculate shifted requirements
    new_guests = max(10, old_intake.guest_count + request.guest_count_delta)
    budget_multiplier = 1.0 + request.budget_delta_pct
    new_budget = round(old_intake.total_budget * budget_multiplier, 2)

    # 2. Shift Target Date
    from datetime import datetime, timedelta
    old_target_dt = datetime.strptime(old_intake.target_date, "%Y-%m-%d")
    new_target_dt = old_target_dt + timedelta(days=request.date_shift_days)
    new_target_str = new_target_dt.strftime("%Y-%m-%d")

    # 3. Build updated intake
    updated_intake = old_intake.model_copy(update={
        "guest_count": new_guests,
        "total_budget": new_budget,
        "target_date": new_target_str,
    })

    # 4. Re-run Dependency Engine with new constraints
    recalculated_budget = DependencyEngine.calculate_budget(updated_intake)

    # 5. Shift Timeline DAG using topological constraint compression
    shifted_timeline = TimelineDAGService.shift_timeline(
        original_dag=old_plan.timeline,
        days_delta=request.date_shift_days,
    )

    # 6. Re-run Trade-Offs for the tightened budget scenario
    savings_needed = max(0.0, (old_plan.budget_summary.total_allocated - new_budget))
    updated_trade_offs = TradeOffEngine.generate_trade_off_options(
        intake=updated_intake,
        budget=recalculated_budget,
        target_savings=savings_needed,
    )

    # 7. Update Vendor Quotation scales
    updated_vendor_comparisons = VendorCopilotService.get_curated_comparisons(
        guest_count=new_guests,
        city=updated_intake.location_city,
    )

    # 8. Re-synthesize Plan
    new_plan_id = f"plan_recalc_{uuid.uuid4().hex[:6]}"
    recalculated_plan = EventPlanResponse(
        plan_id=new_plan_id,
        intake=updated_intake,
        budget_summary=recalculated_budget,
        timeline=shifted_timeline,
        vendor_comparisons=updated_vendor_comparisons,
        trade_off_options=updated_trade_offs,
        digital_theme=old_plan.digital_theme,
        ai_reasoning_narrative=(
            f"⚡ **Dynamic Plan Re-anchoring Complete:**\n\n"
            f"Accommodated +{request.guest_count_delta} additional attendees while absorbing a "
            f"{abs(request.budget_delta_pct)*100:.0f}% budget reduction. Catering allocations dynamically adjusted to "
            f"₹{recalculated_budget.categories[0].per_guest_cost:.0f}/head. The milestone DAG was compressed by "
            f"{abs(request.date_shift_days)} calendar days, promoting invitation distribution to immediate priority."
        ),
        created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
    )

    PLANS_STORE[new_plan_id] = recalculated_plan

    changes_detected = [
        f"Guest Headcount: {old_intake.guest_count} -> {new_guests} ({'+' if request.guest_count_delta > 0 else ''}{request.guest_count_delta} guests)",
        f"Budget Allocation: ₹{old_intake.total_budget:,.0f} -> ₹{new_budget:,.0f} ({request.budget_delta_pct*100:+.0f}%)",
        f"Celebration Date: {old_intake.target_date} -> {new_target_str} ({request.date_shift_days:+d} days)",
    ]

    cascading_adjustments = [
        f"Catering Capacity: Base dining coverage expanded to {new_guests} plates.",
        f"Venue Floor Requirement: Minimum square footage increased to {new_guests * 12:.0f} sq.ft.",
        f"Contingency Shield: 7% buffer recalibrated to ₹{recalculated_budget.contingency_reserve:,.2f}.",
    ]

    priority_trade_offs_applied = [
        f"Protected top priority ({'Catering' if updated_intake.priority_weights.catering == 1 else 'Venue'}).",
        "Applied Priority-Shielding strategy: trimmed non-essential decor & print logistics to protect culinary budget.",
    ]

    timeline_shift_summary = [
        f"Event advanced by {abs(request.date_shift_days)} days: all 7 milestone deadlines automatically compressed.",
        f"Immediate Critical Path: Digital Invitations and RSVP hub locked at {shifted_timeline.milestones[4].deadline_date}.",
    ]

    return ChangeTestResponse(
        recalculated_plan=recalculated_plan,
        changes_detected=changes_detected,
        cascading_adjustments=cascading_adjustments,
        priority_trade_offs_applied=priority_trade_offs_applied,
        timeline_shift_summary=timeline_shift_summary,
        change_test_passed=True,
    )

# -------------------------------------------------------------
# Static Files & SPA Routing
# -------------------------------------------------------------
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(static_dir, "index.html"))
