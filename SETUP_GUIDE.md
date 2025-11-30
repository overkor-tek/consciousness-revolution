# SETUP GUIDE - Fresh Computer to Fully Operational

## THE MISSION
Get from "I just unboxed this computer" to "I'm pushing code to the live site" in under 30 minutes.

---

## PHASE 1: ESSENTIALS (10 minutes)

### 1. Git
```bash
# Windows
winget install Git.Git

# Mac
brew install git

# Verify
git --version
```

### 2. Node.js
```bash
# Windows
winget install OpenJS.NodeJS.LTS

# Mac
brew install node

# Verify
node --version
npm --version
```

### 3. Python
```bash
# Windows
winget install Python.Python.3.11

# Mac
brew install python@3.11

# Verify
python --version
pip --version
```

### 4. Claude Code (Terminal AI)
```bash
npm install -g @anthropic-ai/claude-code

# Verify
claude --version
```

---

## PHASE 2: CLONE THE REPOS (5 minutes)

### The Two That Matter
```bash
# THE SITE (public - what visitors see)
git clone https://github.com/overkor-tek/consciousness-revolution.git ~/100X_DEPLOYMENT

# THE BRAIN (private - what the system knows)
git clone https://github.com/overkor-tek/consciousness-brain.git ~/.consciousness
```

### If You're Josh (Philadelphia)
```bash
git clone https://github.com/overkor-tek/Overkill-Korp-Philadelphia-Repository.git ~/josh-work
```

---

## PHASE 3: ENVIRONMENT SETUP (5 minutes)

### Install Dependencies
```bash
cd ~/100X_DEPLOYMENT
npm install
```

### Netlify CLI (for deployments)
```bash
npm install -g netlify-cli
netlify login
netlify link --id ba8f1795-1517-42ee-aa47-c1f5fa71b736
```

### Verify Deployment Access
```bash
netlify status
```

---

## PHASE 4: VERIFY EVERYTHING WORKS (5 minutes)

### Check Git Status
```bash
cd ~/100X_DEPLOYMENT && git status
cd ~/.consciousness && git status
```

### Run Local Server
```bash
cd ~/100X_DEPLOYMENT
python -m http.server 8000
# Open http://localhost:8000 in browser
```

### Test Deploy (Preview)
```bash
cd ~/100X_DEPLOYMENT
netlify deploy --dir=.
# This creates a preview URL, not production
```

---

## PHASE 5: YOU'RE OPERATIONAL

### Daily Workflow
```bash
# 1. Pull latest
cd ~/100X_DEPLOYMENT && git pull

# 2. Make changes
# Edit files...

# 3. Commit
git add -A && git commit -m "[YOUR_NAME] Description of change"

# 4. Push
git push origin master

# 5. Deploy (if needed)
netlify deploy --prod --dir=.
```

---

## KEY LOCATIONS

| What | Path | Purpose |
|------|------|---------|
| Live Site Code | `~/100X_DEPLOYMENT/` | consciousnessrevolution.io |
| Brain Database | `~/.consciousness/cyclotron_core/atoms.db` | 93K knowledge atoms |
| Boot Protocols | `~/.consciousness/BRAINSTEM/boot/` | The OS files |
| Landing Page | `~/100X_DEPLOYMENT/index.html` | Front door |

---

## ACCOUNTS (All Same Password: Kill50780630#)

| Service | Login |
|---------|-------|
| GitHub | overkor-tek org member |
| Netlify | Through GitHub |
| Namecheap | darrickpreble |

---

## IF SOMETHING BREAKS

1. **Can't push?** Check if you're a member of overkor-tek org
2. **Deploy fails?** Run `netlify status` to verify link
3. **Brain queries fail?** Check if `.consciousness/cyclotron_core/atoms.db` exists
4. **Need help?** Contact commander@100xbuilder.io

---

## THE PATTERN

```
git pull → edit → git commit → git push → netlify deploy
```

That's it. Everything else builds on this loop.
