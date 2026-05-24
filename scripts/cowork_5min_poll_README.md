# cowork_5min_poll.ps1 — セットアップと運用

> ## ⚠️ DEPRECATED（2026-05-24, PI 判断）
> 自律 5 分巡回ループは **停止** しました。監視は Cowork supervisor の 15 分巡回が代替します。
> 経緯: `cowork/progress/2026-05-24_1145_directive_PI_decisions.md` §Part 2。
> **解除手順**は本書末尾「§ 停止（Unregister）手順」、**再び有効化**する場合は「§ 再開手順」を参照。
> 以下のセットアップ記述は履歴として保持します。

5 分ごとに `claude --continue` を起動して `cowork/progress/` の新着を確認させる
Windows Task Scheduler 用スクリプトです。

詳細設計: `cowork/COWORK_CLAUDECODE_PATTERN.md` §「5 分自律巡回ループ」
動機: `cowork/progress/2026-05-23_2225_BLOCKED_session_stalled.md`（4 時間沈黙事例の再発防止）

---

## 1. 前提

- Windows 10/11、PowerShell 5.1+ (PowerShell 7 でも可)
- `claude` (Claude Code CLI) が PATH 上で起動できること（`claude --version` で確認）
- 管理者権限で PowerShell を起動できること（Task Scheduler 登録のため）
- Anthropic API キーが Claude Code に設定済み（プラン: Pro/Max 推奨。1 日 ~3-8M tok 消費見込み）

## 2. インストール（PI が管理者 PowerShell から 1 回だけ実行）

```powershell
# 1. プロジェクトルートを確認（環境変数で上書きしたい場合は事前にセット）
$env:COWORK_PROJECT_ROOT = "C:\Users\kteru\tb-perovskite"  # 既定値と同じなら省略可

# 2. Task Scheduler に 5 分間隔タスクを登録
$Action  = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File C:\Users\kteru\tb-perovskite\scripts\cowork_5min_poll.ps1"
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Minutes 5)
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
    -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 4)
Register-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll" `
    -Action $Action -Trigger $Trigger -Settings $Settings -RunLevel Highest
```

登録確認:
```powershell
Get-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll"
Get-ScheduledTaskInfo -TaskName "Cowork-ClaudeCode-5min-poll"
```

## 3. 動作確認

1. **手動 1 回実行**して動くか確認:
   ```powershell
   Start-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll"
   ```
2. ログ確認:
   ```powershell
   Get-Content -Tail 30 "C:\Users\kteru\tb-perovskite\cowork\polling_logs\poll_$(Get-Date -Format yyyy-MM-dd).log"
   ```
3. 5 分経過後に自動再実行されることを確認。

## 4. 停止 / 一時無効化

PI が手作業で集中したいとき:
```powershell
Disable-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll"
```
再開:
```powershell
Enable-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll"
```
完全削除:
```powershell
Unregister-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll" -Confirm:$false
```

## 5. ログ

- 場所: `cowork/polling_logs/poll_YYYY-MM-DD.log`
- 形式: ISO 8601 タイムスタンプ + `claude` の標準出力／標準エラー
- ローテーション: 日次ファイル（年間 ~5-10 MB を想定、手動削除可）
- **`.gitignore` 対象**（`polling_logs/` ごと除外推奨）

## 6. API トークン消費の目安

| ケース | トークン/巡回 | 1 日合計 |
|---|---|---|
| 新着ゼロ・継続作業中（log 1 行追記して終了） | ~3-10k | ~1-3M |
| 新着 directive あり・短い実行 | ~15-30k | ~5-8M |
| 沈黙状態から復旧（git log + progress 全読み + 着手） | ~50-100k | スパイク的に |

Pro プラン (5-rate limit) / Max プランで実用範囲。Free プランでは使わない。

## 7. PC スリープ中の挙動

Task Scheduler の既定では PC スリープ中は動きません。深夜も巡回したい場合:

```powershell
# Wake the computer to run this task を有効化
$task = Get-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll"
$task.Settings.WakeToRun = $true
Set-ScheduledTask -InputObject $task
```

ただし PC を頻繁にウェイクすると電源に影響します。ノート PC では非推奨。

## 8. トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| ログに何も出ない | Task Scheduler 未起動 | `Get-ScheduledTaskInfo` で `LastRunTime` 確認、再登録 |
| `claude: command not found` | PATH 通ってない | フルパス指定 or `claude.cmd` を PowerShell プロファイルで alias |
| `lock age X min skip` ばかり | 巡回が 4 分以上かかっている | `ExecutionTimeLimit` を 8 分に伸ばす or 巡回プロンプトを軽量化 |
| 重複 commit が増える | 巡回プロンプトの冪等性破れ | `cowork/COWORK_CLAUDECODE_PATTERN.md` §「層 3」の冪等ルールを再点検 |
| API rate limit | 巡回頻度過剰 | 5 分 → 10 分に伸ばす（`-RepetitionInterval` 変更）|

## 9. supervisor (Cowork 15 分 patrol) との関係

- **Cowork 15 分 patrol** は監督役（レビュー、directive 発行、ハルシネーション検出）
- **本 5 分巡回** は実装役（生存確認、新着 directive 取得、続行判断）
- 両者は独立に動く。supervisor が新規 directive を書くと、本 5 分巡回が 5 分以内に拾う。

---

## § 停止（Unregister）手順 — 2026-05-24 PI 判断で停止

PI が管理者 PowerShell で 1 行実行（Claude Code は Linux サンドボックスから PowerShell 実行不可のため手動）:

```powershell
Unregister-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll" -Confirm:$false
```

完了確認: `Get-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll"` が **ObjectNotFound** を返せば成功。

## § 再開手順（参考 — 将来再び有効化する場合）

本書冒頭「インストール（Register-ScheduledTask）」をそのまま再実行すればよい。スクリプト本体（`cowork_5min_poll.ps1`）は
履歴として保持されているため改変不要。再開時は `cowork/COWORK_CLAUDECODE_PATTERN.md` の停止注記も解除すること。

---

**質問・改善案は `cowork/progress/2026-05-24_<HHMM>_polling_feedback.md` で。**
