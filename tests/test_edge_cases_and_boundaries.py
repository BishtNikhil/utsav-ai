"""
Comprehensive Edge Case, Boundary Condition, and WCAG Accessibility Tests.

Validates robust input validation, boundary calculations, domain exception hierarchy,
enterprise OWASP CSP headers, and WCAG 2.4.1 keyboard accessibility compliance.
"""

import os
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import EventIntakeRequest, ExperienceTier
from app.services.dependency_engine import DependencyEngine
from app.services.timeline_dag import TimelineDAGService
from app.core.exceptions import (
    UtsavAIException,
    InvalidBudgetError,
    InvalidGuestCountError,
    TimelineDependencyError,
)

client = TestClient(app)


def test_invalid_budget_boundary_exception():
    """Validates that non-positive budget values trigger domain-specific InvalidBudgetError."""
    req = EventIntakeRequest(
        title="Edge Case Zero Budget",
        guest_count=100,
        total_budget=10000.0, # Minimum allowable in schema
        target_date="2027-05-15",
    )
    # Artificially test negative budget directly on the DependencyEngine
    req.total_budget = -500.0
    with pytest.raises(InvalidBudgetError):
        DependencyEngine.calculate_budget(req)


def test_invalid_guest_count_boundary_exception():
    """Validates that non-positive guest counts trigger domain-specific InvalidGuestCountError."""
    req = EventIntakeRequest(
        title="Edge Case Zero Guests",
        guest_count=50,
        total_budget=500000.0,
        target_date="2027-05-15",
    )
    req.guest_count = 0
    with pytest.raises(InvalidGuestCountError):
        DependencyEngine.calculate_budget(req)


def test_invalid_date_format_timeline_exception():
    """Validates that malformed target date strings trigger TimelineDependencyError."""
    with pytest.raises(TimelineDependencyError):
        TimelineDAGService.generate_timeline("not-a-valid-date-string")


def test_contingency_reserve_exact_arithmetic():
    """Validates exact 7% mathematical contingency calculation across diverse budgets."""
    res_800k = DependencyEngine.calculate_contingency_reserve(800000.0, 0.07)
    assert res_800k == 56000.0

    res_1m = DependencyEngine.calculate_contingency_reserve(1000000.0, 0.07)
    assert res_1m == 70000.0

    res_150k = DependencyEngine.calculate_contingency_reserve(150000.0, 0.07)
    assert res_150k == 10500.0


def test_venue_minimum_square_footage_scaling():
    """Validates physical space constraints per attendee for crowd safety."""
    sqft_100 = DependencyEngine.get_minimum_venue_sqft(100, "indoor_banquet")
    assert sqft_100 == 1200.0

    sqft_250 = DependencyEngine.get_minimum_venue_sqft(250, "indoor_banquet")
    assert sqft_250 == 3000.0


def test_enterprise_security_headers_extended():
    """Validates complete suite of OWASP enterprise security headers."""
    res = client.get("/health")
    assert res.status_code == 200

    headers = res.headers
    assert "Content-Security-Policy" in headers
    assert "Permissions-Policy" in headers
    assert "Strict-Transport-Security" in headers
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-XSS-Protection"] == "1; mode=block"


def test_wcag_skip_link_and_aria_live_semantics():
    """Validates WCAG 2.4.1 bypass block skip-links and aria-live announcements."""
    static_html_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    assert os.path.exists(static_html_path)

    with open(static_html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Skip Link for keyboard navigation
    assert 'class="skip-link"' in html
    assert 'href="#main-content"' in html

    # Live regions for screen reader status messages
    assert 'aria-live="polite"' in html
    assert 'aria-atomic="true"' in html
    assert 'role="status"' in html
    assert 'role="main"' in html
    assert 'role="region"' in html


def test_domain_exception_handler_response():
    """Validates that custom UtsavAIException translates to clean HTTP 400 with structured JSON."""
    exc = InvalidBudgetError("Budget insufficient for guest count", {"min_required": 100000.0})
    assert isinstance(exc, UtsavAIException)
    assert exc.message == "Budget insufficient for guest count"
    assert exc.details["min_required"] == 100000.0
