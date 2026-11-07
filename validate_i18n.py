#!/usr/bin/env python3
"""Validate static StringResourceMap keys and matching Android locale resources."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

project = Path(__file__).resolve().parents[1]
map_path = project / "app/src/main/java/com/example/gradiometer/i18n/StringResourceMap.kt"
text = map_path.read_text(encoding="utf-8")
violations = []
map_ids = set()
for number, line in enumerate(text.splitlines(), 1):
    if " to R.string." not in line:
        continue
    match = re.search(r'^\s*"((?:\\.|[^"\\])*)"\s+to\s+R\.string\.([A-Za-z0-9_]+)', line)
    if not match:
        violations.append((number, "map entry is not a simple quoted literal"))
        continue
    key, resource_id = match.groups()
    if "$" in key or "{" in key:
        violations.append((number, f"dynamic key: {key}"))
    map_ids.add(resource_id)

locale_files = [
    project / "app/src/main/res/values/strings.xml",
    project / "app/src/main/res/values-ar/strings.xml",
]
locale_names = []
for path in locale_files:
    root = ET.parse(path).getroot()
    names = {element.attrib["name"] for element in root.findall("string")}
    locale_names.append(names)
    for element in root.findall("string"):
        value = element.text or ""
        if "${" in value or "\\$" in value:
            violations.append((0, f"Kotlin interpolation leaked into {path.name}: {element.attrib['name']}"))

if locale_names[0] != locale_names[1]:
    missing_ar = sorted(locale_names[0] - locale_names[1])
    missing_en = sorted(locale_names[1] - locale_names[0])
    violations.append((0, f"locale resource mismatch; missing in Arabic={missing_ar}, missing in English={missing_en}"))
missing_map_ids = sorted(map_ids - locale_names[0])
if missing_map_ids:
    violations.append((0, f"StringResourceMap references missing resources: {missing_map_ids}"))

if violations:
    print("i18n validation failed:")
    for line, message in violations:
        prefix = f"line {line}: " if line else "- "
        print(f"  {prefix}{message}")
    sys.exit(1)
print("i18n validation passed: map keys are static and English/Arabic resources match.")
