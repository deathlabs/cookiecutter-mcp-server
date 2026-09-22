def rename_file(old_file_path: str, new_file_path: str) -> str:
    """Rename a file.

    Args:
        old_file_path (str): The current path of the file to be renamed.
        new_file_path (str): The new path for the file.

    Returns:
        A message indicating the file has been renamed.
    """
    return f"File renamed from {old_file_path} to {new_file_path}."
