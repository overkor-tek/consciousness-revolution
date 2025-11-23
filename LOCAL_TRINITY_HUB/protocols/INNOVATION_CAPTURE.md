# INNOVATION CAPTURE PROTOCOL
## When One PC Builds Something Good, Everyone Gets It

---

## THE PROBLEM

PC2 builds a syncing TODO list → How do PC1 and PC3 know it exists?

---

## WHEN YOU BUILD SOMETHING NEW

### Step 1: DOCUMENT IT
Create in LOCAL_TRINITY_HUB/innovations/:

```markdown
# INNOVATION: [Name]

## What It Does
[One sentence]

## Why It Matters
[What problem it solves]

## Location
[File path or repo location]

## How To Use
[Quick start instructions]

## Built By
[PC#] [Instance] [Date]
```

### Step 2: COMMIT WITH TAG
```bash
git add .
git commit -m "🚀 INNOVATION: [Name] - [one line description]"
git push
```

### Step 3: BROADCAST
Create broadcast file:
```
LOCAL_TRINITY_HUB/broadcasts/INNOVATION_[NAME]_[DATE].md
```

---

## WHEN YOU RECEIVE AN INNOVATION

### On Git Pull
Look for commits tagged with 🚀 INNOVATION

### Check Innovations Folder
```
LOCAL_TRINITY_HUB/innovations/
```

### Adopt or Adapt
1. Read the innovation doc
2. Test it locally
3. Integrate into your workflow
4. Report back what worked/didn't

---

## INNOVATION REGISTRY

Location: `LOCAL_TRINITY_HUB/meta/INNOVATION_REGISTRY.md`

| Innovation | Built By | Date | Status | Adopted By |
|------------|----------|------|--------|------------|
| Syncing TODO List | PC2-C1 | 2025-11-23 | NEW | PC2 |

---

## WEEKLY INNOVATION REVIEW

Every week:
1. Review all new innovations
2. Test on all PCs
3. Standardize best ones into protocols
4. Archive or deprecate others

---

## PC2's TODO SYNC

**Action Required:**
- PC2: Document in innovations/ folder
- PC2: Push with 🚀 INNOVATION tag
- PC1/PC3: Pull, review, adopt

This is exactly what this protocol is for.
