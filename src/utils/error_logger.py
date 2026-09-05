"""Error logging and stream redirection utilities for Pac-Man."""

from datetime import datetime
import io
import sys
from typing import TextIO


def _write_timestamped_lines(log_path: str, lines: list[str]) -> None:
    """Append timestamped non-empty lines to the target log file."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(log_path, "a", encoding="utf-8") as file:
            for line in lines:
                trimmed = line.strip()
                if trimmed:
                    file.write(f"[{now_str}] {trimmed}\n")
    except Exception:
        pass


class ErrorLogStream(io.TextIOBase):
    """Stream wrapper that writes timestamped messages to a log file."""

    def __init__(self, log_path: str = "errors.log") -> None:
        """Initialize the stream wrapper with target log file path."""
        super().__init__()
        self.log_path = log_path
        self._buffer: str = ""

    def write(self, s: str) -> int:
        """Buffer and write incoming messages into the log file."""
        if not s:
            return 0

        self._buffer += s
        if "\n" in self._buffer:
            lines = self._buffer.split("\n")
            self._buffer = lines[-1]
            _write_timestamped_lines(self.log_path, lines[:-1])
        return len(s)

    def flush(self) -> None:
        """Flush any remaining buffered text into the log file."""
        if self._buffer.strip():
            _write_timestamped_lines(self.log_path, [self._buffer])
        self._buffer = ""


class ErrorLogger:
    """Manager for error logging and stderr stream redirection."""

    _original_stderr: TextIO | None = None
    _installed_stream: ErrorLogStream | None = None
    _log_path: str = "errors.log"

    @classmethod
    def install(cls, log_path: str = "errors.log") -> None:
        """Redirect sys.stderr exclusively to the specified log file."""
        cls._log_path = log_path
        if cls._original_stderr is None:
            cls._original_stderr = sys.stderr
        cls._installed_stream = ErrorLogStream(log_path=log_path)
        sys.stderr = cls._installed_stream

    @classmethod
    def uninstall(cls) -> None:
        """Restore original sys.stderr stream."""
        if cls._installed_stream is not None:
            cls._installed_stream.flush()
            cls._installed_stream = None
        if cls._original_stderr is not None:
            sys.stderr = cls._original_stderr
            cls._original_stderr = None

    @classmethod
    def log(cls, message: str, log_path: str | None = None) -> None:
        """Write a timestamped message directly to the log file."""
        target_path = log_path or cls._log_path
        _write_timestamped_lines(target_path, message.strip().splitlines())

    @classmethod
    def is_installed(cls) -> bool:
        """Return True if sys.stderr is currently redirected."""
        return cls._installed_stream is not None
