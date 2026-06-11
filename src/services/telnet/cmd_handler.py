import logging
import socket
import time

from src.core.configs import Settings

logger = logging.getLogger(__name__)

_CRLF = b"\r\n"


class CmdHandler:

    def __init__(self, settings: Settings) -> None:
        self._timeout  = settings.TELNET_TIMEOUT_MS / 1000
        self._max_retry = settings.TELNET_MAX_RETRIES

    def execute(self, camera_id: str, command: str, params: str | None) -> str:
        """
        Connects to the camera, sends the command, and returns the response.
        Performs up to max_retries attempts with increasing intervals.
        Throws a RuntimeError in case of a permanent failure.
        """
        host, port = self._parse_camera_id(camera_id)
        cmd_line = self._build_command(command, params)

        last_error: Exception | None = None

        for attempt in range(1, self._max_retry + 1):
            try:
                response = self._send(host, port, cmd_line)
                logger.info(
                    "Telnet OK | camera=%s command=%s attempt=%s",
                    camera_id, command, attempt,
                )
                return response
            except (OSError, TimeoutError) as e:
                last_error = e
                logger.warning(
                    "Telnet FAIL | camera=%s command=%s attempt=%s/%s erro=%s",
                    camera_id, command, attempt, self._max_retry, e,
                )
                if attempt < self._max_retry:
                    time.sleep(attempt)  # backoff simples: 1s, 2s, 3s...

        raise RuntimeError(
            f"Permanent failure after {self._max_retry} retries | "
            f"camera={camera_id} command={command} erro={last_error}"
        )

    def _send(self, host: str, port: int, cmd_line: bytes) -> str:
        """Open connection, send command and read response."""

        with socket.create_connection((host, port), timeout=self._timeout) as sock:
            self._wait_ready(sock)
            sock.sendall(cmd_line)
            return self._read_response(sock)

    def _wait_ready(self, sock: socket.socket) -> None:
        """
        Wait initial message of CMS 2.2:
        '<date> <time> CMS_Telner_API_<version> <hostname> <status>'
        Discard content - only garants when server already
        """
        self._read_until(sock, b"\n")

    def _read_response(self, sock: socket.socket) -> str:
        """Read until find last line - pattern CMS 2.2"""
        return self._read_until(sock, b"\n").decode("utf-8").strip()

    def _read_until(self, sock: socket.socket, delimiter: bytes) -> bytes:
        """Read byte-to-byte until find delimiter."""
        buf = b""
        while not buf.endswith(delimiter):
            chunk = sock.recv(1)
            if not chunk:
                raise RuntimeError("Connection closed from server before awnser")
            buf += chunk
        return buf

    @staticmethod
    def _build_command(command: str, params: str | None) -> bytes:
        """
        Build command string on CMS 2.2 format:
        '<command> [params]\r\n'

        """
        line = command if not params else f"{command} {params}"
        return (line + "\r\n").encode("utf-8")

    @staticmethod
    def _parse_camera_id(camera_id: str) -> tuple[str, int]:
        """
        Wait camera_id on format 'host:port' (ex: '192.168.1.10:4585').
        Standard port CMS 2.2: 4585.
        """
        if ":" in camera_id:
            host, port_str = camera_id.rsplit(":", 1)
            return host, int(port_str)
        return camera_id, 4585