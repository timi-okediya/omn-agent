from .manager import GitToolManager
from langchain_core.tools import tool

git_manager = GitToolManager()


@tool
def git_init(path: str = None):
    """Initialize a new git repository."""
    return git_manager.init(path=path)


@tool
def git_clone(repo_url: str, directory: str = None):
    """Clone a remote repository."""
    return git_manager.clone(repo_url=repo_url, directory=directory)


@tool
def git_status():
    """Get the current git status."""
    return git_manager.status()


@tool
def git_add(path: str = "."):
    """Stage files for commit."""
    return git_manager.add(path=path)


@tool
def git_restore(path: str):
    """Restore a file to last committed state."""
    return git_manager.restore(path=path)


@tool
def git_rm(path: str):
    """Remove a file from git and working directory."""
    return git_manager.rm(path=path)


@tool
def git_commit(message: str):
    """Commit staged changes."""
    return git_manager.commit(message=message)


@tool
def git_branch(name: str = None, delete: bool = False):
    """List, create, or delete branches."""
    return git_manager.branch(name=name, delete=delete)


@tool
def git_checkout(name: str, create: bool = False):
    """Switch branches or create new branch."""
    return git_manager.checkout(name=name, create=create)


@tool
def git_switch(name: str, create: bool = False):
    """Switch to a branch."""
    return git_manager.switch(name=name, create=create)


@tool
def git_merge(branch: str, no_ff: bool = False):
    """Merge a branch into current branch."""
    return git_manager.merge(branch=branch, no_ff=no_ff)


@tool
def git_rebase(branch: str = None):
    """Rebase current branch onto another."""
    return git_manager.rebase(branch=branch)


@tool
def git_log(n: int = 10):
    """Get commit history."""
    return git_manager.log(n=n)


@tool
def git_show(ref: str = "HEAD"):
    """Show a commit or file at a ref."""
    return git_manager.show(ref=ref)


@tool
def git_diff(ref1: str = None, ref2: str = None, staged: bool = False):
    """Show changes between commits."""
    return git_manager.diff(ref1=ref1, ref2=ref2, staged=staged)


@tool
def git_blame(file_path: str):
    """Show who changed each line of a file."""
    return git_manager.blame(file_path=file_path)


@tool
def git_tag(name: str, message: str = None):
    """Create or list tags."""
    return git_manager.tag(name=name, message=message)


@tool
def git_remote(action: str, name: str = None, url: str = None):
    """Manage remote repositories."""
    return git_manager.remote(action=action, name=name, url=url)


@tool
def git_fetch(remote: str = "origin"):
    """Fetch from remote."""
    return git_manager.fetch(remote=remote)


@tool
def git_pull(remote: str = "origin", branch: str = None):
    """Pull changes from remote."""
    return git_manager.pull(remote=remote, branch=branch)


@tool
def git_push(remote: str = "origin", branch: str = None, set_upstream: bool = False):
    """Push changes to remote."""
    return git_manager.push(remote=remote, branch=branch, set_upstream=set_upstream)


@tool
def git_reset(mode: str = "--soft", ref: str = "HEAD~1"):
    """Reset HEAD to a commit."""
    return git_manager.reset(mode=mode, ref=ref)


@tool
def git_stash(action: str = "save"):
    """Stash changes."""
    return git_manager.stash(action=action)


@tool
def git_stash_pop():
    """Apply and remove stashed changes."""
    return git_manager.stash(action="save", pop=True)


@tool
def git_current_branch():
    """Get current branch name."""
    return git_manager.current_branch()


@tool
def git_is_repo():
    """Check if directory is a git repository."""
    return git_manager.is_repo()


@tool
def git_clean(dry_run: bool = True):
    """Remove untracked files."""
    return git_manager.clean(dry_run=dry_run)


GIT_TOOLS = [
    git_init,
    git_clone,
    git_status,
    git_add,
    git_restore,
    git_rm,
    git_commit,
    git_branch,
    git_checkout,
    git_switch,
    git_merge,
    git_rebase,
    git_log,
    git_show,
    git_diff,
    git_blame,
    git_tag,
    git_remote,
    git_fetch,
    git_pull,
    git_push,
    git_reset,
    git_stash,
    git_stash_pop,
    git_current_branch,
    git_is_repo,
    git_clean,
]
