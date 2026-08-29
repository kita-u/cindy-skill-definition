#!/usr/bin/env python3
"""Serve this folder and open try.html in a browser.

Regenerates skill-definition.js from skill-definition.md first.
"""
from __future__ import annotations

import json
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

HERE = Path(__file__).resolve().parent
PORT = 8765


def write_skill_js() -> None:
    skill = (HERE / "skill-definition.md").read_text(encoding="utf-8")
    js = (
        "/* generated from skill-definition.md; do not edit by hand */\n"
        "window.CINDY_SKILL = " + json.dumps(skill, ensure_ascii=False) + ";\n"
    )
    (HERE / "skill-definition.js").write_text(js, encoding="utf-8", newline="\n")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))


def main() -> None:
    write_skill_js()
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = "http://127.0.0.1:%d/try.html" % PORT
    print("Serving", HERE)
    print("Open", url)
    print("Paste your own Gemini API key on the page. Ctrl+C to stop.")
    webbrowser.open(url)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
