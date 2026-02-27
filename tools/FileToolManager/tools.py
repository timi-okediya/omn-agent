from .manager import FileToolManager
from langchain_core.tools import tool

manager = FileToolManager()

@tool
def create_file(path: str, overwrite: bool = False, create_parents: bool = False):
    """Create a new file at the exact provided absolute or relative path. Fail if the file already exists unless overwrite=true is explicitly provided. Do not create parent directories unless create_parents=true is explicitly provided. Return success status and full resolved path."""
    return manager.create_file(
        path=path,
        overwrite=overwrite,
        create_parents=create_parents
    )

@tool
def read_file(path: str):
    """Read and return the full textual contents of the file at the exact provided path. Fail if the file does not exist, is a directory, or is not readable as text. Do not truncate content."""
    return manager.read_file(
        path=path
    )


@tool
def write_file(path: str, content: str, overwrite: bool = False, create_if_missing: bool = True):
    """Write provided full content to the file at the exact path. Overwrite existing content only if overwrite=true is explicitly provided. Fail if file does not exist and create_if_missing=false."""
    return manager.write_file(
        path=path,
        content=content,
        overwrite=overwrite,
        create_if_missing=create_if_missing
    )
