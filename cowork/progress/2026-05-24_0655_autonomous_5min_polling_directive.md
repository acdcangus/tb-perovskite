# Directive — 自律 5 分巡回ループの導入（PI 起床トリガ）

**発行元:** Cowork supervisor (chat session, PI 起床後の直接依頼)
**発行時刻:** 2026-05-24 06:55 JST (21:51 UTC, 5/23)
**対象 commit:** `1a93de0`（Claude Code が ~5 分前に push、Theme I exploratory log）
**背景:** 昨夜 17:40 UTC → 21:45 UTC の約 4 時間沈黙（`2026-05-23_2225_BLOCKED_session_stalled.md` 参照）。PI から「Claude Code が自律的に 5 分ごとに指示確認するようにして」との依頼。

---

## 1. やってほしいこと（タスク化、優先度高）

### Task X1: PowerShell 巡回スクリプトをコミット

ファイル: `scripts/cowork_5min_poll.ps1`

中身は `cowork/COWORK_CLAUDECODE_PATTERN.md` の §「5 分自律巡回ループ」§「層 1」§「PowerShell スクリプト」をそのままコピー。**ハードコードされた `C:\Users\kteru\tb-perovskite` パスを `$env:COWORK_PROJECT_ROOT` で上書き可能に**してください（デフォルトはハードコード値）：

```powershell
$ProjectRoot = if ($env:COWORK_PROJECT_ROOT) { $env:COWORK_PROJECT_ROOT } else { "C:\Users\kteru\tb-perovskite" }
```

加えて:
- `polling_logs/` は `.gitignore` に追加（コミット汚染防止）
- スクリプト先頭に SPDX license ヘッダと使用法コメント

commit メッセージ例:
```
scripts: add 5-min autonomous polling script (cowork_5min_poll.ps1)

PowerShell + Windows Task Scheduler で claude --continue -p を 5 分ごとに起動。
Claude Code セッションがクラッシュ・スタックしても OS から強制的に巡回プロンプトを流し込み、
silent gap (2026-05-23 17:40 UTC→21:45 UTC, ~4h) の再発を防ぐ。

Refs cowork/COWORK_CLAUDECODE_PATTERN.md §「5 分自律巡回ループ」
Refs cowork/progress/2026-05-23_2225_BLOCKED_session_stalled.md
Refs cowork/progress/2026-05-24_0655_autonomous_5min_polling_directive.md
```

### Task X2: Task Scheduler 登録の README を書く

ファイル: `scripts/cowork_5min_poll_README.md`

内容:
1. インストール手順（管理者 PowerShell から `Register-ScheduledTask`）
2. 停止 / 一時無効化コマンド
3. ログ確認場所（`cowork/polling_logs/`）
4. API トークン消費の目安（5-30k tok/巡回 × 288 巡回/日）
5. PC スリープ中の挙動（`Wake the computer to run this task` の有無で変わる）
6. **PI が手作業で集中したい時の disable 方法**

### Task X3: セッション内ループ（層 2）の実装

以下の 2 点を Claude Code 自身の習慣として実装:

**(a) 長いスクリプトに 5 分巡回フック**

`scripts/` 配下で計算時間が 5 分以上見込まれるスクリプト（例: `scan_shift_current_9materials.py`、`scan_g_factors.py`、Theme I 以降の新規スキャン）の主ループに以下を追加:

```python
from pathlib import Path
import datetime as _dt
import subprocess as _sp

_LAST_POLL = _dt.datetime.now()

def _check_cowork_progress(project_root: Path) -> None:
    """Cowork progress/ の新着 directive を確認（5 分ごとに呼ぶ）.

    新着があれば stdout に WARNING を吐く。スクリプト本体は止めない
    （止めると Production の中断になるため、検出のみ）。
    """
    global _LAST_POLL
    now = _dt.datetime.now()
    if (now - _LAST_POLL).total_seconds() < 300:
        return
    _LAST_POLL = now
    progress = project_root / "cowork" / "progress"
    if not progress.is_dir():
        return
    cutoff = now - _dt.timedelta(minutes=10)
    new = [
        p for p in progress.glob("*.md")
        if _dt.datetime.fromtimestamp(p.stat().st_mtime) > cutoff
        and any(tag in p.name for tag in ("directive_", "code_review", "question", "BLOCKED"))
    ]
    if new:
        print(f"[cowork-poll {now:%H:%M}] new directive(s): {[p.name for p in new]}", flush=True)
```

