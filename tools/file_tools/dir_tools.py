from pathlib import Path
import os
from langchain_core.tools import tool


@tool
def create_folder(name: str) -> dict:
    """
        Use this tool ONLY when the user explicitly asks to create a new folder.
    """
    try:
        path = Path(name)

        # Check if the parent directory exists, otherwise create it
        parent_path = path.parent
        if not parent_path.exists():
            os.makedirs(parent_path)

        # Create or fail to create the new folder
        if path.exists():
            return {
                "status": "exists",
                "message": f"Folder '{name}' already exists."
            }
        else:
            path.mkdir(parents=True, exist_ok=False)

        return {
            "status": "created",
            "message": f"Folder '{name}' created successfully."
        }

    except Exception as e:
        # Handle exceptions and provide detailed messages
        return {
            "status": "error",
            "message": str(e)
        }


