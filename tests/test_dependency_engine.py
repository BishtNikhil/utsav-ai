import pytest
from app.models.schemas import EventIntakeRequest, EventCategory, ExperienceTier, PriorityRanking
from app.services.dependency_engine import DependencyEngine

def test_budget_calculation_balance():
    intake = EventIntakeRequest(
        title="Test Royal Wedding",
        category=EventCategory.WEDDING,
        guest_count=200,
        total_budget=800000.0,
        target_date="2027-02-28",
        experience_tier=ExperienceTier.STANDARD,
        priority_weights=PriorityRanking(catering=1, venue=2, decor=3, photography=4, entertainment=5),
    )

    summary = DependencyEngine.calculate_budget(intake)

    assert summary.total_budget == 800000.0
    assert summary.contingency_reserve > 0
    assert summary.is_balanced is True
    assert len(summary.categories) == 5

    # Catering should have the highest allocation because it's Priority #1
    catering_cat = [c for c in summary.categories if c.category_id == "cat_catering"][0]
    decor_cat = [c for c in summary.categories if c.category_id == "cat_decor"][0]
    assert catering_cat.allocated_amount > decor_cat.allocated_amount

def test_guest_count_scaling():
    intake_small = EventIntakeRequest(
        title="Small Gathering",
        category=EventCategory.BIRTHDAY,
        guest_count=50,
        total_budget=200000.0,
        target_date="2027-03-15",
    )
    intake_large = EventIntakeRequest(
        title="Large Gathering",
        category=EventCategory.BIRTHDAY,
        guest_count=250,
        total_budget=500000.0,
        target_date="2027-03-15",
    )

    summary_small = DependencyEngine.calculate_budget(intake_small)
    summary_large = DependencyEngine.calculate_budget(intake_large)

    catering_small = [c for c in summary_small.categories if c.category_id == "cat_catering"][0]
    catering_large = [c for c in summary_large.categories if c.category_id == "cat_catering"][0]

    assert catering_large.allocated_amount > catering_small.allocated_amount
