#!/usr/bin/env python3
import pathlib, subprocess, sys, json, urllib.request

SELF = pathlib.Path(__file__).resolve()
API_KEY = (SELF.parent / "key.txt").read_text().strip()      # key is read from key.txt, never written here
src = SELF.read_text()                                        # read myself

body = json.dumps({
    "model": "claude-sonnet-4-6",          # opus-4-8 = strongest, haiku-4-5-20251001 = cheapest
    "max_tokens": 8192,                     # must be big enough to return the WHOLE file
    "messages": [{"role": "user",
        "content": "Edit this Python code. Return only the new code, no prose:\n\n" + src}],
}).encode()
req = urllib.request.Request(                                 # ask the model
    "https://api.anthropic.com/v1/messages", body,
    headers={"x-api-key": API_KEY,
             "anthropic-version": "2023-06-01",
             "content-type": "application/json"})
data = json.load(urllib.request.urlopen(req))
resp = "".join(b["text"] for b in data["content"] if b["type"] == "text")

code = resp.strip()                                           # strip ``` fences if added
if code.startswith("```"):
    code = code.split("\n", 1)[1].rsplit("```", 1)[0]

SELF.write_text(code.strip() + "\n")                          # overwrite myself
subprocess.run([sys.executable, str(SELF)])                   # rerun the new version