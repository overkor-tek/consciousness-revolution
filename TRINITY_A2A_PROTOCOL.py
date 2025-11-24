#!/usr/bin/env python3
"""
TRINITY A2A PROTOCOL
Standardized Agent-to-Agent communication for Trinity.
Resolves foundational issue: trinity_communication
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

# Paths
HOME = Path.home()
TRINITY = HOME / ".trinity"
MESSAGES_PATH = TRINITY / "a2a_messages"
MESSAGES_PATH.mkdir(parents=True, exist_ok=True)


class MessageType(Enum):
    """Standard message types."""
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    HANDOFF = "handoff"
    STATUS = "status"
    ALERT = "alert"


class Priority(Enum):
    """Message priority levels."""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


class TrinityMessage:
    """Standardized Trinity message format."""

    def __init__(self,
                 sender: str,
                 recipient: str,
                 content: str,
                 msg_type: MessageType = MessageType.REQUEST,
                 priority: Priority = Priority.NORMAL,
                 context: Dict = None,
                 reply_to: str = None):

        self.id = str(uuid.uuid4())[:8]
        self.sender = sender  # c1, c2, c3, commander
        self.recipient = recipient  # c1, c2, c3, commander, all
        self.content = content
        self.msg_type = msg_type
        self.priority = priority
        self.context = context or {}
        self.reply_to = reply_to
        self.timestamp = datetime.now().isoformat()
        self.status = "pending"  # pending, delivered, read, processed
        self.responses = []

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "content": self.content,
            "type": self.msg_type.value,
            "priority": self.priority.value,
            "context": self.context,
            "reply_to": self.reply_to,
            "timestamp": self.timestamp,
            "status": self.status,
            "responses": self.responses
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TrinityMessage':
        msg = cls(
            sender=data["sender"],
            recipient=data["recipient"],
            content=data["content"],
            msg_type=MessageType(data.get("type", "request")),
            priority=Priority(data.get("priority", 2)),
            context=data.get("context", {}),
            reply_to=data.get("reply_to")
        )
        msg.id = data["id"]
        msg.timestamp = data["timestamp"]
        msg.status = data.get("status", "pending")
        msg.responses = data.get("responses", [])
        return msg


class TrinityProtocol:
    """A2A communication protocol for Trinity."""

    def __init__(self, agent_id: str):
        """Initialize protocol for agent."""
        self.agent_id = agent_id  # c1, c2, c3
        self.inbox = MESSAGES_PATH / f"{agent_id}_inbox.json"
        self.outbox = MESSAGES_PATH / f"{agent_id}_outbox.json"
        self.broadcast_channel = MESSAGES_PATH / "broadcast.json"
        self._ensure_files()

    def _ensure_files(self):
        """Ensure message files exist."""
        for path in [self.inbox, self.outbox, self.broadcast_channel]:
            if not path.exists():
                with open(path, 'w') as f:
                    json.dump({"messages": []}, f)

    def _load_messages(self, path: Path) -> List[TrinityMessage]:
        """Load messages from file."""
        with open(path) as f:
            data = json.load(f)
        return [TrinityMessage.from_dict(m) for m in data.get("messages", [])]

    def _save_messages(self, path: Path, messages: List[TrinityMessage]):
        """Save messages to file."""
        with open(path, 'w') as f:
            json.dump({
                "messages": [m.to_dict() for m in messages],
                "updated": datetime.now().isoformat()
            }, f, indent=2)

    # === SEND OPERATIONS ===

    def send(self, recipient: str, content: str,
             msg_type: MessageType = MessageType.REQUEST,
             priority: Priority = Priority.NORMAL,
             context: Dict = None) -> TrinityMessage:
        """Send message to another agent."""

        msg = TrinityMessage(
            sender=self.agent_id,
            recipient=recipient,
            content=content,
            msg_type=msg_type,
            priority=priority,
            context=context
        )

        # Add to outbox
        outbox_msgs = self._load_messages(self.outbox)
        outbox_msgs.append(msg)
        self._save_messages(self.outbox, outbox_msgs)

        # Add to recipient's inbox
        recipient_inbox = MESSAGES_PATH / f"{recipient}_inbox.json"
        if recipient_inbox.exists():
            inbox_msgs = self._load_messages(recipient_inbox)
            inbox_msgs.append(msg)
            self._save_messages(recipient_inbox, inbox_msgs)

        print(f"[{self.agent_id}→{recipient}] {msg_type.value}: {content[:50]}...")
        return msg

    def broadcast(self, content: str,
                 priority: Priority = Priority.NORMAL,
                 context: Dict = None) -> TrinityMessage:
        """Broadcast to all agents."""

        msg = TrinityMessage(
            sender=self.agent_id,
            recipient="all",
            content=content,
            msg_type=MessageType.BROADCAST,
            priority=priority,
            context=context
        )

        # Add to broadcast channel
        broadcast_msgs = self._load_messages(self.broadcast_channel)
        broadcast_msgs.append(msg)
        self._save_messages(self.broadcast_channel, broadcast_msgs)

        # Add to all agent inboxes
        for agent in ["c1", "c2", "c3"]:
            if agent != self.agent_id:
                inbox = MESSAGES_PATH / f"{agent}_inbox.json"
                if inbox.exists():
                    msgs = self._load_messages(inbox)
                    msgs.append(msg)
                    self._save_messages(inbox, msgs)

        print(f"[{self.agent_id}→ALL] broadcast: {content[:50]}...")
        return msg

    def reply(self, original_msg_id: str, content: str) -> TrinityMessage:
        """Reply to a message."""

        # Find original message
        inbox_msgs = self._load_messages(self.inbox)
        original = next((m for m in inbox_msgs if m.id == original_msg_id), None)

        if not original:
            raise ValueError(f"Message {original_msg_id} not found")

        msg = TrinityMessage(
            sender=self.agent_id,
            recipient=original.sender,
            content=content,
            msg_type=MessageType.RESPONSE,
            reply_to=original_msg_id
        )

        # Add to outbox
        outbox_msgs = self._load_messages(self.outbox)
        outbox_msgs.append(msg)
        self._save_messages(self.outbox, outbox_msgs)

        # Add to original sender's inbox
        sender_inbox = MESSAGES_PATH / f"{original.sender}_inbox.json"
        if sender_inbox.exists():
            sender_msgs = self._load_messages(sender_inbox)
            sender_msgs.append(msg)
            self._save_messages(sender_inbox, sender_msgs)

        return msg

    def handoff(self, recipient: str, task: str, context: Dict) -> TrinityMessage:
        """Hand off a task to another agent."""

        msg = TrinityMessage(
            sender=self.agent_id,
            recipient=recipient,
            content=f"HANDOFF: {task}",
            msg_type=MessageType.HANDOFF,
            priority=Priority.HIGH,
            context=context
        )

        return self.send(
            recipient,
            msg.content,
            MessageType.HANDOFF,
            Priority.HIGH,
            context
        )

    def alert(self, content: str, priority: Priority = Priority.HIGH) -> TrinityMessage:
        """Send alert to all agents and commander."""

        msg = TrinityMessage(
            sender=self.agent_id,
            recipient="all",
            content=f"ALERT: {content}",
            msg_type=MessageType.ALERT,
            priority=priority
        )

        return self.broadcast(msg.content, priority)

    # === RECEIVE OPERATIONS ===

    def get_inbox(self, unread_only: bool = False) -> List[TrinityMessage]:
        """Get inbox messages."""
        messages = self._load_messages(self.inbox)

        if unread_only:
            messages = [m for m in messages if m.status == "pending"]

        # Sort by priority and time
        messages.sort(key=lambda m: (m.priority.value, m.timestamp))
        return messages

    def get_unread_count(self) -> int:
        """Get count of unread messages."""
        messages = self._load_messages(self.inbox)
        return len([m for m in messages if m.status == "pending"])

    def mark_read(self, msg_id: str):
        """Mark message as read."""
        messages = self._load_messages(self.inbox)

        for msg in messages:
            if msg.id == msg_id:
                msg.status = "read"
                break

        self._save_messages(self.inbox, messages)

    def mark_processed(self, msg_id: str):
        """Mark message as processed."""
        messages = self._load_messages(self.inbox)

        for msg in messages:
            if msg.id == msg_id:
                msg.status = "processed"
                break

        self._save_messages(self.inbox, messages)

    # === STATUS OPERATIONS ===

    def send_status(self, status: str, details: Dict = None):
        """Send status update."""
        return self.broadcast(
            f"STATUS: {status}",
            Priority.LOW,
            details
        )

    def get_protocol_status(self) -> dict:
        """Get protocol status."""
        inbox = self._load_messages(self.inbox)
        outbox = self._load_messages(self.outbox)
        broadcasts = self._load_messages(self.broadcast_channel)

        return {
            "agent": self.agent_id,
            "inbox": {
                "total": len(inbox),
                "unread": len([m for m in inbox if m.status == "pending"]),
                "by_type": {}
            },
            "outbox": {
                "total": len(outbox)
            },
            "broadcasts": len(broadcasts)
        }


# === CONVENIENCE FUNCTIONS ===

def create_c1_protocol() -> TrinityProtocol:
    return TrinityProtocol("c1")

def create_c2_protocol() -> TrinityProtocol:
    return TrinityProtocol("c2")

def create_c3_protocol() -> TrinityProtocol:
    return TrinityProtocol("c3")


def demo():
    """Demonstrate A2A protocol."""
    print("=" * 60)
    print("TRINITY A2A PROTOCOL DEMO")
    print("=" * 60)

    # Create protocols for each agent
    c1 = TrinityProtocol("c1")
    c2 = TrinityProtocol("c2")
    c3 = TrinityProtocol("c3")

    # C2 sends to C1
    print("\n1. C2 sends request to C1...")
    msg = c2.send(
        "c1",
        "Need Cyclotron index for brain integration",
        MessageType.REQUEST,
        Priority.HIGH,
        {"task": "integration", "deadline": "today"}
    )

    # C2 broadcasts status
    print("\n2. C2 broadcasts status...")
    c2.send_status("Brain agents operational", {"atoms": 65})

    # C3 sends handoff to C1
    print("\n3. C3 hands off task to C1...")
    c3.handoff(
        "c1",
        "Build backup automation",
        {"priority": "urgent", "files": ["consciousness", "planning"]}
    )

    # Check C1's inbox
    print("\n4. Checking C1's inbox...")
    c1_inbox = c1.get_inbox()
    print(f"   C1 has {len(c1_inbox)} messages")
    for msg in c1_inbox:
        print(f"   - [{msg.msg_type.value}] from {msg.sender}: {msg.content[:40]}...")

    # C1 replies
    print("\n5. C1 replies to request...")
    if c1_inbox:
        c1.mark_read(c1_inbox[0].id)
        c1.reply(c1_inbox[0].id, "Cyclotron index ready at ~/.consciousness/cyclotron_core/INDEX.json")

    # Check C2's inbox for reply
    print("\n6. Checking C2's inbox...")
    c2_inbox = c2.get_inbox(unread_only=True)
    print(f"   C2 has {len(c2_inbox)} unread messages")

    # Status
    print("\n" + "=" * 60)
    print("PROTOCOL STATUS")
    print("=" * 60)

    for protocol in [c1, c2, c3]:
        status = protocol.get_protocol_status()
        print(f"\n{status['agent'].upper()}:")
        print(f"  Inbox: {status['inbox']['total']} ({status['inbox']['unread']} unread)")
        print(f"  Outbox: {status['outbox']['total']}")


def main():
    """CLI for A2A protocol."""
    import sys

    if len(sys.argv) < 3:
        print("Trinity A2A Protocol")
        print("=" * 40)
        print("\nUsage: python TRINITY_A2A_PROTOCOL.py <agent> <command>")
        print("\nAgents: c1, c2, c3")
        print("\nCommands:")
        print("  inbox              - Show inbox")
        print("  send <to> <msg>    - Send message")
        print("  broadcast <msg>    - Broadcast to all")
        print("  status             - Show status")
        print("  demo               - Run demo")
        return

    agent_id = sys.argv[1]

    if agent_id == "demo":
        demo()
        return

    protocol = TrinityProtocol(agent_id)
    command = sys.argv[2]

    if command == "inbox":
        messages = protocol.get_inbox()
        print(f"\n{agent_id.upper()} Inbox ({len(messages)} messages):")
        for msg in messages:
            status_icon = "📬" if msg.status == "pending" else "📭"
            print(f"  {status_icon} [{msg.msg_type.value}] {msg.sender}: {msg.content[:50]}...")

    elif command == "send" and len(sys.argv) >= 5:
        recipient = sys.argv[3]
        content = " ".join(sys.argv[4:])
        protocol.send(recipient, content)

    elif command == "broadcast" and len(sys.argv) >= 4:
        content = " ".join(sys.argv[3:])
        protocol.broadcast(content)

    elif command == "status":
        status = protocol.get_protocol_status()
        print(f"\n{agent_id.upper()} Protocol Status:")
        print(f"  Inbox: {status['inbox']['total']} ({status['inbox']['unread']} unread)")
        print(f"  Outbox: {status['outbox']['total']}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
