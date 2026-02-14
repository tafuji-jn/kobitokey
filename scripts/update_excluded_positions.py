"""
MOUSEレイヤーのキー配置を解析し、excluded-positionsを自動更新するスクリプト。

対象外（オートマウスレイヤーを抜けるキー）:
  - &trans（透過）
  - &to N（レイヤー切替）

上記以外のキー（&mkp_exit_AML等のマクロ含む）はすべて
excluded-positions に含まれ、押してもオートマウスレイヤーに留まる。
※ 左クリック後のレイヤー解除は &mkp_exit_AML マクロが担当。
"""

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
KEYMAP_PATH = REPO_ROOT / "config" / "KobitoKey.keymap"
OVERLAY_PATH = (
    REPO_ROOT
    / "config"
    / "boards"
    / "shields"
    / "KobitoKey"
    / "KobitoKey_left.overlay"
)

MOUSE_LAYER_LABEL = "MOUSE"

# オートマウスレイヤーを抜けるキー（excluded-positionsに含めない）
EXIT_PATTERNS = [
    r"^&trans$",
    r"^&to \d+$",
]


def parse_bindings(bindings_text: str) -> list[str]:
    """bindings文字列をキーバインディングのリストに分割する。"""
    # 全体を空白でトークン分割
    tokens = bindings_text.split()
    keys = []
    current = None

    for token in tokens:
        if token.startswith("&"):
            # 新しいバインディングの開始
            if current is not None:
                keys.append(current)
            current = token
        else:
            # 前のバインディングのパラメータ
            if current is not None:
                current += " " + token
    if current is not None:
        keys.append(current)

    return keys


def parse_mouse_layer(keymap_text: str) -> list[str]:
    """MOUSEレイヤーのbindingsを抽出してキーリストを返す。"""
    pattern = re.compile(
        r'label\s*=\s*"' + re.escape(MOUSE_LAYER_LABEL) + r'".*?'
        r"bindings\s*=\s*<(.*?)>",
        re.DOTALL,
    )
    m = pattern.search(keymap_text)
    if not m:
        print(f'エラー: label="{MOUSE_LAYER_LABEL}" のレイヤーが見つかりません', file=sys.stderr)
        sys.exit(1)

    return parse_bindings(m.group(1))


def should_exclude(key: str) -> bool:
    """このキーがexcluded-positionsに含まれるべきかを判定。"""
    for pat in EXIT_PATTERNS:
        if re.match(pat, key):
            return False
    return True


def update_overlay(overlay_text: str, positions: list[int]) -> str:
    """overlay内のexcluded-positionsを更新する。"""
    pos_str = "\n".join(f"        {p}" for p in sorted(positions))
    new_block = f"&zip_temp_layer {{\n    excluded-positions = <\n{pos_str}\n    >;\n}}"

    pattern = re.compile(
        r"&zip_temp_layer\s*\{[^}]*excluded-positions\s*=\s*<[^>]*>\s*;\s*\}",
        re.DOTALL,
    )
    if not pattern.search(overlay_text):
        print("エラー: overlay内にexcluded-positionsブロックが見つかりません", file=sys.stderr)
        sys.exit(1)

    return pattern.sub(new_block, overlay_text)


def main():
    keymap_text = KEYMAP_PATH.read_text(encoding="utf-8")
    overlay_text = OVERLAY_PATH.read_text(encoding="utf-8")

    keys = parse_mouse_layer(keymap_text)
    print(f"MOUSEレイヤー: {len(keys)}キー検出")

    excluded = []
    for i, key in enumerate(keys):
        if should_exclude(key):
            excluded.append(i)
            print(f"  位置{i}: {key} -> excluded（レイヤー維持）")
        else:
            print(f"  位置{i}: {key} -> exit（レイヤー解除）")

    new_overlay = update_overlay(overlay_text, excluded)

    if new_overlay == overlay_text:
        print("\nexcluded-positionsに変更なし")
    else:
        OVERLAY_PATH.write_text(new_overlay, encoding="utf-8")
        print(f"\nexcluded-positions更新: {excluded}")


if __name__ == "__main__":
    main()
