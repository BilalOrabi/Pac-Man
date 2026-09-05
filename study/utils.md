# Utils Module (`src/utils/`)

## 1. Module Overview
The `utils` module implements centralized error interception and logging mechanisms required by project memory and 42 evaluation norms. It enforces silent console execution by redirecting standard error (`sys.stderr`) into `errors.log`, formatting every record with standard timestamp prefixes (`[YYYY-MM-DD HH:MM:SS] <message>`), and providing thread-safe direct logging for non-fatal runtime warnings (e.g. JSON bounds clamping and audio hardware failures).

---

## 2. File & Class Breakdown

### `error_logger.py`
Implements stream redirection wrappers and direct disk logging utilities.

| Function / Method / Class | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `_format_log_line` | `(timestamp: str, text: str) -> str` | *(Internal helper)* Formats an individual log entry with standardized timestamp prefix. |
| `_write_timestamped_lines` | `(log_path: str, lines: list[str]) -> None` | *(Internal helper)* Appends timestamped non-empty lines directly to disk with exception suppression. |
| `ErrorLogStream` | `io.TextIOBase` | Custom stream wrapper redirecting incoming text writes into timestamped disk log entries. |
| `ErrorLogStream._process_buffered_lines` | `(self) -> None` | *(Internal helper)* Splits accumulated buffer by newline delimiter and flushes completed lines. |
| `ErrorLogStream.write` | `(self, s: str) -> int` | Buffers incoming character streams and appends completed lines to `errors.log`. |
| `ErrorLogStream.flush` | `(self) -> None` | Flushes any remaining incomplete lines from memory buffer into the file. |
| `ErrorLogger.install` | `(cls, log_path: str = "errors.log") -> None` | Redirects `sys.stderr` exclusively to the specified log file to silence console clutter. |
| `ErrorLogger.uninstall` | `(cls) -> None` | Restores original `sys.stderr` stream back to default terminal standard error. |
| `ErrorLogger.log` | `(cls, message: str, log_path: str \| None = None) -> None` | Appends a timestamped warning or diagnostic message directly to the log file. |
| `ErrorLogger.is_installed` | `(cls) -> bool` | Queries whether standard error redirection is currently active. |

