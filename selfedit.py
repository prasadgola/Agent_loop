import pathlib, subprocess, sys, json, urllib.request, re


# Body
Path = pathlib.Path(__file__).resolve()
key = (Path.parent / "key.txt").read_text().strip()

Initial_food = "Create self sustaining intelligence army of agents working together in unision with memory using all python properties and compute without syntax error\n"

# Brain connection
req = urllib.request.Request("https://api.anthropic.com/v1/messages",json.dumps({"model": "claude-sonnet-4-6","max_tokens": 64000,"messages": [{"role": "user", "content": Initial_food + Path.read_text()}],}).encode(),
    headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
)


# Brain signals unpack
code = json.load(urllib.request.urlopen(req))["content"][0]["text"].strip()


# Filter brain signals
fence = "`" * 3
if fence in code:
    match = re.search(fence + r"(?:python)?\n(.*)" + fence, code, re.DOTALL)
    if match:
        code = match.group(1).strip()


# put brain signals into action
Path.write_text(code + "\n")
subprocess.run([sys.executable, str(Path)])