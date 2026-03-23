from pathlib import Path
import tomllib

from click.testing import CliRunner

from unrealhub import __version__
from unrealhub.cli import main


def test_cli_version_matches_project_metadata():
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with pyproject.open("rb") as f:
        project = tomllib.load(f)

    assert __version__ == project["project"]["version"]


def test_cli_reports_version():
    runner = CliRunner()

    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert f"unrealhub, version {__version__}" in result.output
