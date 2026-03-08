from .manager import FileToolManager, DirectoryManager
from langchain_core.tools import tool

file_manager = FileToolManager()
dir_manager = DirectoryManager()

@tool
def create_file(path: str, overwrite: bool = False, create_parents: bool = False):
    """Create a new empty file. Returns success status and path."""
    return file_manager.create_file(path=path, overwrite=overwrite, create_parents=create_parents)

@tool
def read_file(path: str):
    """Read the full contents of a file. Returns the file content."""
    return file_manager.read_file(path=path)

@tool
def write_file(path: str, content: str, overwrite: bool = False):
    """Write content to a file. Creates parent directories if needed."""
    return file_manager.write_file(path=path, content=content, overwrite=overwrite, create_if_missing=True)

@tool
def append_to_file(path: str, content: str):
    """Append content to an existing file."""
    return file_manager.append_to_file(path=path, content=content)

@tool
def delete_file(path: str):
    """Delete a file or directory."""
    return file_manager.delete_file(path=path)

@tool
def list_directory(path: str = "."):
    """List contents of a directory."""
    return dir_manager.list_directory(path=path)

@tool
def create_directory(path: str):
    """Create a new directory."""
    return dir_manager.create_directory(path=path)

@tool
def delete_directory(path: str):
    """Delete a directory and all its contents."""
    return dir_manager.delete_directory(path=path)

@tool
def file_exists(path: str):
    """Check if a file or directory exists."""
    return file_manager.file_exists(path=path)

@tool
def get_file_info(path: str):
    """Get file metadata (size, dates, permissions)."""
    return file_manager.get_file_info(path=path)

@tool
def search_files(path: str, pattern: str):
    """Search for files containing a text pattern."""
    return dir_manager.search_files_by_content(path=path, pattern=pattern)

@tool
def find_files(path: str, name: str):
    """Find files by name (supports wildcards)."""
    return dir_manager.find_files_by_name(path=path, name=name)

@tool
def find_by_extension(path: str, ext: str):
    """Find all files with a specific extension."""
    return dir_manager.find_files_by_extension(path=path, ext=ext)

@tool
def copy_file(source: str, destination: str):
    """Copy a file or directory."""
    return file_manager.copy_file(path=source, new_path=destination)

@tool
def move_file(source: str, destination: str):
    """Move a file or directory."""
    return file_manager.move_file(path=source, new_path=destination)

@tool
def replace_in_file(path: str, old: str, new: str):
    """Replace text in a file."""
    return file_manager.replace_in_file(path=path, old=old, new=new)

@tool
def get_file_size(path: str):
    """Get file size in bytes."""
    return file_manager.get_file_size(path=path)

@tool
def count_lines(path: str):
    """Count lines in a file."""
    return file_manager.count_lines(path=path)

@tool
def validate_json(path: str):
    """Validate if a file contains valid JSON."""
    return file_manager.validate_json_file(path=path)

@tool
def read_json(path: str):
    """Read and parse a JSON file."""
    return file_manager.read_json(path=path)

@tool
def write_json(path: str, data: dict):
    """Write data to a JSON file."""
    return file_manager.write_json(path=path, data=data)

@tool
def calculate_hash(path: str, algorithm: str = "sha256"):
    """Calculate file hash (sha256, md5, sha1)."""
    return file_manager.calculate_file_hash(path=path, algorithm=algorithm)

@tool
def get_directory_tree(path: str = ".", max_depth: int = 3):
    """Get directory tree structure."""
    return dir_manager.get_directory_tree(path=path, max_depth=max_depth)


FILE_TOOLS = [
    create_file,
    read_file,
    write_file,
    append_to_file,
    delete_file,
    list_directory,
    create_directory,
    delete_directory,
    file_exists,
    get_file_info,
    search_files,
    find_files,
    find_by_extension,
    copy_file,
    move_file,
    replace_in_file,
    get_file_size,
    count_lines,
    validate_json,
    read_json,
    write_json,
    calculate_hash,
    get_directory_tree,
]
