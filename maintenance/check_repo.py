"""Static checks for the course repository (no API calls, no notebook execution).

Run from the course folder:
    uv run --group dev python maintenance/check_repo.py

Checks:
  1. Notebook JSON is valid (nbformat schema) and uses the standard python3 kernel.
  2. Python code in notebooks and scripts parses.
  3. Every imported third-party module is declared for its Part in pyproject.toml.
  4. Tracked files and notebook outputs contain no likely secrets, account IDs or local paths.
  5. No Google Colab code or links, and no pip install paths: `uv sync` is the only setup path.
"""
import argparse
import ast
import json
import re
import subprocess
import sys
import tomllib
from importlib.metadata import packages_distributions
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PART_GROUP = {"Part1": "part1", "Part2": "part2", "Part3": "part3", "Part4": "part4"}
OPTIONAL_IMPORTS = {"langflow"}  # optional extras, not installed by `uv sync`
SECRET_PATTERNS = {
    "OpenAI-style key": r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}",
    "Groq key": r"\bgsk_[A-Za-z0-9]{20,}",
    "Tavily key": r"\btvly-[A-Za-z0-9-]{16,}",
    "AWS access key": r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b",
    "Langflow/Astra token": r"AstraCS:[A-Za-z0-9]{10,}",
    "AWS account ID in ARN": r"arn:aws:[a-z0-9-]*:[a-z0-9-]*:\d{12}:",
    "Hard-coded agent ID": r"agent(?:Alias)?Id\s*=\s*['\"][A-Z0-9]{10}['\"]",
    "Local Windows user path": r"[A-Za-z]:\\\\?Users\\\\?[A-Za-z0-9._-]+",
    "Local macOS/Linux home path": r"/(?:Users|home)/[a-z][a-z0-9._-]+/",
    "Instructor .env path": r"YTReusable",
}

problems = []


def problem(msg):
    problems.append(msg)
    print("  FAIL", msg)


def tracked_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [ROOT / line for line in out.splitlines() if (ROOT / line).exists()]


def strip_magics(source):
    """Blank out IPython magics and shell commands, including their backslash-continued lines."""
    out, continuing = [], False
    for line in source.splitlines():
        is_magic = continuing or line.lstrip().startswith(("%", "!"))
        continuing = is_magic and line.rstrip().endswith("\\")
        out.append("" if is_magic else line)
    return "\n".join(out)


def code_units(files):
    """Yield (path, label, source) for each notebook code cell and Python script."""
    for path in files:
        if path.suffix == ".ipynb":
            nb = json.loads(path.read_text(encoding="utf-8"))
            for i, cell in enumerate(nb["cells"]):
                if cell["cell_type"] == "code":
                    yield path, f"cell {i}", strip_magics("".join(cell["source"]))
        elif path.suffix == ".py":
            yield path, "script", path.read_text(encoding="utf-8")


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def check_notebooks(files):
    print("1. Notebook JSON and kernel metadata")
    import nbformat

    for path in files:
        if path.suffix != ".ipynb":
            continue
        nb = nbformat.read(path, as_version=4)
        try:
            nbformat.validate(nb)
        except nbformat.ValidationError as e:
            problem(f"{path.relative_to(ROOT)}: invalid notebook ({e.message})")
        kernel = nb.metadata.get("kernelspec", {}).get("name")
        if kernel != "python3":
            problem(f"{path.relative_to(ROOT)}: kernelspec is {kernel!r}, expected 'python3'")


def check_parse(files):
    print("2. Python syntax")
    for path, label, source in code_units(files):
        try:
            ast.parse(source)
        except SyntaxError as e:
            problem(f"{path.relative_to(ROOT)} {label}: {e.msg} (line {e.lineno})")


def check_imports(files):
    print("3. Imports declared for each Part")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    groups = project["dependency-groups"]
    shared = {normalize(re.split(r"[<>=!~ ;\[]", d)[0]) for d in project["project"]["dependencies"]}
    module_to_dists = packages_distributions()
    for path, label, source in code_units(files):
        part = path.relative_to(ROOT).parts[0]
        if part not in PART_GROUP:
            continue
        declared = shared | {normalize(re.split(r"[<>=!~ ;\[]", d)[0]) for d in groups[PART_GROUP[part]]}
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue  # already reported by check 2
        for node in ast.walk(tree):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else (
                [node.module] if isinstance(node, ast.ImportFrom) and node.module and node.level == 0 else [])
            for name in names:
                top = name.split(".")[0]
                if top in sys.stdlib_module_names or top in OPTIONAL_IMPORTS:
                    continue
                dists = {normalize(d) for d in module_to_dists.get(top, [])}
                if not dists:
                    problem(f"{path.relative_to(ROOT)} {label}: '{top}' is not installed in this environment")
                elif not dists & declared:
                    problem(f"{path.relative_to(ROOT)} {label}: '{top}' ({', '.join(sorted(dists))}) "
                            f"is not declared in dependency group {PART_GROUP[part]}")


def check_security(files):
    print("4. Secrets, account identifiers and local paths")
    for path in files:
        if path.suffix in {".lock"} or path.name == "check_repo.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                problem(f"{path.relative_to(ROOT)}:{line}: possible {label} (value not shown)")


COLAB_PATTERNS = {
    "Colab import": r"google\.colab",
    "Colab link or badge": r"colab\.research\.google\.com",
    "Colab install pins": r"COLAB_PACKAGES|IN_COLAB",
    "retired *_Colab.ipynb notebook": r"[\w./-]*_Colab\.ipynb",
    "pip install instruction or magic": r"pip install|%pip|!pip",
}


def check_no_colab(files):
    print("5. No Google Colab code or links, no pip install paths")
    for path in files:
        if path.name == "check_repo.py":
            continue
        if path.name == "requirements.txt":
            problem(f"{path.relative_to(ROOT)}: requirements files are retired - use pyproject.toml and uv.lock")
            continue
        if path.suffix == ".ipynb" and path.stem.endswith("_Colab"):
            problem(f"{path.relative_to(ROOT)}: retired duplicate notebook is still tracked")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in COLAB_PATTERNS.items():
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                problem(f"{path.relative_to(ROOT)}:{line}: {label} ({match.group(0)})")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args()
    files = tracked_files()
    check_notebooks(files)
    check_parse(files)
    check_imports(files)
    check_security(files)
    check_no_colab(files)
    print(f"\n{len(problems)} problem(s) found." if problems else "\nAll checks passed.")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
