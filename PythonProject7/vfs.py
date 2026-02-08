# vfs.py – простая виртуальная файловая система на JSON
import json
from pathlib import Path

APP_ROOT = Path(__file__).parent
VFS_PATH = APP_ROOT / "vfs.json"


DEFAULT_VFS = {
    "type": "dir",
    "name": "/",
    "children": [
        {
            "type": "dir",
            "name": "Документы",
            "children": [
                {
                    "type": "file",
                    "name": "readme.txt",
                    "content": "Добро пожаловать в Windows 12 FakeOS!\n"
                }
            ]
        },
        {
            "type": "dir",
            "name": "Система",
            "children": []
        }
    ]
}


def _load_tree():
    if not VFS_PATH.exists():
        save_tree(DEFAULT_VFS)
        return DEFAULT_VFS
    with open(VFS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tree(tree):
    with open(VFS_PATH, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)


def _split(path: str):
    if path == "/" or path == "":
        return []
    return [p for p in path.split("/") if p]


def _find_node(tree, path: str):
    parts = _split(path)
    node = tree
    for part in parts:
        if node.get("type") != "dir":
            return None
        found = None
        for ch in node.get("children", []):
            if ch["name"] == part:
                found = ch
                break
        if not found:
            return None
        node = found
    return node


def list_dir(path: str):
    tree = _load_tree()
    node = _find_node(tree, path)
    if not node or node.get("type") != "dir":
        return []
    return node.get("children", [])


def read_file(path: str) -> str:
    tree = _load_tree()
    node = _find_node(tree, path)
    if not node or node.get("type") != "file":
        return ""
    return node.get("content", "")


def write_file(path: str, content: str):
    tree = _load_tree()
    parent_path, _, fname = path.rpartition("/")
    parent = _find_node(tree, parent_path)
    if not parent or parent.get("type") != "dir":
        return
    # ищем существующий файл
    for ch in parent.get("children", []):
        if ch["name"] == fname and ch["type"] == "file":
            ch["content"] = content
            save_tree(tree)
            return
    # иначе создаём
    parent.setdefault("children", []).append({
        "type": "file",
        "name": fname,
        "content": content
    })
    save_tree(tree)


def create_dir(path: str, name: str):
    tree = _load_tree()
    parent = _find_node(tree, path)
    if not parent or parent.get("type") != "dir":
        return
    parent.setdefault("children", []).append({
        "type": "dir",
        "name": name,
        "children": []
    })
    save_tree(tree)
