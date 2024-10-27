import os
import pathlib as pl


def extract_template_name(template: str) -> str:
    """
    Extracts the name of the template from either a local file path or a remote URL.

    For local paths, it returns the last directory or file name. For remote Git URLs,
    it extracts the repository name from the URL by splitting on '.' and taking the first part.

    Args:
        template (str): The template location, which can be a local file path (Linux, MacOS, Windows)
                        or a remote URL (e.g., a Git repository URL).

    Returns:
        str: The extracted template name, which is the last part of the local path or the remote URL.
             - For local paths, it's the last folder or file name.
             - For remote URLs, it's the last part of the URL, typically the repository name,
               with any extensions removed.

    Example:
        - Input: "/home/user/projects/my-template" -> Output: "my-template"
        - Input: "https://github.com/user/my-repo.git" -> Output: "my-repo"
    """
    path = pl.Path(template)

    if path.is_absolute() or os.path.exists(template):
        return path.name
    else:
        template_name = template.rstrip("/").split("/")[-1]
        return template_name.split(".")[0]
