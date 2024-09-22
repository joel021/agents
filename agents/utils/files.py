
import os

def recursive_scan(current_path: str):
    folder_content = {}
    try:
        # List the contents of the directory
        for entry in os.listdir(current_path):
            full_path = os.path.join(current_path, entry)
            if os.path.isdir(full_path):
                # If entry is a folder, recursively scan it
                folder_content[entry] = recursive_scan(full_path)
            else:
                # If entry is a file, add it to the folder's list of files
                if "files" not in folder_content:
                    folder_content["files"] = []
                folder_content["files"].append(entry)
    except PermissionError:
        print(f"Permission Denied: {current_path}")
    return folder_content

