#!/usr/bin/env python3
"""
Generate ABOUT files from a conda-lock.yml file.

- For each package in the conda-lock file, a <name>-<platform>.ABOUT file is generated.
- Additionally, an ABOUT file for the codebase itself is created.

Requirements:
    pip install pyyaml

Usage:
    python conda_lock_to_about.py
    # optionally:
    python conda_lock_to_about.py path/to/conda-lock.yml out_dir
"""

import sys
import os
from pathlib import Path
import urllib.parse

import yaml


def parse_conda_url_to_purl(url: str) -> dict:
    """
    Extract PURL and conda metadata from a conda package URL.
    Example URL:
      https://conda.anaconda.org/conda-forge/linux-64/zlib-1.2.8-3.tar.bz2
    """
    parsed = urllib.parse.urlparse(url)
    parts = parsed.path.strip("/").split("/")
    # Expected structure: [channel, subdir, filename]
    if len(parts) < 3:
        raise ValueError(f"Unexpected URL structure: {url}")

    channel = parts[-3]
    subdir = parts[-2]
    filename = parts[-1]

    # Detect file extension (.tar.bz2 or .conda)
    file_ext = None
    base = filename
    if base.endswith(".tar.bz2"):
        file_ext = "tar.bz2"
        base_no_ext = base[: -len(".tar.bz2")]
    elif base.endswith(".conda"):
        file_ext = "conda"
        base_no_ext = base[: -len(".conda")]
    else:
        # Fallback: split at first dot
        dot_idx = base.find(".")
        if dot_idx != -1:
            file_ext = base[dot_idx + 1 :]
            base_no_ext = base[:dot_idx]
        else:
            file_ext = ""
            base_no_ext = base

    # name-version-build
    tokens = base_no_ext.split("-")
    if len(tokens) >= 3:
        pkg_name = tokens[0]
        pkg_version = tokens[1]
        build = "-".join(tokens[2:])
    elif len(tokens) == 2:
        pkg_name, pkg_version = tokens
        build = ""
    else:
        pkg_name = tokens[0]
        pkg_version = ""
        build = ""

    purl = f"pkg:conda/{pkg_name}@{pkg_version}"
    qualifiers = []

    if channel:
        qualifiers.append(f"channel={channel}")
    if subdir:
        qualifiers.append(f"subdir={subdir}")
    if build:
        qualifiers.append(f"build={build}")
    if file_ext:
        qualifiers.append(f"type={file_ext}")

    if qualifiers:
        purl = purl + "?" + "&".join(qualifiers)

    return {
        "name": pkg_name,
        "version": pkg_version,
        "channel": channel,
        "subdir": subdir,
        "build": build,
        "type": file_ext,
        "purl": purl,
    }


def write_about_file(path: Path, fields: dict) -> None:
    """
    Write an ABOUT file with simple key: value lines.
    Multiline fields are written using YAML block syntax.
    """
    lines = []
    for key, value in fields.items():
        if value is None:
            continue
        if "\n" in str(value):
            lines.append(f"{key}: |")
            for line in str(value).splitlines():
                lines.append(f"  {line}")
        else:
            lines.append(f"{key}: {value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✔ Created ABOUT file: {path}")


def generate_package_about_files(lock_data: dict, out_dir: Path) -> None:
    """
    Create ABOUT files for every conda-managed package inside conda-lock.yml.
    """
    packages = lock_data.get("package", [])
    for pkg in packages:
        if pkg.get("manager") != "conda":
            continue

        name = pkg.get("name")
        version = pkg.get("version")
        platform = pkg.get("platform")
        url = pkg.get("url")

        if not url:
            print(f"⚠️  Package {name} ({platform}) has no URL – skipped.")
            continue

        meta = parse_conda_url_to_purl(url)

        about_fields = {
            "about_resource": name,
            "name": meta["name"] or name,
            "version": meta["version"] or version,
            "platform": platform,
            "download_url": url,
            "purl": meta["purl"],
            "package_manager": "conda",
            "conda_channel": meta["channel"],
            "conda_subdir": meta["subdir"],
            "conda_build": meta["build"],
        }

        filename = f"{name}-{platform}.ABOUT"
        out_path = out_dir / filename
        write_about_file(out_path, about_fields)


def generate_codebase_about(out_dir: Path) -> None:
    """
    Create an ABOUT file for the codebase itself.
    This contains metadata for the C-zlib-Demo project.
    """
    about_fields = {
        "about_resource": ".",
        "name": "c-zlib-demo",
        "version": "0.1.0",
        "download_url": "https://github.com/SecuraPoint/C-zlib-Demo/archive/refs/heads/main.zip",
        "vcs_url": "https://github.com/SecuraPoint/C-zlib-Demo.git",
        "summary": "Demo C project using zlib for SBOM/SCA and ScanCode.io experiments.",
        "license_expression": "",
    }

    out_path = out_dir / "c-zlib-demo.ABOUT"
    write_about_file(out_path, about_fields)


def main():
    lock_path = Path("conda-lock.yml")
    out_dir = Path("about")

    if len(sys.argv) >= 2:
        lock_path = Path(sys.argv[1])
    if len(sys.argv) >= 3:
        out_dir = Path(sys.argv[2])

    if not lock_path.is_file():
        print(f"❌ conda-lock file not found: {lock_path}")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    with lock_path.open("r", encoding="utf-8") as f:
        lock_data = yaml.safe_load(f)

    generate_package_about_files(lock_data, out_dir)
    generate_codebase_about(out_dir)

    print("🎉 Done. ABOUT files written to:", out_dir.resolve())


if __name__ == "__main__":
    main()
