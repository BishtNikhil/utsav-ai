"""
UtsavAI Domain Exception Hierarchy.

Provides domain-specific exceptions for constraint checking, budget allocations,
milestone DAG dependency validation, and vendor quotation analysis.
"""

from typing import Optional, Dict, Any


class UtsavAIException(Exception):
    """Base exception for all domain errors within UtsavAI."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConstraintViolationError(UtsavAIException):
    """Raised when an event intake constraint is violated or physically unachievable."""
    pass


class InvalidBudgetError(ConstraintViolationError):
    """Raised when total allocated budget is insufficient for baseline guest hospitality."""
    pass


class InvalidGuestCountError(ConstraintViolationError):
    """Raised when guest count falls outside allowable physical venue bounds."""
    pass


class TimelineDependencyError(UtsavAIException):
    """Raised when milestone dependency cycles or invalid prerequisite orders occur."""
    pass


class VendorQuotationError(UtsavAIException):
    """Raised when vendor quotations contain missing disclosures or computational errors."""
    pass
