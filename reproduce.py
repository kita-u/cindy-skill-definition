#!/usr/bin/env python3
"""NL -> CindyScript using YOUR Gemini API key and the published skill.

This is a minimal stand-in for the authors' server-side proxy.
It does not embed a key. Set GEMINI_API_KEY in the environment.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

MODEL = "gemini-3.5-flash"
ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    + MODEL
    + ":generateContent"
)
SKILL_FILE = Path(__file__).with_name("skill-definition.md")


def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        sys.exit(
            "Set GEMINI_API_KEY to your own key. This repository does not ship one."
        )

    prompt = " ".join(sys.argv[1:]).strip() or "Construct a regular pentagon"
    skill = SKILL_FILE.read_text(encoding="utf-8")

    payload = {
        "system_instruction": {"parts": [{"text": skill}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 16384,
        },
    }
    url = ENDPOINT + "?" + urllib.parse.urlencode({"key": api_key})
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        sys.exit(exc.read().decode("utf-8", errors="replace") or str(exc))

    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text = "".join(
        p.get("text", "") for p in parts if p.get("text") and not p.get("thought")
    )
    finish = data.get("candidates", [{}])[0].get("finishReason")
    print(text)
    if finish:
        print("\n[finishReason: %s]" % finish, file=sys.stderr)


if __name__ == "__main__":
    main()
