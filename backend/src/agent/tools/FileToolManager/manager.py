import os
import shutil
import json
from pathlib import Path
from typing import Optional


class FileToolManager:

    def create_file(self, path: str, overwrite: bool = False, create_parents: bool = False):
        try:
            p = Path(path)
            if p.exists() and not overwrite:
                return {"status": "error", "message": f"File already exists: {path}"}
            if create_parents:
                p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()
            return {"status": "success", "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def read_file(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            if p.is_dir():
                return {"status": "error", "message": f"Path is a directory: {path}"}
            content = p.read_text(encoding="utf-8")
            return {"status": "success", "content": content, "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def write_file(self, path: str, content: str, overwrite: bool = False, create_if_missing: bool = True):
        try:
            p = Path(path)
            if p.exists() and not overwrite:
                return {"status": "error", "message": f"File exists, use overwrite=true: {path}"}
            if not p.exists() and not create_if_missing:
                return {"status": "error", "message": f"File does not exist: {path}"}
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return {"status": "success", "path": str(p.resolve()), "bytes_written": len(content)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def append_to_file(self, path: str, content: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            with open(p, "a", encoding="utf-8") as f:
                f.write(content)
            return {"status": "success", "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_file(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            return {"status": "success", "message": f"Deleted: {path}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def rename_file(self, path: str, new_name: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            new_path = p.parent / new_name
            p.rename(new_path)
            return {"status": "success", "new_path": str(new_path.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def move_file(self, path: str, new_path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            dest = Path(new_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(dest))
            return {"status": "success", "new_path": str(dest.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def copy_file(self, path: str, new_path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            dest = Path(new_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            if p.is_dir():
                shutil.copytree(p, dest)
            else:
                shutil.copy2(p, dest)
            return {"status": "success", "new_path": str(dest.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def file_exists(self, path: str):
        p = Path(path)
        return {"status": "success", "exists": p.exists(), "path": str(p.resolve())}

    def get_file_info(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            stat = p.stat()
            return {
                "status": "success",
                "path": str(p.resolve()),
                "size": stat.st_size,
                "is_file": p.is_file(),
                "is_dir": p.is_dir(),
                "modified": stat.st_mtime,
                "created": stat.st_ctime,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_file_size(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            return {"status": "success", "size": p.stat().st_size, "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_file_permissions(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            import stat as stat_module
            st = p.stat()
            mode = stat_module.filemode(st.st_mode)
            return {"status": "success", "permissions": mode, "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def set_file_permissions(self, path: str, mode: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            import stat as stat_module
            p.chmod(stat_module.S_IMODE(int(mode, 8)))
            return {"status": "success", "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def touch_file(self, path: str):
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()
            return {"status": "success", "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def replace_in_file(self, path: str, old: str, new: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            content = p.read_text(encoding="utf-8")
            if old not in content:
                return {"status": "error", "message": "String not found in file"}
            new_content = content.replace(old, new)
            p.write_text(new_content, encoding="utf-8")
            return {"status": "success", "replacements": content.count(old)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def search_in_file(self, path: str, pattern: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            content = p.read_text(encoding="utf-8")
            lines = content.split("\n")
            matches = [(i+1, line) for i, line in enumerate(lines) if pattern in line]
            return {"status": "success", "matches": matches, "count": len(matches)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def count_lines(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            count = sum(1 for _ in open(p, encoding="utf-8"))
            return {"status": "success", "lines": count}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_file_lines(self, path: str, start: int = 1, end: Optional[int] = None):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            lines = p.read_text(encoding="utf-8").split("\n")
            if end:
                return {"status": "success", "lines": lines[start-1:end], "count": len(lines[start-1:end])}
            return {"status": "success", "lines": lines[start-1:], "count": len(lines[start-1:])}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def validate_json_file(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            json.loads(p.read_text(encoding="utf-8"))
            return {"status": "success", "valid": True}
        except json.JSONDecodeError as e:
            return {"status": "success", "valid": False, "error": str(e)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def format_json_file(self, path: str, indent: int = 2):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            data = json.loads(p.read_text(encoding="utf-8"))
            formatted = json.dumps(data, indent=indent, ensure_ascii=False)
            p.write_text(formatted, encoding="utf-8")
            return {"status": "success", "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def read_json(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            data = json.loads(p.read_text(encoding="utf-8"))
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def write_json(self, path: str, data: dict, indent: int = 2):
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            content = json.dumps(data, indent=indent, ensure_ascii=False)
            p.write_text(content, encoding="utf-8")
            return {"status": "success", "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def detect_file_type(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            import mimetypes
            mime = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
            return {"status": "success", "mime_type": mime, "extension": p.suffix}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def compare_files(self, path1: str, path2: str):
        try:
            p1, p2 = Path(path1), Path(path2)
            if not p1.exists() or not p2.exists():
                return {"status": "error", "message": "One or both files not found"}
            content1, content2 = p1.read_text(encoding="utf-8"), p2.read_text(encoding="utf-8")
            identical = content1 == content2
            return {"status": "success", "identical": identical}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_file_encoding(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            with open(p, "rb") as f:
                import chardet
                raw = f.read()
                result = chardet.detect(raw)
                return {"status": "success", "encoding": result["encoding"], "confidence": result["confidence"]}
        except ImportError:
            return {"status": "success", "encoding": "utf-8", "note": "chardet not installed, assuming utf-8"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def calculate_file_hash(self, path: str, algorithm: str = "sha256"):
        try:
            import hashlib
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            h = hashlib.new(algorithm)
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    h.update(chunk)
            return {"status": "success", "hash": h.hexdigest(), "algorithm": algorithm}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_created_time(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            return {"status": "success", "created": p.stat().st_ctime}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_modified_time(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            return {"status": "success", "modified": p.stat().st_mtime}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_modified_time(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"File not found: {path}"}
            import time
            os.utime(p, (time.time(), time.time()))
            return {"status": "success", "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}


class DirectoryManager:
    
    def create_directory(self, path: str):
        try:
            p = Path(path)
            p.mkdir(parents=True, exist_ok=True)
            return {"status": "success", "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_directory(self, path: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"Directory not found: {path}"}
            shutil.rmtree(p)
            return {"status": "success", "message": f"Deleted: {path}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_directory(self, path: str = "."):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"Directory not found: {path}"}
            if not p.is_dir():
                return {"status": "error", "message": f"Not a directory: {path}"}
            items = [{"name": item.name, "is_dir": item.is_dir()} for item in p.iterdir()]
            return {"status": "success", "items": items, "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def directory_exists(self, path: str):
        p = Path(path)
        return {"status": "success", "exists": p.exists() and p.is_dir(), "path": str(p.resolve())}

    def get_directory_size(self, path: str):
        try:
            p = Path(path)
            if not p.exists() or not p.is_dir():
                return {"status": "error", "message": f"Directory not found: {path}"}
            total = sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
            return {"status": "success", "size": total, "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_directory_tree(self, path: str = ".", max_depth: int = 3):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"Directory not found: {path}"}
            
            def build_tree(dir_path: Path, depth: int = 0):
                if depth > max_depth:
                    return "..."
                items = []
                for item in sorted(dir_path.iterdir()):
                    if item.is_dir():
                        items.append({"name": item.name + "/", "children": build_tree(item, depth + 1)})
                    else:
                        items.append({"name": item.name})
                return items
            
            return {"status": "success", "tree": build_tree(p), "path": str(p.resolve())}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def walk_directory(self, path: str = "."):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"Directory not found: {path}"}
            result = []
            for root, dirs, files in os.walk(p):
                rel = Path(root).relative_to(p)
                result.append({"path": str(rel), "dirs": dirs, "files": files})
            return {"status": "success", "walk": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def search_files_by_content(self, path: str, pattern: str, file_pattern: str = "*"):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"Directory not found: {path}"}
            matches = []
            from fnmatch import fnmatch
            for f in p.rglob(file_pattern):
                if f.is_file():
                    try:
                        content = f.read_text(encoding="utf-8", errors="ignore")
                        if pattern in content:
                            matches.append(str(f.relative_to(p)))
                    except:
                        pass
            return {"status": "success", "matches": matches, "count": len(matches)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def find_files_by_name(self, path: str, name: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"Directory not found: {path}"}
            matches = [str(f.relative_to(p)) for f in p.rglob(name) if f.is_file()]
            return {"status": "success", "matches": matches, "count": len(matches)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def find_files_by_extension(self, path: str, ext: str):
        try:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "message": f"Directory not found: {path}"}
            if not ext.startswith("."):
                ext = "." + ext
            matches = [str(f.relative_to(p)) for f in p.rglob(f"*{ext}")]
            return {"status": "success", "matches": matches, "count": len(matches)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
