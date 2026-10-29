"""Expose a loopback-only host Ollama service to local Docker containers.

Run this in a host-networked container. The listener binds only to Docker's
host-gateway address, so the Ollama API stays off external host interfaces.
"""

import os
import socket
import socketserver
from threading import Thread


UPSTREAM = ("127.0.0.1", int(os.getenv("OLLAMA_UPSTREAM_PORT", "11434")))
LISTEN = (socket.gethostbyname("host.docker.internal"), int(os.getenv("OLLAMA_BRIDGE_PORT", "11435")))


class Bridge(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            upstream = socket.create_connection(UPSTREAM, timeout=5)
        except OSError:
            return
        with upstream:
            upstream.settimeout(None)

            def copy(source, target):
                try:
                    while chunk := source.recv(65536):
                        target.sendall(chunk)
                except OSError:
                    pass
                try:
                    target.shutdown(socket.SHUT_WR)
                except OSError:
                    pass

            incoming = Thread(target=copy, args=(self.request, upstream), daemon=True)
            incoming.start()
            copy(upstream, self.request)
            incoming.join(timeout=1)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(LISTEN, Bridge) as server:
        print(f"Ollama loopback bridge listening on {LISTEN[0]}:{LISTEN[1]}", flush=True)
        server.serve_forever()
