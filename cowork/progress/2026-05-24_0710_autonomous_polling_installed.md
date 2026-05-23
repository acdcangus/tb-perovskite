# 自律 5 分巡回ループ導入 完了（X1–X5）— 2026-05-24 07:10

PI directive `2026-05-24_0655_autonomous_5min_polling_directive.md` の X1–X5 を実装・コミット。
**commit `3f51cef`**（push 済み）。

## 完了タスク

| Task | 内容 | 状態 |
|---|---|---|
| X1 | `scripts/cowork_5min_poll.ps1`（層 1, OS スケジューラ） | ✅ `$env:COWORK_PROJECT_ROOT` 上書き可、lock + 再帰防止、SPDX ヘッダ付き |
| X2 | `scripts/cowork_5min_poll_README.md`（登録/停止/ログ/トークン/スリープ/disable） | ✅ 117 行 |
| X3a | `scan_shift_current_9materials.py` 主ループに `_check_cowork_progress()`（層 2） | ✅ 検出のみ・scan 非停止、liveness を `cowork/polling_logs/` に追記 |
| X3b | commit 前 `git status` + progress/ 確認の再徹底 | ✅ 慣習として継続（本 commit でも実施） |
| X4 | `PRODUCTION_RULES.md` に「5 分巡回前提」段落 | ✅ |
| X5 | `next_directive.md` §-1 にループ説明リンク | ✅ |

`cowork/polling_logs/` は `.gitignore` 済み。`COWORK_CLAUDECODE_PATTERN.md`（PI/Cowork 追記の 127 行パターン）も同 commit で追跡。

## PI が手で 1 回叩くコマンド（管理者 PowerShell）

```powershell
$Action  = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File C:\Users\kteru\tb-perovskite\scripts\cowork_5min_poll.ps1"
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries `
    -AllowStartIfOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 4)
Register-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll" `
    -Action $Action -Trigger $Trigger -Settings $Settings -RunLevel Highest
```
停止: `Disable-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll"`（集中作業時）。詳細は README。

## ★ 要 PI 判断（directive §4 note 2）

- スクリプトは `claude --continue -p $Prompt` を使用（既存セッションに接続）。
  **環境によっては `--continue` が新セッションを開始**してしまう場合があります。その場合 `-p` のみ（毎回新規・
  コンテキスト消費増）にするか、PI 環境で `--continue` が期待通り既存セッションへ繋がるか **1 回手動検証**を推奨。
- SPDX は **`NOASSERTION`**（リポジトリに LICENSE ファイルが無いため捏造回避）。プロジェクトのライセンスが決まったら差し替えを。

## 次

5 分巡回ループ導入は最優先タスクとして完了。指示が無ければ Theme I（励起子）§3 の PI 判断待ち、
または有効質量マップ単独の Production 化に進みます。次の巡回で `cowork/progress/` を確認します。
