import re

import toml


def get_versions_from_pyproject(file_path="pyproject.toml"):
    with open(file_path, "r") as file:
        pyproject_data = toml.load(file)
    python_version = pyproject_data["tool"]["poetry"]["dependencies"].get(
        "python"
    )
    fastapi_version = pyproject_data["tool"]["poetry"]["dependencies"].get(
        "fastapi"
    )
    return python_version, fastapi_version


def replace_line_in_file(file_path, line_number, new_content):
    with open(file_path, "r") as file:
        lines = file.readlines()
    if line_number <= len(lines):
        lines[line_number - 1] = f"{new_content}\n"
    with open(file_path, "w") as file:
        file.writelines(lines)


coverage_file = ".tox/report/coverage.xml"
try:
    with open(coverage_file, "r") as f:
        coverage_content = f.read()
        coverage_match = re.search(
            r'<coverage.*line-rate="([\d.]+)"', coverage_content
        )
        coverage_percentage = (
            float(coverage_match.group(1)) * 100 if coverage_match else 0
        )
except Exception:
    coverage_percentage = 0.0

badge_color = "green" if coverage_percentage >= 90 else "red"


new_coverage_badge = f'    "https://img.shields.io/badge/{coverage_percentage:.2f}%25-{badge_color}?style=flat&logo=checkmarx&logoColor=white&label=Coverage&labelColor=gray"'
replace_line_in_file("README.md", 27, new_coverage_badge)
python_version, fastapi_version = get_versions_from_pyproject()
new_python_badge = f'    "https://img.shields.io/badge/{python_version}-2596be?style=flat&logo=Python&logoColor=white&label=Python&labelColor=gray"'
replace_line_in_file("README.md", 22, new_python_badge)
# new_fastapi_badge = f'    "https://img.shields.io/badge/{fastapi_version}-green?style=flat&logo=fastapi&logoColor=white&label=FastAPI&labelColor=gray"'
# replace_line_in_file("README.md", 26, new_fastapi_badge)
