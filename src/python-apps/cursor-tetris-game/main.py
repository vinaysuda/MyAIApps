import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial


def main() -> None:
    """
    MVP runner: serves the static Tetris frontend and opens it in a browser.

    Run:
      py main.py
    """

    here = os.path.dirname(os.path.abspath(__file__))
    web_dir = os.path.join(here, "web")
    index_path = os.path.join(web_dir, "index.html")

    if not os.path.isdir(web_dir):
        raise FileNotFoundError(f"Missing web directory: {web_dir}")
    if not os.path.isfile(index_path):
        raise FileNotFoundError(f"Missing web entrypoint: {index_path}")

    port = 8000
    # Optional: `python main.py 9000`
    if len(sys.argv) >= 2:
        try:
            port = int(sys.argv[1])
        except ValueError:
            raise ValueError(f"Invalid port: {sys.argv[1]}")

    handler = partial(SimpleHTTPRequestHandler, directory=web_dir)
    httpd = HTTPServer(("127.0.0.1", port), handler)
    url = f"http://127.0.0.1:{port}/index.html"

    print(f"Serving Tetris on {url}")
    # Best-effort: if browser launch fails, server still runs.
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
