#!/usr/bin/env bash
# Installs a pre-push hook running the full validator, external-paths included.
#
# CI cannot run external-paths: it resolves ~/brain/... which exists only on this
# machine. That check is the one that catches C-01 (a renumbered vault path that left two
# skills non-functional and went unnoticed for nine commits), so it needs to be enforced
# somewhere. This is that somewhere.
#
#   bash scripts/install-hooks.sh     # install
#   git push --no-verify              # bypass once, deliberately
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOK="$REPO_ROOT/.git/hooks/pre-push"

cat > "$HOOK" <<'HOOK_BODY'
#!/usr/bin/env bash
# Installed by scripts/install-hooks.sh — re-run it to update.
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
if ! python3 "$REPO_ROOT/scripts/validate_skills.py" --quiet; then
    echo ""
    echo "pre-push blocked: skills validation failed (see above)."
    echo "Fix it, or push with --no-verify if the failure is external-paths on a machine"
    echo "that does not have ~/brain — that check is machine-dependent by design."
    exit 1
fi
HOOK_BODY

chmod +x "$HOOK"
echo "installed: $HOOK"
echo "verifying it runs..."
python3 "$REPO_ROOT/scripts/validate_skills.py" --quiet \
    && echo "validator currently clean — hook will allow pushes" \
    || echo "validator currently FAILING — hook would block a push right now"
