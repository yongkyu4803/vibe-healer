#!/bin/bash
# healer 플러그인을 Claude Code skills 디렉토리에 설치합니다.
# 사용법: bash scripts/install_claude_code.sh
#
# ~/.claude/skills/healer/ 에 설치하면 @skills-dir 방식으로 자동 로드됩니다.
# 업데이트 시에도 동일하게 실행하면 됩니다.

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$HOME/.claude/skills/healer"

echo "healer 플러그인 설치 중..."
echo "소스: $PLUGIN_DIR"
echo "대상: $SKILLS_DIR"
echo ""

# 기존 설치 제거 후 재생성
rm -rf "$SKILLS_DIR"
mkdir -p "$SKILLS_DIR"

# .claude-plugin, commands, skills 복사
cp -r "$PLUGIN_DIR/.claude-plugin" "$SKILLS_DIR/"
cp -r "$PLUGIN_DIR/commands"       "$SKILLS_DIR/"
cp -r "$PLUGIN_DIR/skills"         "$SKILLS_DIR/"

echo "✅ 설치 완료"
echo ""
echo "Claude Code를 재시작(또는 /reload-plugins)하면 다음 명령어를 사용할 수 있습니다:"
echo "  /healer:start"
echo "  /healer:error-doctor"
echo "  /healer:git-savepoint"
echo "  /healer:deploy-fixer"
echo "  /healer:api-key-guardian"
echo "  /healer:local-run-doctor"
echo "  /healer:ui-screenshot-reviewer"
