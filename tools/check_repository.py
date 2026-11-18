#!/usr/bin/env python3
"""Check documentation and JSON/trace integrity, not runtime conformance.

No third-party dependencies. Documentation must be standalone: local links stay
inside this checkout, while external references use explicit URLs.
"""
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def headings(path):
    anchors, seen = set(), {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', path.read_text(), re.M):
        heading = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', heading)
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchors.add(slug if count == 0 else f'{slug}-{count}')
    return anchors


def main():
    failures = []
    links, json_files, active_cases = 0, 0, 0
    paths = sorted(p for p in ROOT.rglob('*') if p.is_file()
                   and not any(x.startswith('.') for x in p.relative_to(ROOT).parts))
    for path in paths:
        relative = str(path.relative_to(ROOT))
        if path.suffix == '.md':
            for match in re.finditer(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', path.read_text()):
                raw = match[1].strip().strip('<>')
                url = urlsplit(raw)
                if url.scheme or raw.startswith('//'):
                    continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                if not target.is_relative_to(ROOT):
                    failures.append(f'{relative}: external checkout dependency {raw}')
                    continue
                links += 1
                if not target.exists():
                    failures.append(f'{relative}: missing {raw}')
                elif url.fragment and target.suffix == '.md' and unquote(url.fragment) not in headings(target):
                    failures.append(f'{relative}: missing anchor {raw}')
        elif path.suffix == '.json':
            json_files += 1
            try:
                data = json.loads(path.read_text())
            except (ValueError, UnicodeError) as error:
                failures.append(f'{relative}: invalid JSON: {error}')
                continue
            if not isinstance(data, dict) or 'cases' not in data:
                continue
            names = set()
            for case in data['cases']:
                name = case.get('name')
                if not name or name in names:
                    failures.append(f'{relative}: missing/duplicate trace name {name}')
                names.add(name)
                steps = case.get('steps')
                if not isinstance(steps, list) or not steps:
                    failures.append(f'{relative}: {name}: no trace steps')
                    continue
                for step in steps:
                    if not isinstance(step.get('event'), str) or not step['event']:
                        failures.append(f'{relative}: {name}: missing event')
                    if 'expect' in step and (not isinstance(step['expect'], list)
                            or not step['expect'] or not all(isinstance(x, str) and x for x in step['expect'])):
                        failures.append(f'{relative}: {name}: invalid expectations')
            active_cases += len(data['cases'])
    print(json.dumps({'local_links_and_anchors': links, 'json_files': json_files,
                      'active_trace_cases': active_cases,
                      'failures': failures}, indent=2))
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
