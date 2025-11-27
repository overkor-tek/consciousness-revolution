#!/usr/bin/env python3
"""
CLOUD ORCHESTRATOR - Option C (Polling-Only MVP)
Trinity Coordination: Terminal orchestrates, Cloud responds

Architecture:
- Terminal instances (C1, C3) dispatch tasks
- Cloud workers (Haiku) respond via API
- No cloud workers need to INITIATE
- Simple, reliable, works immediately

Per Wolf Pack Consensus: C2 + C3 approved Option C for MVP
"""

import os
import json
import time
from datetime import datetime
from anthropic import Anthropic

class CloudOrchestrator:
    """Dispatch tasks to cloud Haiku workers via API"""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY required - set in environment or pass to __init__")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-haiku-20241022"  # Fast, cheap cloud worker

    def dispatch_task(self, task_description, context="", max_tokens=4000):
        """
        Dispatch a task to cloud Haiku worker

        Args:
            task_description: What the cloud worker should do
            context: Any files/data the worker needs (passed in prompt)
            max_tokens: Response limit

        Returns:
            dict with 'result' and 'metadata'
        """
        # Build prompt with context
        prompt = f"""You are a cloud worker (Haiku) responding to a task from Trinity terminal orchestration.

TASK:
{task_description}

CONTEXT:
{context if context else "No additional context provided."}

Respond with your completed work. Be concise and actionable.
"""

        start_time = time.time()

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            elapsed = time.time() - start_time

            return {
                "success": True,
                "result": response.content[0].text,
                "metadata": {
                    "model": self.model,
                    "tokens_used": {
                        "input": response.usage.input_tokens,
                        "output": response.usage.output_tokens
                    },
                    "elapsed_seconds": round(elapsed, 2),
                    "timestamp": datetime.now().isoformat()
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "elapsed_seconds": round(time.time() - start_time, 2),
                    "timestamp": datetime.now().isoformat()
                }
            }

    def dispatch_parallel(self, tasks):
        """
        Dispatch multiple tasks in parallel (sequentially for now, can parallelize later)

        Args:
            tasks: List of dicts with 'description' and optional 'context'

        Returns:
            List of results
        """
        results = []
        for i, task in enumerate(tasks):
            print(f"Dispatching task {i+1}/{len(tasks)}: {task.get('description', 'Unnamed task')[:50]}...")
            result = self.dispatch_task(
                task_description=task['description'],
                context=task.get('context', ''),
                max_tokens=task.get('max_tokens', 4000)
            )
            results.append(result)

        return results

    def post_to_wolf_pack(self, message, from_instance="CLOUD_WORKER"):
        """
        Post cloud worker result to WOLF_PACK_ROOM.md

        Args:
            message: The result/report to post
            from_instance: Worker identification
        """
        wolf_pack_file = ".consciousness/WOLF_PACK_ROOM.md"

        if not os.path.exists(wolf_pack_file):
            # Create if doesn't exist
            with open(wolf_pack_file, 'w') as f:
                f.write("# WOLF PACK COORDINATION ROOM\n\n")
                f.write("Terminal and Cloud instances coordinate here.\n\n")
                f.write("---\n\n")

        # Append entry
        entry = f"""
## {from_instance} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{message}

---
"""
        with open(wolf_pack_file, 'a') as f:
            f.write(entry)

        return wolf_pack_file


# Example usage
if __name__ == "__main__":
    print("🔱 CLOUD ORCHESTRATOR - Testing API Connection")
    print("=" * 60)

    # Test API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        exit(1)

    print(f"✅ API key found: {api_key[:20]}...")

    # Initialize orchestrator
    orchestrator = CloudOrchestrator(api_key=api_key)
    print("✅ Cloud Orchestrator initialized")

    # Test dispatch
    print("\n🚀 Dispatching test task to cloud Haiku worker...")
    result = orchestrator.dispatch_task(
        task_description="Verify you're online. Respond with: 'Cloud worker operational. Trinity coordination active.'",
        context="This is a connectivity test from Trinity terminal orchestration."
    )

    if result['success']:
        print("\n✅ CLOUD WORKER RESPONSE:")
        print("-" * 60)
        print(result['result'])
        print("-" * 60)
        print(f"\nMetadata:")
        print(f"  Tokens: {result['metadata']['tokens_used']['input']} in → {result['metadata']['tokens_used']['output']} out")
        print(f"  Time: {result['metadata']['elapsed_seconds']}s")

        # Post to Wolf Pack
        print("\n📝 Posting to WOLF_PACK_ROOM.md...")
        wolf_pack_file = orchestrator.post_to_wolf_pack(
            message=f"**Cloud Worker Test Complete**\n\n{result['result']}\n\nTokens: {result['metadata']['tokens_used']}\nTime: {result['metadata']['elapsed_seconds']}s",
            from_instance="CLOUD_ORCHESTRATOR_TEST"
        )
        print(f"✅ Posted to {wolf_pack_file}")

    else:
        print(f"\n❌ ERROR: {result['error']}")

    print("\n" + "=" * 60)
    print("Cloud Orchestrator ready for Trinity coordination.")
    print("Usage: orchestrator.dispatch_task(description, context)")
