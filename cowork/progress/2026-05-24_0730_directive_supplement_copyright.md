# Directive 補足 — MIT LICENSE の Copyright holder 確定

**発行元:** Cowork supervisor（PI 起床判断 (iv) を受領）
**発行時刻:** 2026-05-24 07:30 JST (22:30 UTC, 5/23)
**親 directive:** `2026-05-24_0715_directive_theme_I_hybrid_and_license.md` §2 Task Y2
**スコープ:** Y2 (LICENSE) の Copyright holder 名のみを確定。他の Y1/Y2 仕様は親 directive のまま。

---

## 確定事項

PI から本セッションで以下の判断を受領:

> 「MIT 採用時の Copyright holder は tk」

→ **Copyright holder 表記は `tk` を使用**してください（PI のイニシャル）。

## 反映方法

### `LICENSE`（repo ルート）

MIT License テンプレートの copyright 行:

```
Copyright (c) 2026 tk
```

### `scripts/cowork_5min_poll.ps1` SPDX ヘッダ

```powershell
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
```

### 主要 `src/perovskite_tb/*.py` および `scripts/*.py`（オプション追加）

```python
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 tk
```

## 注意

- `Teruhisa Kotani` の full name 表記には**しない**（PI 明示で `tk`）
- 過去 commit の author email（`ktmailmg@gmail.com`）や git config の author name は変更しなくて OK（ライセンス表記とは独立）
- 論文化・公開時に full name 表記が必要になったら、PI が後から差し替える判断をします

## 親 directive との関係

Y2 タスクは本補足で copyright が確定したので、**Y2 はそのまま着手可能**になりました。Y1-a/Y1-c/Y1-d は親 directive のまま（変更なし）。

完了通知は親 directive §4 に従って `cowork/progress/2026-05-24_<HHMM>_Y2_license_added.md` で。
