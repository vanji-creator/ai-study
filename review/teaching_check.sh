#!/bin/bash
# Printed into the tutor's context before every reply (UserPromptSubmit hook in
# .claude/settings.json). It is the check behind CLAUDE.md §1.2 — "a rule nothing checks
# is a wish". Keep it short: it is read on every turn.
cat <<'CHECKLIST'
Teaching check (CLAUDE.md §1.2) — before replying:
1. Am I answering his exact question first?
2. One idea only?
3. Any maths word not yet in notes/maths-for-ml.md? Teach it first.
4. Does any formula appear before its question, picture and measured numbers?
5. Am I asking him to do arithmetic? Ask about meaning, direction or why instead.
6. Am I widening — extra reasons, cases or tables he did not ask for?
CHECKLIST
