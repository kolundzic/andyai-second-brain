#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -f README.md
test -f docs/visuals/andyai-second-brain-overview.png
test -f docs/visuals/what-you-can-do-with-it.png
test -f docs/visuals/how-it-works.png
test -f docs/visuals/trust-and-privacy-architecture.png
test -f docs/visuals/plans-and-pricing.png
test -f docs/marketing/FRONT_PAGE_COPY_DECK.md
test -f docs/tutorials/01-beginner-quickstart.md
test -f docs/beginners/WHAT_IS_ANDYAI_SECOND_BRAIN.md
test -f docs/trust/PRIVACY_AND_TRUST.md
test -f docs/pricing/PLANS_AND_PRICING.md
test -f docs/tutorials/FIRST_TUTORIAL_SCAFFOLD.md
grep -q "AndyAI Second Brain" README.md
grep -q "Plans & Pricing" README.md
grep -q "Trust is not a feature" README.md
echo "marketing pack36-37 verify passed"
