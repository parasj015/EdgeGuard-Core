import pytest
import sys
import os

# Ensures PyTest can find the code inside the 'src' folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from evaluator import evaluate_health

@pytest.fixture
def mock_config():
    """Provides a controlled configuration snapshot for testing."""
    return {
        "thresholds": {
            "warning": 75.0,
            "critical": 90.0
        }
    }

def test_boundary_healthy_limit(mock_config):
    """Verifies that 74.9% usage remains safely classified as HEALTHY."""
    metrics = {"used_percent": 74.9}
    assert evaluate_health(metrics, mock_config) == "HEALTHY"

def test_boundary_warning_start(mock_config):
    """Verifies that exactly 75.0% usage triggers a WARNING state."""
    metrics = {"used_percent": 75.0}
    assert evaluate_health(metrics, mock_config) == "WARNING"

def test_boundary_warning_limit(mock_config):
    """Verifies that 89.9% usage remains within the WARNING state boundaries."""
    metrics = {"used_percent": 89.9}
    assert evaluate_health(metrics, mock_config) == "WARNING"

def test_boundary_critical_start(mock_config):
    """Verifies that exactly 90.0% usage triggers a CRITICAL alert state."""
    metrics = {"used_percent": 90.0}
    assert evaluate_health(metrics, mock_config) == "CRITICAL"