# Coding Agent

A simple coding agent powered by Google Gemini (`gemini-2.5-flash`) that autonomously reads, writes, and executes code within a sandboxed directory.
This is just a toy project to demonstrate how coding models work, and not meant for production usage.

## Setup

Requires Python 3.12+ and [uv](https://github.com/astral-sh/uv).

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```

## Usage

```bash
uv run main.py "your prompt here"
uv run main.py "your prompt here" --info   # verbose: show token counts and function call args/results
```

### Tests

```bash
uv run tests.py
```

## Example:
Modify `calculator.py` to have a higher precedence than other operations.
Then, run:
```bash
uv run main.py "There is a bug in the calculator.py function that needs to be fixed. For some reason, addition is happening before other operations, causing incorrect responses."
```
The agent should be able to solve this easily.

## Overview

`main.py` runs the agentic loop (up to 20 iterations).
Each iteration: 
1. Calls the Gemini model
2. Collects function calls
3. Executes them
4. Appends results to the message history
5. And loops until the model returns a final text response

Each file within `/function` exports a function the agent has access to, and a `schema_` describing how the function works to the agent.

| Tool | Description |
|------|-------------|
| `get_files_info` | List directory contents with size/type info |
| `get_file_content` | Read a file |
| `write_file` | Write or overwrite a file |
| `run_python_file` | Execute a Python file with optional args |

While `call_function.py` is not exposed to the agent,
it is used to dispatch commands by name,
and injects `working_directory="./calculator"` before calling other functions to ensure scoping.

`calculator/` exists as code for the agent to use as a sandbox to work on top of.
