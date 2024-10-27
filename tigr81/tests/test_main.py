from typer.testing import CliRunner

from tigr81.main import app

runner = CliRunner()

def test_version():
    """Test the version command."""
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0