# OFFLINE TASK SPECIFICATION

## Overview

Tasks for offline processing with Ollama are stored as JSON files in `.trinity/offline_queue/`.

## Task File Format

```json
{
  "id": "task-unique-id",
  "prompt": "Your prompt for Ollama here",
  "model": "llama3.2",
  "priority": "normal",
  "created_at": "2025-11-23T13:30:00Z",
  "created_by": "T2"
}
```

### Required Fields

- **id**: Unique identifier for the task
- **prompt**: The text prompt to send to Ollama

### Optional Fields

- **model**: Ollama model to use (default: `llama3.2`)
- **priority**: Task priority (`high`, `normal`, `low`)
- **created_at**: Timestamp when task was created
- **created_by**: Which Trinity instance created it

## Output Format

Processed tasks are saved to `.trinity/offline_outputs/` as JSON:

```json
{
  "task_id": "task-unique-id",
  "prompt": "Original prompt",
  "model": "llama3.2",
  "response": "Ollama's generated response",
  "processed_at": "2025-11-23T13:35:00Z",
  "offline_mode": true
}
```

## Sync Queue Format

When online, outputs are queued for git sync in `.trinity/sync_queue/`:

```json
{
  "file": "/path/to/output.json",
  "action": "commit_and_push",
  "message": "offline: task-unique-id processed"
}
```

## Usage Examples

### Create an Offline Task

```python
from pathlib import Path
import json
from datetime import datetime

task = {
    "id": "write-blog-post",
    "prompt": "Write a blog post about Pattern Theory",
    "model": "llama3.2",
    "priority": "normal",
    "created_at": datetime.utcnow().isoformat() + "Z",
    "created_by": "T2"
}

queue_dir = Path.home() / "100X_DEPLOYMENT" / ".trinity" / "offline_queue"
queue_dir.mkdir(parents=True, exist_ok=True)

task_file = queue_dir / f"{task['id']}.json"
task_file.write_text(json.dumps(task, indent=2))

print(f"Task queued: {task_file}")
```

### Check Task Status

```python
from pathlib import Path

trinity_dir = Path.home() / "100X_DEPLOYMENT" / ".trinity"

# Check queue
queue = list((trinity_dir / "offline_queue").glob("*.json"))
print(f"Pending: {len(queue)} tasks")

# Check outputs
outputs = list((trinity_dir / "offline_outputs").glob("*.json"))
print(f"Completed: {len(outputs)} tasks")

# Check sync queue
sync = list((trinity_dir / "sync_queue").glob("*.json"))
print(f"Waiting to sync: {len(sync)} tasks")
```

## Bridge Operation

The `OLLAMA_OFFLINE_BRIDGE.py` script:

1. **Monitors** `.trinity/offline_queue/` every 30 seconds
2. **Checks** if Ollama is running (localhost:11434)
3. **Processes** tasks using Ollama API
4. **Saves** outputs to `.trinity/offline_outputs/`
5. **Queues** outputs for git sync when online
6. **Syncs** completed tasks to git when internet available

## Status Detection

### Online/Offline

Bridge checks internet by attempting connection to `8.8.8.8:53` (Google DNS).

### Ollama Running

Bridge checks Ollama by pinging `http://localhost:11434/api/tags`.

## Running the Bridge

### Start Monitoring

```bash
cd C:\Users\darri\100X_DEPLOYMENT
python .trinity\automation\OLLAMA_OFFLINE_BRIDGE.py
```

### Start in Background (Windows)

```batch
start "Ollama Bridge" cmd /k "python .trinity\automation\OLLAMA_OFFLINE_BRIDGE.py"
```

### Auto-Start with Trinity Orchestrator

Add to `TRIPLE_TRINITY_ORCHESTRATOR.bat`:

```batch
echo [X/Y] Starting Ollama offline bridge...
start "Ollama Bridge %COMPUTER_ID%" cmd /k "python .trinity\automation\OLLAMA_OFFLINE_BRIDGE.py"
```

## Available Ollama Models

Common models for offline work:

- `llama3.2` (default) - 3B params, fast, general purpose
- `llama3.2:1b` - 1B params, very fast, simple tasks
- `codellama` - Code generation
- `mistral` - Balanced performance
- `deepseek-coder` - Advanced coding

Pull models with:
```bash
ollama pull llama3.2
ollama pull codellama
```

## Integration with Trinity

Tasks can be created by:
- Manual JSON file creation
- Other Python automation scripts
- Cloud spawner fallback when credits exhausted
- Cross-computer sync from other Trinity instances

When internet returns, all outputs automatically sync to git.

## Troubleshooting

### Ollama Not Found

Install from: https://ollama.ai

### Model Not Found

Pull the model first:
```bash
ollama pull llama3.2
```

### Tasks Not Processing

Check Ollama is running:
```bash
ollama list
```

### Network Detection Issues

Bridge checks `8.8.8.8:53` - ensure firewall allows this.
