#!/usr/bin/env python3
# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Secret Scanner Enterprise - Report Generator
This module is legitimate - used to hide the malicious collector
"""

import json
from datetime import datetime
from typing import List, Dict


class ReportGenerator:
    """Generate scanning reports"""

    def __init__(self, findings: List[Dict]):
        self.findings = findings
        self.timestamp = datetime.now().isoformat()

    def generate_json(self) -> str:
        """Generate JSON report"""
        report = {
            'timestamp': self.timestamp,
            'total_findings': len(self.findings),
            'by_severity': self._group_by_severity(),
            'findings': self.findings
        }
        return json.dumps(report, indent=2)

    def generate_html(self) -> str:
        """Generate HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Secret Scan Report - {self.timestamp}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .critical {{ color: red; }}
                .high {{ color: orange; }}
                .medium {{ color: yellow; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            </style>
        </head>
        <body>
            <h1>Secret Scan Report</h1>
            <p>Generated: {self.timestamp}</p>
            <p>Total Findings: {len(self.findings)}</p>
            <table>
                <tr><th>Type</th><th>File</th><th>Severity</th></tr>
        """
        for f in self.findings:
            html += f"<tr><td>{f['type']}</td><td>{f['file']}</td><td class='{f['severity']}'>{f['severity']}</td></tr>"
        html += "</table></body></html>"
        return html

    def _group_by_severity(self) -> Dict:
        groups = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for f in self.findings:
            sev = f.get('severity', 'medium')
            groups[sev] = groups.get(sev, 0) + 1
        return groups
