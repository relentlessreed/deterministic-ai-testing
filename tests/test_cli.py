import json
from pathlib import Path

from mockllm.cli import main


def test_cli_help(capsys):
    assert main() == 1

    output = capsys.readouterr().out

    assert "init" in output
    assert "snapshot" in output
    assert "state" in output
    assert "dashboard" in output


def test_state_save_and_test(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    state_path = Path("state/current.json")

    monkeypatch.setattr(
        "sys.argv",
        [
            "mockllm",
            "state",
            "save",
            str(state_path),
            "--name",
            "checkout-agent",
            "--json",
            '{"step":"payment"}',
        ],
    )

    assert main() == 0

    data = json.loads(state_path.read_text())

    assert data["name"] == "checkout-agent"
    assert data["state"] == {"step": "payment"}

    monkeypatch.setattr(
        "sys.argv",
        [
            "mockllm",
            "state",
            "test",
            str(state_path),
            "--json",
            '{"step":"payment"}',
        ],
    )

    assert main() == 0
    assert "PASS" in capsys.readouterr().out


def test_init_command(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr("sys.argv", ["mockllm", "init"])

    assert main() == 0

    assert Path("scenarios/default.yaml").exists()
    assert Path("snapshots").exists()
    assert Path("tests/test_ai.py").exists()


def test_dashboard_command(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    Path("snapshots").mkdir()
    Path("snapshots/hello.json").write_text("{}")

    monkeypatch.setattr("sys.argv", ["mockllm", "dashboard"])

    assert main() == 0

    dashboard = Path("mockllm-dashboard.html")

    assert dashboard.exists()
    assert "hello.json" in dashboard.read_text()
