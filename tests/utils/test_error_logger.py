"""Tests for the centralized error and warning logger."""

from pathlib import Path
import re
import sys

from src.utils.error_logger import ErrorLogger, ErrorLogStream

TIMESTAMP_PATTERN = re.compile(
    r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] "
)


def test_error_logger_direct_log(tmp_path: Path) -> None:
    """ErrorLogger.log writes a timestamped line to the file."""
    log_file = tmp_path / "errors.log"
    ErrorLogger.log("Test warning message", log_path=str(log_file))

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "Test warning message" in content
    assert TIMESTAMP_PATTERN.match(content) is not None


def test_error_logger_appends_across_calls(tmp_path: Path) -> None:
    """Successive logs append to the existing log file."""
    log_file = tmp_path / "errors.log"
    ErrorLogger.log("First warning", log_path=str(log_file))
    ErrorLogger.log("Second warning", log_path=str(log_file))

    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    assert "First warning" in lines[0]
    assert "Second warning" in lines[1]
    assert TIMESTAMP_PATTERN.match(lines[0]) is not None
    assert TIMESTAMP_PATTERN.match(lines[1]) is not None


def test_error_logger_multiline_message(tmp_path: Path) -> None:
    """Multiline messages get timestamps on every non-empty line."""
    log_file = tmp_path / "errors.log"
    ErrorLogger.log("Line 1\nLine 2\nLine 3", log_path=str(log_file))

    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3
    for idx, expected in enumerate(["Line 1", "Line 2", "Line 3"]):
        assert expected in lines[idx]
        assert TIMESTAMP_PATTERN.match(lines[idx]) is not None


def test_error_logger_install_and_uninstall(tmp_path: Path) -> None:
    """Install redirects sys.stderr and uninstall restores original stream."""
    log_file = tmp_path / "errors.log"
    original_stderr = sys.stderr

    try:
        ErrorLogger.install(str(log_file))
        assert ErrorLogger.is_installed() is True
        assert sys.stderr != original_stderr

        print("Captured stderr message", file=sys.stderr)
        sys.stderr.flush()
    finally:
        ErrorLogger.uninstall()

    assert ErrorLogger.is_installed() is False
    assert sys.stderr == original_stderr

    content = log_file.read_text(encoding="utf-8")
    assert "Captured stderr message" in content
    assert TIMESTAMP_PATTERN.match(content) is not None


def test_error_log_stream_buffering(tmp_path: Path) -> None:
    """ErrorLogStream buffers partial writes until a newline is sent."""
    log_file = tmp_path / "stream.log"
    stream = ErrorLogStream(str(log_file))

    stream.write("Hello ")
    assert not log_file.exists() or log_file.read_text() == ""

    stream.write("World!\n")
    content = log_file.read_text(encoding="utf-8")
    assert "Hello World!" in content
    assert TIMESTAMP_PATTERN.match(content) is not None


def test_error_log_stream_flush_partial(tmp_path: Path) -> None:
    """Flushing an incomplete line writes it out with a timestamp."""
    log_file = tmp_path / "stream_flush.log"
    stream = ErrorLogStream(str(log_file))

    stream.write("Incomplete line")
    stream.flush()

    content = log_file.read_text(encoding="utf-8")
    assert "Incomplete line" in content
    assert TIMESTAMP_PATTERN.match(content) is not None
