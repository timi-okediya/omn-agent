import subprocess
import os
from pathlib import Path


class GitToolManager:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
    
    def _run(self, *args, cwd=None):
        cwd = cwd or self.repo_path
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Command timed out"}
        except FileNotFoundError:
            return {"status": "error", "message": "Git not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def init(self, path: str = None):
        target = Path(path) if path else self.repo_path
        return self._run("init", str(target))

    def clone(self, repo_url: str, directory: str = None):
        target = directory or "."
        return self._run("clone", repo_url, target)

    def status(self):
        return self._run("status", "--porcelain")

    def add(self, path: str = "."):
        return self._run("add", path)

    def restore(self, path: str):
        return self._run("restore", path)

    def rm(self, path: str):
        return self._run("rm", path)

    def commit(self, message: str):
        return self._run("commit", "-m", message)

    def amend_commit(self, amend: bool = True):
        if amend:
            return self._run("commit", "--amend", "--no-edit")
        return self._run("commit", "--no-edit")

    def branch(self, name: str = None, delete: bool = False):
        if delete:
            return self._run("branch", "-D", name)
        if name:
            return self._run("branch", name)
        return self._run("branch", "-a")

    def checkout(self, name: str, create: bool = False):
        if create:
            return self._run("checkout", "-b", name)
        return self._run("checkout", name)

    def switch(self, name: str, create: bool = False):
        if create:
            return self._run("switch", "-c", name)
        return self._run("switch", name)

    def merge(self, branch: str, no_ff: bool = False):
        args = ["merge"]
        if no_ff:
            args.append("--no-ff")
        args.append(branch)
        return self._run(*args)

    def rebase(self, branch: str = None):
        if branch:
            return self._run("rebase", branch)
        return self._run("rebase", "--continue")

    def cherry_pick(self, commit_hash: str):
        return self._run("cherry-pick", commit_hash)

    def log(self, n: int = 10, oneline: bool = True):
        args = ["log"]
        if oneline:
            args.append("--oneline")
        args.append(f"-n{n}")
        return self._run(*args)

    def show(self, ref: str = "HEAD"):
        return self._run("show", ref)

    def diff(self, ref1: str = None, ref2: str = None, staged: bool = False):
        args = ["diff"]
        if staged:
            args.append("--staged")
        if ref1:
            args.append(ref1)
        if ref2:
            args.append(ref2)
        return self._run(*args)

    def blame(self, file_path: str):
        return self._run("blame", file_path)

    def tag(self, name: str, message: str = None, annotate: bool = False):
        if annotate and message:
            return self._run("tag", "-a", name, "-m", message)
        return self._run("tag", name)

    def remote(self, action: str, name: str = None, url: str = None):
        if action == "add" and name and url:
            return self._run("remote", "add", name, url)
        if action == "remove" and name:
            return self._run("remote", "remove", name)
        if action == "list" or action == "-v":
            return self._run("remote", "-v")
        return self._run("remote", action)

    def fetch(self, remote: str = "origin", all: bool = False):
        if all:
            return self._run("fetch", "--all")
        return self._run("fetch", remote)

    def pull(self, remote: str = "origin", branch: str = None):
        args = ["pull", remote]
        if branch:
            args.append(branch)
        return self._run(*args)

    def push(self, remote: str = "origin", branch: str = None, set_upstream: bool = False, tags: bool = False):
        args = ["push"]
        if set_upstream:
            args.append("-u")
        if tags:
            args.append("--tags")
        args.append(remote)
        if branch:
            args.append(branch)
        return self._run(*args)

    def reset(self, mode: str = "--soft", ref: str = "HEAD~1"):
        return self._run("reset", mode, ref)

    def revert(self, commit_hash: str, no_commit: bool = False):
        args = ["revert"]
        if no_commit:
            args.append("--no-commit")
        args.append(commit_hash)
        return self._run(*args)

    def stash(self, action: str = "save", pop: bool = False, apply: bool = False):
        if pop:
            return self._run("stash", "pop")
        if apply:
            return self._run("stash", "apply")
        if action == "save":
            return self._run("stash", "save")
        return self._run("stash", "list")

    def clean(self, dry_run: bool = False, force: bool = True):
        args = ["clean"]
        if dry_run:
            args.append("--dry-run")
        if force:
            args.append("-f")
        return self._run(*args)

    def gc(self, aggressive: bool = False):
        args = ["gc"]
        if aggressive:
            args.append("--aggressive")
        return self._run(*args)

    def fsck(self):
        return self._run("fsck")

    def reflog(self, n: int = 20):
        return self._run("reflog", f"-n{n}")

    def current_branch(self):
        result = self._run("branch", "--show-current")
        if result["status"] == "success":
            return {"status": "success", "branch": result["stdout"]}
        return result

    def is_repo(self):
        git_dir = self.repo_path / ".git"
        if git_dir.exists():
            return {"status": "success", "is_repo": True}
        return {"status": "success", "is_repo": False}

    def count_objects(self):
        return self._run("count-objects", "-v")

    def short_status(self):
        return self._run("status", "-s")
