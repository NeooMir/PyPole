# Low-level IPC transport and socket client for the Pole / NeoMir educational IDE.
# Handles automatic socket discovery, singleton connection lifecycles, and serializes
# JSON command and telemetry payloads between external environments and the Pole IDE.

import os
import sys
import json
import socket
from pathlib import Path
from typing import Optional, Dict, Any, Union
from .errors import PoleConnectionError


class PoleClient:
    # Singleton IPC client for sending performer commands and receiving states from Pole
    _instance: Optional['PoleClient'] = None

    def __init__(self, socket_path: Optional[str] = None):
        self.socket_path = socket_path or self._discover_socket()
        self._sock: Optional[socket.socket] = None

    @classmethod
    def default(cls) -> 'PoleClient':
        # Returns shared singleton client instance for current process
        if cls._instance is None:
            cls._instance = PoleClient()
        return cls._instance

    @staticmethod
    def _discover_socket() -> str:
        # Automatically locates active Pole socket in the environment
        env_sock = os.environ.get("NEOMIR_SOCKET") or os.environ.get("POLE_SOCKET")
        if env_sock and os.path.exists(env_sock):
            return env_sock

        candidates = []
        if env_sock:
            candidates.append(Path(env_sock))

        if sys.platform != "win32":
            runtime_dir = os.environ.get("XDG_RUNTIME_DIR", "/tmp")
            candidates.append(Path(runtime_dir) / "neomir.sock")
            candidates.append(Path(runtime_dir) / "pole.sock")
            candidates.append(Path("/tmp") / "neomir.sock")
            candidates.append(Path("/tmp") / "pole.sock")
        else:
            temp_dir = os.environ.get("TEMP", os.environ.get("TMP", "C:\\Temp"))
            candidates.append(Path(temp_dir) / "neomir.sock")
            candidates.append(Path(temp_dir) / "pole.sock")

        for p in candidates:
            if p.exists():
                return str(p)
        return str(candidates[0])

    def connect(self) -> socket.socket:
        # Connects to the Pole IDE socket
        if self._sock is not None:
            return self._sock

        target_path = self.socket_path
        if not os.path.exists(target_path):
            discovered = self._discover_socket()
            if os.path.exists(discovered):
                target_path = discovered
                self.socket_path = discovered
            else:
                raise PoleConnectionError(
                    f"Pole IPC socket not found at '{target_path}'. "
                    "Make sure the Pole application is currently running!"
                )

        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(target_path)
            self._sock = s
            return s
        except Exception as e:
            self._sock = None
            raise PoleConnectionError(
                f"Failed to connect to Pole socket ({target_path}): {e}. "
                "Ensure Pole is open and ready to receive commands."
            ) from e

    def send_command(self, cmd_or_payload: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        # Sends command payload to server and parses JSON response
        sock = self.connect()
        if isinstance(cmd_or_payload, str):
            payload = {"cmd": cmd_or_payload}
        else:
            payload = cmd_or_payload

        raw_req = json.dumps(payload) + "\n"
        try:
            sock.sendall(raw_req.encode("utf-8"))
            data = sock.recv(4096)
            if not data:
                self._sock = None
                raise PoleConnectionError("Connection to Pole was closed by the server.")

            line = data.decode("utf-8").strip()
            if line.startswith("{"):
                return json.loads(line)
            return {"status": "ok", "raw": line}
        except (socket.error, OSError) as e:
            self._sock = None
            raise PoleConnectionError(f"Error transmitting command to Pole: {e}") from e

    def close(self):
        # Closes active socket connection
        if self._sock is not None:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None
