#!/usr/bin/env bash
set -euo pipefail
required=(README.md ANDYAI_CONTEXT.md SECOND_BRAIN_CANON.md docs/pack8/PACK8_TOC.md runtime/bin/brain-lifecycle)
for f in "${required[@]}"; do
  [[ -e "$f" ]] || { echo "Missing required file: $f"; exit 1; }
done
[[ -x runtime/bin/brain-lifecycle ]] || { echo "runtime/bin/brain-lifecycle not executable"; exit 1; }
python3 - <<'PYVERIFY'
from pathlib import Path
import json
for p in Path('schemas').glob('*.json'):
    json.loads(p.read_text(encoding='utf-8'))
print('✅ AndyAI Second Brain verification passed.')
PYVERIFY
