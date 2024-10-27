import os
import pathlib as pl
import cookiecutter.repository as ck


def extract_template_name(template: str) -> str:
    """
    Extracts the name of the template from either a local directory path or a remote URL.
    
    For local directory paths, it returns the last directory name. For remote Git URLs,
    it extracts the repository name from the URL by removing any extensions.
    
    Args:
        template (str): The template location, which can be a local directory path 
                        or a remote URL (e.g., a Git repository URL).
                        
    Returns:
        str: The extracted template name, which is the last part of the local directory path 
             or the remote URL, typically the directory or repository name, without extensions.
               
    Raises:
        ValueError: If the input is neither a valid local directory path nor a Git repository URL.
        
    Example:
        - Input: "/home/user/projects/my-template" -> Output: "my-template"
        - Input: "https://github.com/user/my-repo.git" -> Output: "my-repo"
    """

    # Check if it's a valid Git repository URL
    if ck.is_repo_url(template):
        # Extract the repository name from the URL
        template_name = template.rstrip("/").split("/")[-1]
        return template_name.replace(".git", "").replace(".", "")
    

    path = pl.Path(template)

    if not os.path.exists(template):
        raise ValueError("The input must be an existing directory.")

    if not os.path.isdir(template):
        return path.name
    
    raise ValueError("The input must be either a valid local directory or a Git repository URL.")
