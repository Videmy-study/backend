#!/usr/bin/env python3
"""Simple test script to verify imports work correctly."""

import sys
from pathlib import Path

# Add parent directories to path
current_dir = Path(__file__).parent
backend_dir = current_dir.parent
academic_research_path = backend_dir / "academic-research"
fomc_research_path = backend_dir / "fomc-research"

print("🔍 Testing imports...")
print(f"Current directory: {current_dir}")
print(f"Backend directory: {backend_dir}")
print(f"Academic research path: {academic_research_path}")
print(f"FOMC research path: {fomc_research_path}")

# Add paths to sys.path
if academic_research_path.exists():
    sys.path.insert(0, str(academic_research_path))
    print("✅ Added academic-research to sys.path")
else:
    print("❌ academic-research path not found")

if fomc_research_path.exists():
    sys.path.insert(0, str(fomc_research_path))
    print("✅ Added fomc-research to sys.path")
else:
    print("❌ fomc-research path not found")

print("\n🧪 Testing imports...")

# Test academic research import
try:
    from academic_research import academic_coordinator
    print("✅ Successfully imported academic_coordinator")
    print(f"   Name: {academic_coordinator.name}")
    print(f"   Description: {academic_coordinator.description}")
except ImportError as e:
    print(f"❌ Failed to import academic_coordinator: {e}")

# Test FOMC research import
try:
    from fomc_research import root_agent
    print("✅ Successfully imported root_agent")
    print(f"   Name: {root_agent.name}")
    print(f"   Description: {root_agent.description}")
except ImportError as e:
    print(f"❌ Failed to import root_agent: {e}")

print("\n✅ Import test completed!") 