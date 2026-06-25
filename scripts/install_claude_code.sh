#!/bin/bash
# vibe-healer 플러그인을 Claude Code 로컬 플러그인으로 등록합니다.
# 사용법: bash scripts/install_claude_code.sh

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PLUGINS_CACHE="$HOME/.claude/plugins/cache/local"
INSTALLED_JSON="$HOME/.claude/plugins/installed_plugins.json"
VERSION="0.1.0"
PLUGIN_NAME="vibe-healer"
INSTALL_PATH="$PLUGINS_CACHE/$PLUGIN_NAME/$VERSION"

echo "vibe-healer 로컬 플러그인 설치..."
echo "소스: $PLUGIN_DIR"
echo ""

# 플러그인 캐시 디렉토리 생성
mkdir -p "$PLUGINS_CACHE/$PLUGIN_NAME"

# 이미 존재하면 제거 후 재등록
if [ -L "$INSTALL_PATH" ] || [ -d "$INSTALL_PATH" ]; then
  rm -rf "$INSTALL_PATH"
fi

# 소스 폴더를 버전 경로로 심링크
ln -s "$PLUGIN_DIR" "$INSTALL_PATH"
echo "✅ 플러그인 캐시 등록: $INSTALL_PATH"

# installed_plugins.json 업데이트
if [ ! -f "$INSTALLED_JSON" ]; then
  echo '{"version": 2, "plugins": {}}' > "$INSTALLED_JSON"
fi

python3 - <<PYEOF
import json, datetime, sys

path = "$INSTALLED_JSON"
with open(path) as f:
    data = json.load(f)

key = "${PLUGIN_NAME}@local"
data["plugins"][key] = [
    {
        "scope": "user",
        "installPath": "$INSTALL_PATH",
        "version": "$VERSION",
        "installedAt": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    }
]

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("✅ installed_plugins.json 업데이트 완료")
PYEOF

echo ""
echo "설치 완료. Claude Code를 재시작하면 다음 스킬을 사용할 수 있습니다:"
echo "  /error-doctor       — 터미널 에러 진단"
echo "  /git-savepoint      — Git 세이브포인트 생성"
echo "  /deploy-fixer       — 배포 실패 진단"
echo "  /api-key-guardian   — API 키 노출 점검"
echo "  /local-run-doctor   — 로컬 실행 진단"
echo "  /ui-screenshot-reviewer — UI 스크린샷 리뷰"
