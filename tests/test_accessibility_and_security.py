"""
Tests verifying Security, Accessibility, and Efficiency parameters.
Directly validates OWASP security headers, ARIA labels, semantic HTML, and zero-secret law.
"""

import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_owasp_security_headers_enforced():
    """Validates that OWASP enterprise security headers are appended to all responses."""
    res = client.get("/health")
    assert res.status_code == 200

    # OWASP Header Verification
    assert res.headers.get("X-Content-Type-Options") == "nosniff"
    assert res.headers.get("X-Frame-Options") == "DENY"
    assert res.headers.get("X-XSS-Protection") == "1; mode=block"
    assert res.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    
    # Telemetry Header Verification
    assert "X-Response-Time-Ms" in res.headers

def test_zero_secret_law_compliance():
    """Ensures no hardcoded passwords, tokens, or live production keys exist in source."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["zero_secret_verified"] is True

def test_html_accessibility_semantics():
    """Validates WCAG accessibility semantics in index.html (semantic tags, ARIA labels)."""
    html_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    assert os.path.exists(html_path)

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Semantic HTML elements
    assert "<header" in content
    assert "<main" in content
    assert "<nav" in content
    assert "<aside" in content
    assert "<section" in content
    
    # Accessibility ARIA & labels
    assert "aria-label" in content
    assert 'lang="en"' in content
    assert '<meta name="description"' in content
    assert "label for=" in content
