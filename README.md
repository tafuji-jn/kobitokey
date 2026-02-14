# KobitoKey

左右分割キーボード KobitoKey のZMKファームウェア設定リポジトリ。

## キーマップ

![KobitoKey Keymap](keymap-drawer/KobitoKey.svg)

キーマップは [ZMK keymap-editor](https://nickcoutsos.github.io/keymap-editor) で編集可能（フォーク要）。
画像はpush時に [keymap-drawer](https://github.com/caksoylar/keymap-drawer) で自動生成される。

## 仕様

- ボード: Seeeduino XIAO BLE
- ファームウェア: ZMK v0.3（ZMK Studio対応）
- キー数: 40キー（5x4 x2）
- トラックボール: PMW3610 x2（左: スクロール専用、右: カーソル + オートマウスレイヤー）
- LED: RGB LED Widget

## 標準からの変更点

### 外部モジュール

| モジュール | 用途 |
|-----------|------|
| [zmk-pmw3610-driver](https://github.com/badjeff/zmk-pmw3610-driver) | PMW3610トラックボールドライバ |
| [zmk-feature-sensor_rotation](https://github.com/hsgw/zmk-feature-sensor_rotation) | トラックボールの回転補正 |
| [zmk-pointing-acceleration](https://github.com/oleksandrmaslov/zmk-pointing-acceleration) | ポインタ加速（左右トラックボール両方に適用） |
| [zmk-tri-state](https://github.com/dhruvinsh/zmk-tri-state) | Alt+Tab / Ctrl+PgDn/PgUpスワッパー |

### カスタムbehavior

| 名前 | 説明 |
|------|------|
| `swapper` | Alt+Tab ウィンドウ切替（Shift併用で逆方向） |
| `tab_next` | Ctrl+PageDown 次のタブ切替 |
| `tab_prev` | Ctrl+PageUp 前のタブ切替 |
| `mkp_exit_AML` | 左クリック + オートマウスレイヤー解除 |

### トラックボール設定

- **左トラックボール**: スクロール専用。ポインタ加速 + XY→スクロール変換
- **右トラックボール**: カーソル移動。ポインタ加速 + オートマウスレイヤー（layer 3）自動有効化
- **スクロールレイヤー** (layer 4): `&mo 4`ホールド中に右トラックボールがスクロール動作に切替

### オートマウスレイヤー

- 右トラックボール操作で自動的にMOUSEレイヤー（layer 3）が有効化
- `excluded-positions`は`scripts/update_excluded_positions.py`でCIにより自動更新
- 左クリック（`&mkp_exit_AML`）でレイヤー解除

### JP配列対応

OS設定が日本語キーボードのまま使用するための変換定義（`JP_*`）を定義。
アンダーバー・円マークはコンボで入力可能。

### パスワードマクロ

`password1`〜`password9` のマクロを定義。
実際のパスワードは非公開リポジトリ（`kobitokey_private`）のGitHub Secretsで管理され、ビルド時に自動変換される。
詳細は非公開リポジトリのREADMEを参照。

### レイヤー構成

| Layer | 名前 | 説明 |
|-------|------|------|
| 0 | default | メインレイヤー |
| 1 | ARROW | 矢印キー + 数字 |
| 2 | NUMBER_FUNC | テンキー + ファンクション + BT |
| 3 | MOUSE | オートマウスレイヤー（自動有効化） |
| 4 | SCROLL | 右トラックボールスクロールモード |
| 5 | MACRO | パスワードマクロ |
