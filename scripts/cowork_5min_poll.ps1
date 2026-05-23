# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
# cowork_5min_poll.ps1
# -----------------------------------------------------------------------------
# 5 分ごとに Claude Code を起こして cowork/progress/ の新着確認と次タスクの
# 実行を促す巡回スクリプト。Windows Task Scheduler から起動される想定。
#
# 詳細設計: cowork/COWORK_CLAUDECODE_PATTERN.md §「5 分自律巡回ループ」
# 動機: 2026-05-23 17:40 UTC → 21:45 UTC の約 4 時間沈黙の再発防止
#       (cowork/progress/2026-05-23_2225_BLOCKED_session_stalled.md)
#
# インストール手順は scripts/cowork_5min_poll_README.md を参照。
# -----------------------------------------------------------------------------

$ProjectRoot = if ($env:COWORK_PROJECT_ROOT) { $env:COWORK_PROJECT_ROOT } else { "C:\Users\kteru\tb-perovskite" }
$LogDir      = Join-Path $ProjectRoot "cowork\polling_logs"
$LogFile     = Join-Path $LogDir ("poll_" + (Get-Date -Format "yyyy-MM-dd") + ".log")

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

# --- 多重起動防止: 既に巡回中（4 分以内）なら skip -------------------------
$LockFile = Join-Path $LogDir ".poll.lock"
if (Test-Path $LockFile) {
    $lockAge = (Get-Date) - (Get-Item $LockFile).LastWriteTime
    if ($lockAge.TotalMinutes -lt 4) {
        Add-Content $LogFile "$(Get-Date -Format o) skip (lock age $([math]::Round($lockAge.TotalMinutes,1)) min)"
        exit 0
    }
}
New-Item -ItemType File -Path $LockFile -Force | Out-Null

try {
    Set-Location $ProjectRoot

    # --- 巡回プロンプト本体（変更時は PATTERN 文書も更新） ----------------
    $Stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $Date  = Get-Date -Format "yyyy-MM-dd"
    $Prompt = @"
[Cowork 自律巡回 $Stamp]

cowork/progress/ の過去 10 分以内の新着 (特に *_directive_*.md / *_code_review.md / *_question.md / BLOCKED_*.md) を確認してください。

判断ルール:
1. 新着 directive があれば内容を要約して即実行（重要度に応じて優先度判断、ただし執筆中の commit/test 単位は finish してから着手）。
2. 何も無く、現在の作業が継続中なら "$(Get-Date -Format HHmm) checked, continuing <topic>" の 1 行を cowork/polling_logs/poll_${Date}.log に追記して作業に戻る。
3. 何も無く、現在やることが無ければ cowork/next_directive.md の優先順位（特に §「PI 不在中の作業優先順位」）に従って次タスクを開始。
4. このターンは最大 3 分以内で切り上げる（巡回は軽量に、長い作業は次の独立セッションで）。
5. 再帰的に本巡回スクリプトを起動しない（無限ループ防止）。

GIT 状態確認: git log -3 --oneline / git status --short を最初に実行してから判断してください。
"@

    # claude --continue で既存セッションに接続。-p で 1-shot 実行。
    # 出力は log に追記、stderr も拾う。
    Add-Content $LogFile "$(Get-Date -Format o) poll start"
    & claude --continue -p $Prompt --output-format text *>&1 | Tee-Object -Append -FilePath $LogFile
    Add-Content $LogFile "$(Get-Date -Format o) poll completed (exit=$LASTEXITCODE)"
} catch {
    Add-Content $LogFile "$(Get-Date -Format o) ERROR: $_"
    throw
} finally {
    Remove-Item $LockFile -Force -ErrorAction SilentlyContinue
}
