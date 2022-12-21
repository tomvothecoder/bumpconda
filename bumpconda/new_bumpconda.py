import glob
from typing import Dict

import yaml
from requests_html import HTMLSession

BASE_URL = "https://anaconda.org/conda-forge"
OMIT_PACKAGES = ["numba", "numpy"]
CONDA_ENV_DIR = "/home/vo13/E3SM-Project/e3sm_diags/conda-env/"


def main():
    env_files = get_env_files(CONDA_ENV_DIR)
    env_files = _update_deps(env_files)

    _update_env_files(env_files)


def get_env_files(dir):
    # Read the conda env yml files into a dictionary, with the key as the filepath
    # and the value as the contents.
    env_files: Dict[str, Dict[str, str]] = {
        path: {} for path in glob.glob(f"{dir}*.yml")
    }

    for filepath in env_files.keys():
        env_files[filepath] = _read_env_file(filepath)

    return env_files


def _read_env_file(filename):
    # FIXME: pyyaml does not preserve comments
    with open(filename, "r") as stream:
        return yaml.safe_load(stream)


def _update_deps(env_files):
    for filepath, contents in env_files.items():
        for index, dep in enumerate(contents["dependencies"]):
            if not isinstance(dep, str):
                continue

            # Only update pinned dependencies (e.g., "xarray=2022.12.0")
            if "=" in dep and ">" not in dep:
                dep_split = dep.strip().split("=")
                dep_name = dep_split[0]
                version = dep_split[1]
                new_version = _get_latest_version(dep_name)

                new_dep = dep.replace(version, new_version)
                env_files[filepath]["dependencies"][index] = new_dep

    return env_files


def _get_latest_version(dep: str) -> str:
    session = HTMLSession()
    response = session.get(f"{BASE_URL}/{dep}")

    try:
        return response.html.find(".subheader", first=True).text
    except AttributeError:
        raise AttributeError(
            f"Version text (.subheader) not found for {dep} in Anaconda link."
        )

def _update_env_files(env_files):
    for filepath, contents in env_files.items():
        with open(filepath, "w") as file:
            yaml.dump(contents, file)

        # Display the files
        with open(filepath) as fp:
            print(fp.read(), end="")

if __name__ == "__main__":
    main()
