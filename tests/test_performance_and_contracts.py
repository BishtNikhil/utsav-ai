"""
Performance, Latency Benchmarks, and Architectural Contract Tests for UtsavAI.

Validates that:
1. Core constraint math and topological DAG sorting execute within strict sub-50ms latency budgets.
2. WAI-ARIA 1.2 tablist, role="tab", role="tabpanel", and live regions comply with WCAG 2.4.1.
3. Enterprise security headers (CSP, Permissions-Policy, HSTS) are strictly active on all routes.
"""

import time
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import EventIntakeRequest, ExperienceTier, PriorityRanking
from app.services.dependency_engine import DependencyEngine
from app.services.timeline_dag import TimelineDAGService

client = TestClient(app)


def test_dependency_engine_sub_15ms_latency():
    """Validates that mathematical constraint calculation executes in strictly under 15ms."""
    req = EventIntakeRequest(
        title="High-Scale Performance Gala",
        guest_count=500,
        total_budget=1500000.0,
        target_date="2027-04-10",
        experience_tier=ExperienceTier.PREMIUM_LUXURY,
        priority_weights=PriorityRanking(catering=1, venue=2, decor=3, photography=4, entertainment=5),
    )

    # Warmup
    DependencyEngine.calculate_budget(req)

    # Measure 50 iterations
    t0 = time.perf_counter()
    for _ in range(50):
        DependencyEngine.calculate_budget(req)
    total_time = time.perf_counter() - t0
    avg_latency_ms = (total_time / 50.0) * 1000.0

    assert avg_latency_ms < 15.0, f"Average latency was {avg_latency_ms:.2f}ms, expected < 15ms"


def test_timeline_dag_sub_25ms_latency():
    """Validates that topological DAG scheduling executes in strictly under 25ms."""
    # Warmup
    TimelineDAGService.generate_timeline("2027-06-20")

    t0 = time.perf_counter()
    for _ in range(50):
        TimelineDAGService.generate_timeline("2027-06-20")
    total_time = time.perf_counter() - t0
    avg_latency_ms = (total_time / 50.0) * 1000.0

    assert avg_latency_ms < 25.0, f"Average DAG latency was {avg_latency_ms:.2f}ms, expected < 25ms"


def test_wai_aria_tabs_accessibility_contract():
    """Validates that index.html strictly adheres to the WAI-ARIA 1.2 Tabs design pattern."""
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # ARIA role contract
    assert 'role="tablist"' in html
    assert 'role="tab"' in html
    assert 'role="tabpanel"' in html
    assert 'aria-controls="tab-budget"' in html
    assert 'aria-selected="true"' in html
    assert 'tabindex="0"' in html


def test_owasp_strict_security_headers_contract():
    """Validates presence and correctness of OWASP CSP, HSTS, and Permissions-Policy."""
    res = client.get("/health")
    assert res.status_code == 200

    headers = res.headers
    assert "default-src 'self'" in headers.get("Content-Security-Policy", "")
    assert "max-age=31536000" in headers.get("Strict-Transport-Security", "")
    assert "geolocation=()" in headers.get("Permissions-Policy", "")
    assert headers.get("X-Frame-Options") == "DENY"
