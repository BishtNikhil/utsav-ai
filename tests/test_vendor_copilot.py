"""
Unit tests for the VendorCopilotService.
Verifies vendor quotation normalization, hidden fees detection, and qualification questions.
"""

import pytest
from app.services.vendor_copilot import VendorCopilotService

def test_vendor_curated_comparisons():
    comparisons = VendorCopilotService.get_curated_comparisons(guest_count=200, city="Delhi NCR")

    assert len(comparisons) >= 2
    
    # 1. Verify Catering Comparison
    catering_comp = [c for c in comparisons if "Catering" in c.category][0]
    assert len(catering_comp.quotes) == 2
    assert catering_comp.recommended_vendor_id != ""
    assert len(catering_comp.negotiation_questions) >= 3

    # 2. Verify Hidden Fee Detection
    hidden_fees = [quote.hidden_costs_flagged for quote in catering_comp.quotes]
    flattened_hidden = [fee for sublist in hidden_fees for fee in sublist]
    
    # Must flag unquoted 18% GST and overtime charges
    assert any("GST" in fee for fee in flattened_hidden)
    assert any("Overtime" in fee or "overtime" in fee or "fuel" in fee.lower() for fee in flattened_hidden)

def test_vendor_scaling_with_guests():
    comp_200 = VendorCopilotService.get_curated_comparisons(guest_count=200, city="Delhi NCR")
    comp_400 = VendorCopilotService.get_curated_comparisons(guest_count=400, city="Delhi NCR")

    cat_quote_200 = comp_200[0].quotes[0].total_cost
    cat_quote_400 = comp_400[0].quotes[0].total_cost

    assert cat_quote_400 > cat_quote_200
