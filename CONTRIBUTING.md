# CONTRIBUTING - How Team Members Submit Work

## THE SIMPLE TRUTH

```
Pull → Edit → Commit → Push → Deploy
```

That's the whole workflow. Everything below is details.

---

## BEFORE YOU START

### 1. Make Sure You Have Access
- [ ] GitHub: Member of overkor-tek organization
- [ ] Netlify: Can access verdant-tulumba-fa2a5a site
- [ ] Local: Cloned both repos (100X_DEPLOYMENT + .consciousness)

### 2. Verify Your Setup
```bash
cd ~/100X_DEPLOYMENT && git status
netlify status
```

If either fails, see SETUP_GUIDE.md

---

## THE WORKFLOW

### Step 1: Pull Latest
```bash
cd ~/100X_DEPLOYMENT
git pull origin master
```
**Always pull before starting work.** Prevents merge conflicts.

### Step 2: Make Your Changes
Edit files using whatever editor you prefer.

### Step 3: Commit
```bash
git add -A
git commit -m "[YOUR_NAME] Brief description"
```

### Step 4: Push
```bash
git push origin master
```

### Step 5: Deploy (if needed)
```bash
netlify deploy --prod --dir=.
```

---

## COMMIT MESSAGE FORMAT
```
[NAME] Action: Description

Examples:
[JOSH] Fix: Login page redirect loop
[C1] Add: New manipulation detector tool
[COMMANDER] Update: Landing page redesign
```

---

## THE MANTRA

**"If it's not in git, it doesn't exist."**

Push your work. Every day. No exceptions.
