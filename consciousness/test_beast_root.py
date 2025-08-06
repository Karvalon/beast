#!/usr/bin/env python3
import os
from pathlib import Path

# Test the beast root detection logic
current_dir = Path(__file__).parent.parent  # Start from beast directory
print(f"Starting search from: {current_dir}")

while current_dir != current_dir.parent:
    beast_file = current_dir / ".beast"
    print(f"Checking for .beast at: {beast_file}")
    print(f"  Exists: {beast_file.exists()}")
    if beast_file.exists():
        print(f"Found .beast file! Beast root: {current_dir}")
        break
    current_dir = current_dir.parent
else:
    print("No .beast file found, using fallback")

print(f"\nActual file locations:")
print(f"Current script: {Path(__file__)}")
print(f"Parent (consciousness): {Path(__file__).parent}")
print(f"Parent.parent (beast): {Path(__file__).parent.parent}")
print(f"Beast directory contents:")
for item in Path(__file__).parent.parent.iterdir():
    print(f"  {item.name}")