スキャンの主ループ（k 点ループ等）の末尾で `_check_cowork_progress(PROJECT_ROOT)` を呼ぶ。これでスクリプト実行中も 5 分粒度で進捗 log に「生存」が残り、新着 directive にも気付く。

**(b) commit 前の `git status` と progress/ 確認の自動化**

既存ルールを再徹底するだけ。docstring・コミットメッセージで明示。

### Task X4: PRODUCTION_RULES.md に「5 分巡回が動いている前提」を追記

`cowork/PRODUCTION_RULES.md` の Production セクションに 1 段落:

> **5 分自律巡回の前提:** Production 実行中も `cowork_5min_poll.ps1` が動作しており、Claude Code は最大 5 分以内に新着 directive を検知できる。Production scan で 30 分以上を要する計算では、上記 (a) の `_check_cowork_progress` を主ループに組み込み、生存と新着検知の両方を担保する。

### Task X5: next_directive.md の冒頭に短いリンクを追加

`cowork/next_directive.md` の §0 ハルシネーション防止の前に、§-1 として:

> **自律 5 分巡回ループ（2026-05-24 導入）:** 詳細は `cowork/COWORK_CLAUDECODE_PATTERN.md` §「5 分自律巡回ループ」。本 directive を読む時は「層 1（OS スケジューラ）が動いている」前提。

---

## 2. 優先順位

X1 → X2 → X5 → X4 → X3 の順を推奨。
X1 / X2 は 30 分以内、X5 / X4 は 10 分以内、X3 は次の新規 Production scan を書く時に同時整備で可。

PI から別タスクが来ていない限り、Theme I 続行や `PI_summary_2026-05-24.md` 修正よりも **このループ導入を最優先**してください。理由：再発防止が今後すべての作業の品質を決めるため。

## 3. 完了通知

- 全完了したら `cowork/progress/2026-05-24_<HHMM>_autonomous_polling_installed.md` で通知
- `scripts/cowork_5min_poll.ps1` と `scripts/cowork_5min_poll_README.md` のパス + commit hash を記載
- PI が手で `Register-ScheduledTask` を叩く必要があるので、コピペできるワンライナーも完了通知に再掲

## 4. 注意

- このスクリプトは Claude Code 自身を起動する → 巡回プロンプト中で**再帰的に巡回プロンプトを発行しない**こと（無限ループ防止、層 1 スクリプト中の lock 機構で 4 分以内の多重起動は弾けるが念のため）
- `claude --continue -p` の `--continue` は既存セッションに接続する。**起動時に新セッションを開始してしまう環境**では `-p` だけにする選択肢もあるが、コンテキスト消費が増える。要 PI 判断
- 巡回 log は `cowork/polling_logs/poll_YYYY-MM-DD.log` に追記方式。1 日 1 ファイル、ローテーション不要（年間 ~5-10 MB と見込み）

---

## 5. supervisor 側の運用変更（参考）

15 分 patrol は維持。ただし、層 1 (5 分巡回) が動き始めると Claude Code 側の commit 頻度が上がるはずなので、supervisor patrol の判定基準を以下に更新する予定:

- silent 30 分（旧: 60 分） → 軽い status check
- silent 60 分（旧: 100 分） → BLOCKED 宣言の準備
- silent 90 分（旧: 200 分） → BLOCKED 宣言

これは supervisor 側の scheduled task プロンプトを後で更新する。

---

**この directive は PI（ktmailmg@gmail.com）の直接依頼に基づきます。PI が起きているので、不明点はチャットで即聞いて OK。**
