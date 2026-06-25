#!/bin/bash
# vibe-healer 플러그인을 Claude Code 로컬 플러그인으로 등록합니다.
# 사용법: bash scripts/install_claude_code.sh

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INSTALLED_JSON="$HOME/.claude/plugins/installed_plugins.json"
VERSION="0.1.0"
PLUGIN_NAME="vibe-healer"

echo "vibe-healer 로컬 플러그인 등록..."
echo "플러그인 경로: $PLUGIN_DIR"
echo ""

# installed_plugins.json 없으면 초기화
if [ ! -f "$INSTALLED_JSON" ]; then
  echo '{"version": 2, "plugins": {}}' > "$INSTALLED_JSON"
fi

python3 - <<PYEOF
import json, datetime

path = "$INSTALLED_JSON"
with open(path) as f:
    data = json.load(f)

key = "${PLUGIN_NAME}@local"
data["plugins"][key] = [
    {
        "scope": "user",
        "installPath": "$PLUGIN_DIR",
        "version": "$VERSION",
        "installedAt": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    }
]

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("✅ installed_plugins.json 등록 완료")
PYEOF

echo ""
echo "완료. Claude Code를 재시작하면 다음 명령어를 사용할 수 있습니다:"
echo "  /vibe-healer:start              — 트리아지 허브"
echo "  /vibe-healer:error-doctor       — 터미널 에러 진단"
echo "  /vibe-healer:git-savepoint      — Git 세이브포인트"
echo "  /vibe-healer:deploy-fixer       — 배포 실패 진단"
echo "  /vibe-healer:api-key-guardian   — API 키 점검"
echo "  /vibe-healer:local-run-doctor   — 로컬 실행 진단"
echo "  /vibe-healer:ui-screenshot-reviewer — UI 리뷰"
