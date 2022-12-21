"""Main module."""
#%%
"""A quick script put together in 30 minutes to make it less tedious to update
conda env `.yml` files with the latest dependencies.
Make sure to create an environment with the required dependencies.
(e.g., mamba create -n update-env -c conda-forge python=3.10 pandas requests-html pyyaml)
This script looks in the `/conda-env` directory for `.yml` files.
"""
import glob
from typing import Dict

import yaml
from requests_html import HTMLSession

# %%
# The base URL to search for packages (conda-forge channel).
BASE_URL = "https://anaconda.org/conda-forge"
# Files and packages to omit from being updated.
OMIT_FILES = ["./conda-env/ci.yml"]
OMIT_PACKAGES = ["numba", "numpy"]
CONDA_ENV_DIR = "/home/vo13/E3SM-Project/e3sm_diags/conda-env/"

#%%
def read_yaml_file(filename):
    with open(filename, "r") as stream:
        return yaml.safe_load(stream)


def get_latest_version(dep: str) -> str:
    session = HTMLSession()
    response = session.get(f"{BASE_URL}/{dep}")

    try:
        return response.html.find(".subheader", first=True).text
    except AttributeError:
        raise AttributeError(
            f"Version text (.subheader) not found for {dep} in Anaconda link."
        )


#%%
# Read the conda env yml files into a dictionary, with the key as the filepath
# and the value as the contents.
# FIXME: pyyaml does not preserve comments
env_files: Dict[str, Dict[str, str]] = {
    path: {} for path in glob.glob(f"{CONDA_ENV_DIR}*.yml") if path not in OMIT_FILES
}

for filepath in env_files:
    env_files[filepath] = read_yaml_file(filepath)

# %%
# Update the dependencies in each file.
for filepath, contents in env_files.items():
    for index, dep in enumerate(contents["dependencies"]):
        if isinstance(dep, str):
            dep = dep.strip()

            if ">=" in dep:
                dep = dep.split(">=")[0]
            elif "=" in dep:
                dep = dep.split("=")[0]
            elif ">" in dep:
                dep = dep.split(">")[0]
        else:
            continue

        if dep not in OMIT_PACKAGES:
            version = get_latest_version(dep)
            env_files[filepath]["dependencies"][index] = f"{dep}={version}"

# %%
# Update the files
for filepath, contents in env_files.items():
    with open(filepath, "w") as file:
        file.write(yaml.dump(contents, default_flow_style=False))

# %%
