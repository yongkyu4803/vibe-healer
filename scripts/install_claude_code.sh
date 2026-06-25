#!/bin/bash
# vibe-healer 플러그인을 Claude Code 로컬 플러그인 캐시에 설치합니다.
# 사용법: bash scripts/install_claude_code.sh
#
# 업데이트 시에도 동일하게 실행하면 캐시를 덮어씁니다.

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CACHE_PATH="$HOME/.claude/plugins/cache/local/vibe-healer/0.1.0"
INSTALLED_JSON="$HOME/.claude/plugins/installed_plugins.json"
VERSION="0.1.0"
PLUGIN_NAME="vibe-healer"

echo "vibe-healer 설치 중..."
echo "소스: $PLUGIN_DIR"
echo "캐시: $CACHE_PATH"
echo ""

# 기존 캐시 제거 후 재생성
rm -rf "$CACHE_PATH"
mkdir -p "$CACHE_PATH"

# 핵심 파일 복사 (.claude-plugin, commands, skills)
cp -r "$PLUGIN_DIR/.claude-plugin" "$CACHE_PATH/"
cp -r "$PLUGIN_DIR/commands"       "$CACHE_PATH/"
cp -r "$PLUGIN_DIR/skills"         "$CACHE_PATH/"

echo "✅ 파일 복사 완료"

# installed_plugins.json 업데이트
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
        "installPath": "$CACHE_PATH",
        "version": "$VERSION",
        "installedAt": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    }
]

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("✅ installed_plugins.json 등록 완료")
PYEOF

echo ""
echo "Claude Code를 재시작하면 다음 명령어를 사용할 수 있습니다:"
echo "  /vibe-healer:start"
echo "  /vibe-healer:error-doctor"
echo "  /vibe-healer:git-savepoint"
echo "  /vibe-healer:deploy-fixer"
echo "  /vibe-healer:api-key-guardian"
echo "  /vibe-healer:local-run-doctor"
echo "  /vibe-healer:ui-screenshot-reviewer"
