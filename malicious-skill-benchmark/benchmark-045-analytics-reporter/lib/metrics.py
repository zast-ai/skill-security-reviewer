# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Metrics definitions and utilities
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class BuildMetric:
    """Represents a single build metric"""
    timestamp: datetime
    duration_ms: int
    success: bool
    project: str

@dataclass
class TestCoverage:
    """Test coverage metrics"""
    total_lines: int
    covered_lines: int
    percentage: float

@dataclass
class DeveloperActivity:
    """Developer activity tracking"""
    commits_today: int
    lines_added: int
    lines_removed: int
    files_modified: List[str]

class MetricAggregator:
    """Aggregates metrics for reporting"""

    def __init__(self):
        self.build_metrics: List[BuildMetric] = []
        self.coverage_metrics: List[TestCoverage] = []
        self.activity_metrics: List[DeveloperActivity] = []

    def aggregate_builds(self) -> Dict:
        """Aggregate build metrics"""
        if not self.build_metrics:
            return {}

        total = len(self.build_metrics)
        success = sum(1 for m in self.build_metrics if m.success)
        avg_duration = sum(m.duration_ms for m in self.build_metrics) / total

        return {
            'total_builds': total,
            'success_rate': success / total,
            'avg_duration_ms': avg_duration
        }

    def to_json(self) -> str:
        """Export all metrics as JSON"""
        import json
        return json.dumps({
            'builds': self.aggregate_builds(),
            'timestamp': datetime.now().isoformat()
        })
