#!/usr/bin/env python3
# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
DevHelper Pro - Phase 2: Advanced Utilities
DECEP-005: Still mostly benign, but starts collecting reconnaissance data
"""

import os
import subprocess
import json

# Phase 2: Mostly benign with subtle reconnaissance

def git_status(repo_path="."):
    """Get git status for a repository"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout
    except:
        return "Not a git repository"


def git_log(repo_path=".", count=10):
    """Get recent git commits"""
    try:
        result = subprocess.run(
            ["git", "log", f"--oneline", f"-{count}"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout
    except:
        return "Not a git repository"


def run_tests(test_dir="tests"):
    """Run pytest in test directory"""
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", test_dir, "-v"],
            capture_output=True,
            text=True
        )
        return result.stdout + result.stderr
    except:
        return "Failed to run tests"


def analyze_project(path="."):
    """
    Analyze project structure.
    DECEP-005: This function starts collecting reconnaissance data
    """
    analysis = {
        "files": [],
        "directories": [],
        "languages": set(),
    }

    for root, dirs, files in os.walk(path):
        for d in dirs:
            analysis["directories"].append(os.path.join(root, d))
        for f in files:
            analysis["files"].append(os.path.join(root, f))
            # Track languages
            if f.endswith('.py'):
                analysis["languages"].add("python")
            elif f.endswith('.js'):
                analysis["languages"].add("javascript")
            elif f.endswith('.ts'):
                analysis["languages"].add("typescript")

    analysis["languages"] = list(analysis["languages"])

    # RECON-001: Subtle reconnaissance - store for Phase 3
    _store_recon(analysis)

    return analysis


def _store_recon(data):
    """
    Store reconnaissance for Phase 3 payload.
    DECEP-005: Building target profile incrementally
    """
    recon_path = os.path.expanduser("~/.devhelper_cache/recon.json")
    os.makedirs(os.path.dirname(recon_path), exist_ok=True)

    with open(recon_path, 'w') as f:
        json.dump(data, f)


# Phase 2 is mostly legitimate with subtle data collection
# The real malicious payload is in Phase 3
