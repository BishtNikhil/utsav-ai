import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import EventIntakeRequest, ChangeTestRequest

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_presets_endpoints():
    res = client.get("/api/presets")
    assert res.status_code == 200
    presets = res.json()
    assert len(presets) >= 3

    # Load specific preset
    res_single = client.get("/api/preset/wedding_srinivas_scenario")
    assert res_single.status_code == 200
    assert "intake" in res_single.json()

def test_plan_generate_endpoint():
    payload = {
        "title": "Test FastAPI Vivah",
        "category": "wedding",
        "guest_count": 180,
        "total_budget": 750000.0,
        "target_date": "2027-03-31",
        "location_city": "Delhi NCR",
        "experience_tier": "standard",
        "priority_weights": {
            "catering": 1,
            "venue": 2,
            "decor": 3,
            "photography": 4,
            "entertainment": 5
        },
        "must_haves": ["Organic Food", "Live Acoustic Music"],
        "special_notes": "Automated testing plan."
    }

    res = client.post("/api/plan/generate", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["plan_id"].startswith("plan_")
    assert len(data["budget_summary"]["categories"]) == 5
    assert len(data["timeline"]["milestones"]) == 7
    assert len(data["trade_off_options"]) == 3
    assert len(data["vendor_comparisons"]) >= 2
    assert "ai_reasoning_narrative" in data

def test_change_test_benchmark_endpoint():
    # 1. Generate baseline plan
    intake_payload = {
        "title": "Benchmark Vivah",
        "category": "wedding",
        "guest_count": 200,
        "total_budget": 800000.0,
        "target_date": "2027-02-28",
        "location_city": "Delhi NCR",
        "experience_tier": "standard",
        "priority_weights": {"catering": 1, "venue": 2, "decor": 3, "photography": 4, "entertainment": 5},
        "must_haves": ["Authentic Food"],
        "special_notes": "Testing Change Test."
    }
    plan_res = client.post("/api/plan/generate", json=intake_payload)
    plan_data = plan_res.json()

    # 2. Trigger Change Test (+50 guests, -10% budget, -14 days date shift)
    change_payload = {
        "current_plan": plan_data,
        "guest_count_delta": 50,
        "budget_delta_pct": -0.10,
        "date_shift_days": -14,
        "user_instruction": "50 more guests added, budget cut by 10%, event moved 2 weeks earlier."
    }

    res = client.post("/api/plan/change-test", json=change_payload)
    assert res.status_code == 200
    change_data = res.json()

    assert change_data["change_test_passed"] is True
    assert len(change_data["changes_detected"]) >= 3
    assert len(change_data["cascading_adjustments"]) >= 3

    # Verify recalculated values
    recalculated_plan = change_data["recalculated_plan"]
    assert recalculated_plan["intake"]["guest_count"] == 250
    assert recalculated_plan["intake"]["total_budget"] == 720000.0
