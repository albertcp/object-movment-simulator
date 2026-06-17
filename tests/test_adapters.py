from __future__ import annotations

import json
from pathlib import Path

import pytest

from adapter.console_adapter import ConsoleAdapter
from adapter.file_adapter import FileAdapter
from adapter.json_adapter import JsonAdapter
from adapter.network_adapter import NetworkAdapter
from logic.messages import PositionMessage


@pytest.fixture
def message() -> PositionMessage:
    return PositionMessage(
        object_id="c1",
        x=50.0,
        y=100.0,
        timestamp=1.5,
    )


class TestJsonAdapter:
    def test_send_to_stdout(
        self, message: PositionMessage, capsys: pytest.CaptureFixture[str]
    ) -> None:
        adapter = JsonAdapter()
        adapter.send(message)
        captured = capsys.readouterr()
        data = json.loads(captured.out.strip())
        assert data["object_id"] == "c1"
        assert data["x"] == 50.0
        assert data["y"] == 100.0
        assert data["timestamp"] == 1.5

    def test_send_to_file(self, message: PositionMessage, tmp_path: Path) -> None:
        out = tmp_path / "positions.jsonl"
        adapter = JsonAdapter(output_path=str(out))
        adapter.send(message)
        lines = out.read_text().strip().split("\n")
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["object_id"] == "c1"

    def test_append_to_file(self, message: PositionMessage, tmp_path: Path) -> None:
        out = tmp_path / "positions.jsonl"
        adapter = JsonAdapter(output_path=str(out))
        adapter.send(message)
        adapter.send(message)
        lines = out.read_text().strip().split("\n")
        assert len(lines) == 2


class TestFileAdapter:
    def test_writes_json_line(self, message: PositionMessage, tmp_path: Path) -> None:
        out = tmp_path / "out.jsonl"
        adapter = FileAdapter(path=str(out))
        adapter.send(message)
        lines = out.read_text().strip().split("\n")
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["object_id"] == "c1"

    def test_appends_multiple(self, message: PositionMessage, tmp_path: Path) -> None:
        out = tmp_path / "out.jsonl"
        adapter = FileAdapter(path=str(out))
        adapter.send(message)
        adapter.send(message)
        adapter.send(message)
        assert len(out.read_text().strip().split("\n")) == 3

    def test_accepts_pathlib_path(self, message: PositionMessage, tmp_path: Path) -> None:
        out = tmp_path / "out.jsonl"
        adapter = FileAdapter(path=out)
        adapter.send(message)
        assert out.exists()


class TestConsoleAdapter:
    def test_prints_formatted(
        self, message: PositionMessage, capsys: pytest.CaptureFixture[str]
    ) -> None:
        adapter = ConsoleAdapter()
        adapter.send(message)
        captured = capsys.readouterr()
        assert "c1" in captured.out
        assert "50.00" in captured.out
        assert "100.00" in captured.out
        assert "1.500" in captured.out


class TestNetworkAdapter:
    def test_raises_not_implemented(self, message: PositionMessage) -> None:
        adapter = NetworkAdapter(host="localhost", port=9999)
        with pytest.raises(NotImplementedError, match="NetworkAdapter not implemented"):
            adapter.send(message)
