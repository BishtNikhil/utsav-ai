import pytest
from app.models.schemas import EventIntakeRequest, PriorityRanking
from app.services.dependency_engine import DependencyEngine
from app.services.trade_off_engine import TradeOffEngine

def test_trade_off_generation():
    intake = EventIntakeRequest(
        title="Test Celebration",
        guest_count=200,
        total_budget=800000.0,
        target_date="2027-02-28",
        priority_weights=PriorityRanking(catering=1, venue=2, decor=4, photography=3, entertainment=5),
    )
    budget = DependencyEngine.calculate_budget(intake)
    options = TradeOffEngine.generate_trade_off_options(intake, budget, target_savings=100000.0)

    assert len(options) == 3
    # Exactly one option should be recommended
    recommended_opts = [o for o in options if o.recommended]
    assert len(recommended_opts) == 1
    # Savings should be positive savings (negative cost delta)
    for opt in options:
        assert opt.cost_delta < 0
        assert len(opt.pros) > 0
        assert len(opt.cons) > 0
