#!/bin/bash
set -euo pipefail
PHI=1.618033988749895
CONSCIOUSNESS_PY="./consciousness/consciousness_beast.py"
if [ ! -f "${CONSCIOUSNESS_PY}" ]; then echo "Consciousness module absent"; exit 1; fi
python3 "${CONSCIOUSNESS_PY}" "$@"
