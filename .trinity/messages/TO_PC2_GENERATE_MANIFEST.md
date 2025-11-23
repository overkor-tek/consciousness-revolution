# PC2: GENERATE CAPABILITY MANIFEST

## Task: Create your capability manifest for cyclotron sync

### Step 1: Copy the manifest generator
```bash
cp ~/100X_DEPLOYMENT/LOCAL_TRINITY_HUB/CAPABILITY_MANIFEST.py ~/PC2_LOCAL_HUB/
```

### Step 2: Run it
```bash
python ~/PC2_LOCAL_HUB/CAPABILITY_MANIFEST.py
```

### Step 3: Push to git
```bash
cd ~/100X_DEPLOYMENT
git add .
git commit -m "PC2 capability manifest"
git push
```

---

## What This Does

- Scans PC2 for all software, commands, modules, API keys
- Structures by 7 domains (infrastructure, pattern, business, etc.)
- Strips personal info
- Outputs to outbound/ for cyclotron distribution

---

## Why

When we compare manifests:
- We see what PC2 has that PC1 doesn't
- We see new capabilities discovered
- Cyclotron distributes what's missing
- All computers stay synchronized

**Run this now and push the output.**
