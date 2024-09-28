import os

from agents.core.dto.response import Response


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


def create_file(file_path: str, content: str):
    if os.path.exists(file_path):
        read_content = read_file(file_path)
        return Response(f"The file {file_path} already exists with the following content: "
                        f"```{read_content}```", True)

    with open(file_path, 'w') as f:
        f.write(content)

    return Response(f"File {file_path} created with the content: ```{content}```", error=False)


def update_file(file_path: str, content: str):
    if not os.path.exists(file_path):
        return Response(f"The file {file_path} does not exists.", True)

    with open(file_path, 'w') as f:
        f.write(content)

    return Response(f"File {file_path} updated to the following content: ```{content}```.", error=False)


def scan_project(path: str):
    return recursive_scan(path)


def read_file(path: str):
    if not os.path.exists(path):
        return Response(f"The file {path} does not exists.", True)

    with open(path, 'r') as f:
        content = f.read()

    return Response(content, error=False)
