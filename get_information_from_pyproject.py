

import tomllib
from pathlib import Path

# Path to your pyproject.toml
pyproject_path = Path("pyproject.toml")

with open(pyproject_path, "rb") as f:
    data = tomllib.load(f)

# Access specific information
project_name = data["project"]["name"]
version = data["project"]["version"]

source_pdf_path = data['source_pdf_details']['source_path']