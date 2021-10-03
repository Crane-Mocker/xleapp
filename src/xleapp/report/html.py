import importlib
import shutil
import typing
from pathlib import Path
from typing import Optional, Union

import xleapp.artifacts as artifacts
import xleapp.globals as g
import xleapp.report.templating as templating

if typing.TYPE_CHECKING:
    from typing import Optional, Union


def copy_static_files() -> None:
    """Copies static files to report folder.

    Returns:
        None
    """
    html_report_root = Path(importlib.util.find_spec(__name__).origin).parent
    static_folder = html_report_root / "_static"
    report_folder = g.report_folder / "_static"
    logo = report_folder / "logo.jpg"

    if not logo.exists():
        shutil.copytree(static_folder, report_folder, dirs_exist_ok=True)


def generate_index(
    artifact_list: dict,
    report_folder: Path,
    log_folder: Path,
    extraction_type: str,
    processing_time: float,
) -> None:

    nav = templating.generate_nav(report_folder, artifacts.selected(artifact_list))

    index_page = templating.Index(
        report_folder,
        log_folder,
        extraction_type,
        processing_time,
    )
    index_page.navigation = nav
    index_file = report_folder / "index.html"
    index_file.write_text(index_page.html())


def generate_artifacts(
    artifact_list: dict,
    report_folder: Path,
):

    selected_artifacts = artifacts.selected(artifact_list)
    nav = templating.generate_nav(report_folder, selected_artifacts)

    for name, artifact in selected_artifacts:
        artifact.html_report.navigation = nav
        artifacts.generate_report(name, artifact, report_folder)
