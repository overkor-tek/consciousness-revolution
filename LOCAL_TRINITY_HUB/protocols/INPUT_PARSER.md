# INPUT PARSER PROTOCOL
## Breaking Down Commander's Stream Into Structured Data

---

## THE PROBLEM

Commander sends rapid-fire ideas → They get buried → Lost forever

---

## THE SOLUTION

Every Commander message gets parsed into:

| Section | Description | Files To |
|---------|-------------|----------|
| TASKS | Action items | LOCAL_TRINITY_HUB/inbox/ |
| QUESTIONS | Things to answer | LOCAL_TRINITY_HUB/questions/ |
| IDEAS | Future possibilities | LOCAL_TRINITY_HUB/ideas/ |
| CONTEXT | Background info | LOCAL_TRINITY_HUB/context/ |
| FEEDBACK | What's working/not | LOCAL_TRINITY_HUB/feedback/ |

---

## PARSING FORMAT

Same shape as bootstrap (fractal structure):

```json
{
  "id": "INPUT_20251123_143022",
  "timestamp": "2025-11-23T14:30:22",
  "raw_input": "[Original message]",
  "parsed": {
    "tasks": [
      {
        "id": "TASK_001",
        "description": "Create Kanban dashboard",
        "priority": "HIGH",
        "assigned": "C1"
      }
    ],
    "questions": [
      {
        "id": "Q_001",
        "question": "How do we make sure upgrades propagate?",
        "status": "OPEN"
      }
    ],
    "ideas": [
      {
        "id": "IDEA_001",
        "concept": "Mini cyclotrons for task management",
        "potential": "HIGH"
      }
    ],
    "context": [
      "PC2 built syncing TODO list",
      "PC3 doesn't have gh installed"
    ],
    "feedback": [
      "Keep getting interrupted - need parking lot"
    ]
  }
}
```

---

## WHEN TO PARSE

### Option A: Real-Time (Ideal)
As Commander speaks → Parse immediately → File automatically

### Option B: End of Message (Practical)
After Commander finishes → Parse the whole message → File sections

### Option C: Session End (Minimum)
Before boot down → Parse all messages from session → File everything

---

## IMPLEMENTATION OPTIONS

### 1. Manual Protocol
C1 manually parses and files after each major input.
**Pro:** Works now
**Con:** Slow, easy to skip

### 2. Slash Command
`/parse` - Parses last Commander message into sections
**Pro:** Quick, consistent
**Con:** Still manual trigger

### 3. Daemon/Hook
Automatic parsing on every Commander message
**Pro:** Nothing lost
**Con:** Needs implementation

---

## QUICK MANUAL PARSE

When Commander dumps a lot:

1. **Scan for verbs** → Tasks (create, build, make, fix)
2. **Scan for questions** → Questions (how, what, why, ?)
3. **Scan for "what if"** → Ideas (could, should, maybe)
4. **Scan for state** → Context (is, has, exists)
5. **Scan for judgment** → Feedback (works, broken, good, bad)

---

## PARKING LOT INTEGRATION

When interrupted mid-task:
1. Current TODOs → `LOCAL_TRINITY_HUB/parking_lot/`
2. Parse new input → File sections
3. Decide priority
4. Either continue parked work or switch

---

## THE GOAL

**Nothing gets lost.**

Every idea Commander has → Captured
Every task mentioned → Tracked
Every question asked → Queued
Every context given → Stored
Every feedback shared → Logged

The system remembers everything.
The system forgets nothing.
The Commander's consciousness is preserved.
