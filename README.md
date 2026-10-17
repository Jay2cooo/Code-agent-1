# Agent Z
A beginner-friendly, supervised coding agent based on your Claude template.
Claude chooses commands; Python executes them in Docker and returns the results.
You approve every command. Guidance from this ChatGPT conversation can be pasted
into Agent Z when it asks a question. There is no automatic connection to this chat.

## Windows setup (PowerShell)
Install Python 3.12+, Git for Windows, and Docker Desktop with Linux containers.
Start Docker Desktop. Restart PowerShell after installation, then check:

```powershell
py --version
git --version
docker info
```

Clone your repository after these files have been pushed:

```powershell
git clone https://github.com/Jay2cooo/Code-agent-1.git
cd Code-agent-1
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
docker pull python:3.12-slim
```
No virtual environment activation or execution-policy change is necessary.
Create an Anthropic API key in your Anthropic console. API usage requires API
billing; do not put your key in the repository or paste it into a chat.
Enter it without putting the literal key in PowerShell history:

```powershell
$secret = Read-Host 'Anthropic API key' -AsSecureString
$env:ANTHROPIC_API_KEY = [System.Net.NetworkCredential]::new('', $secret).Password
.\.venv\Scripts\python.exe agent.py "Create fizzbuzz.py with fizzbuzz(n) returning a string. Test 1, 3, 5, and 15 using unittest, then run the tests."
```
Review each proposed command and type y to run it. Any other answer denies it.
Each task gets a fresh runs/<id>/workspace folder. Logs live alongside it in
trace.jsonl. Inspect files and test results yourself: a model ending its turn is
not independent proof that the task passed. Runs are ignored by Git.

Optional limits:
```powershell
.\.venv\Scripts\python.exe agent.py "Your task" --steps 10 --timeout 30
```
The model defaults to claude-sonnet-5-5; override with --model if your account
requires another available model. See https://platform.claude.com/docs/en/models/overview.
Run local tests (no Docker/API required):
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## What changed from the template
- Clean Python formatting and Windows instructions.
- File reads and edits happen via shell commands inside Docker too.
- Dedicated disposable workspace per task, separate from agent source and logs.
- No network, read-only container root, non-root user, limited CPU/RAM/processes.
- Bounded captured output, command timeout, and cleanup on interruption.
- Errors and step limits are explicit; logs record tool results.
- No unattended or network-enabled mode in this first version.

Docker is a useful isolation layer, not a perfect security boundary. The mounted
workspace is writable and has no disk quota, so use disposable tasks and monitor
host disk space. Keep secrets out of task files; tool output is sent to Claude.
Packages installed outside /workspace disappear between commands. Start with
Python standard-library tasks. The API key stays in the controller process and
is not passed to the sandbox. The controller still needs internet for the API.

## Learning path
1. Read SYSTEM and TOOLS to understand instructions and tool definitions.
2. Read run_agent to see the request → tool → result loop.
3. Read docker_command and run_command to understand execution boundaries.
4. Run FizzBuzz, inspect trace.jsonl, then try a small bug-fixing task.

## Validation status
Python syntax and offline unit tests can be checked without Docker. Live Docker
execution and a real Claude API task must also be tested on your Windows machine.
