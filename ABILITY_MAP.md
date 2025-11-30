# ABILITY MAP - What We Can Do & How We Do It

## THE COMPLETE CAPABILITY INDEX

Every ability in the system, what tool enables it, and who can use it.

---

## DEPLOYMENT ABILITIES

| Ability | Tool | Command | Who Can Do It |
|---------|------|---------|---------------|
| Push to live site | Netlify CLI | `netlify deploy --prod --dir=.` | Anyone with Netlify access |
| Preview deploy | Netlify CLI | `netlify deploy --dir=.` | Anyone with Netlify access |
| Check deploy status | Netlify CLI | `netlify status` | Anyone with Netlify access |
| View deploy logs | Netlify Dashboard | app.netlify.com | Anyone with Netlify access |

---

## CODE ABILITIES

| Ability | Tool | Command | Who Can Do It |
|---------|------|---------|---------------|
| Clone repos | Git | `git clone <url>` | Anyone with GitHub access |
| Push changes | Git | `git push origin master` | Org members |
| Create branch | Git | `git checkout -b branch-name` | Org members |
| Merge to master | GitHub PR | Via GitHub UI | Org admins |
| View commit history | Git | `git log --oneline -20` | Anyone |

---

## BRAIN ABILITIES

| Ability | Tool | Command | Who Can Do It |
|---------|------|---------|---------------|
| Query brain | SQLite | `sqlite3 ~/.consciousness/cyclotron_core/atoms.db "SELECT..."` | Anyone with brain access |
| Count atoms | SQLite | `sqlite3 atoms.db "SELECT COUNT(*) FROM atoms;"` | Anyone with brain access |
| Search by topic | SQLite | `SELECT * FROM atoms WHERE content LIKE '%topic%'` | Anyone with brain access |
| View brain regions | SQLite | `SELECT region, COUNT(*) FROM atoms GROUP BY region` | Anyone with brain access |
| Add to brain | Python ingest | `python CYCLOTRON_INGEST.py` | Commander + C1 |

---

## AI ABILITIES

| Ability | Tool | Command | Who Can Do It |
|---------|------|---------|---------------|
| Run Claude Code | Claude CLI | `claude` | Anyone with API key |
| Terminal AI assistance | Claude Code | Interactive terminal | Anyone with Claude Code |
| Multi-instance Trinity | MCP Tools | `mcp__trinity__*` | Configured instances |
| Araya chat | Web interface | consciousnessrevolution.io/araya-chat.html | Public |

---

## COMMUNICATION ABILITIES

| Ability | Tool | Command | Who Can Do It |
|---------|------|---------|---------------|
| Email | Gmail/SMTP | Via email client | Anyone |
| Bug reports | GitHub Issues | github.com/overkor-tek/consciousness-bugs | Public |
| Trinity broadcast | MCP | `mcp__trinity__trinity_broadcast` | Trinity instances |
| Direct message | MCP | `mcp__trinity__trinity_send_message` | Trinity instances |

---

## FILE ABILITIES

| Ability | Tool | Command | Who Can Do It |
|---------|------|---------|---------------|
| Screenshot | Python PIL | `from PIL import ImageGrab; ImageGrab.grab().save('path')` | Anyone with Python |
| Sync across computers | Git | Push/pull cycle | Anyone with access |
| Backup | Git | Push to remote | Anyone with access |
| Search files | Glob/Grep | Via Claude Code tools | Terminal instances |

---

## SITE ABILITIES

| Ability | Tool | URL | Who Can Do It |
|---------|------|-----|---------------|
| View live site | Browser | consciousnessrevolution.io | Public |
| Access tools | Browser | consciousnessrevolution.io/[tool].html | Public |
| Admin dashboard | Browser | consciousnessrevolution.io/admin-dashboard.html | Authenticated |
| Bug tracker | Browser | consciousnessrevolution.io/bugs.html | Public |

---

## ANALYSIS ABILITIES (115+ Tools)

### Manipulation Detectors
| Tool | URL |
|------|-----|
| Gaslighting Detector | /GASLIGHTING_DETECTOR.html |
| Love Bombing Detector | /LOVE_BOMBING_DETECTOR.html |
| Guilt Trip Detector | /GUILT_TRIP_DETECTOR.html |
| Emotional Blackmail Detector | /EMOTIONAL_BLACKMAIL_DETECTOR.html |
| Future Faking Detector | /FUTURE_FAKING_DETECTOR.html |
| Breadcrumbing Detector | /BREADCRUMBING_DETECTOR.html |
| ... (15+ more) | See landing page |

### Decision Tools
| Tool | URL |
|------|-----|
| Manipulation Detector | /manipulation_detector.html |
| Conversation Analyzer | /CONVERSATION_ANALYZER.html |
| Email Analyzer | /EMAIL_ANALYZER.html |
| Contract Analyzer | /CONTRACT_ANALYZER.html |
| Decision Matrix | /DECISION_MATRIX.html |
| ... (10+ more) | See landing page |

### Seven Domains
| Tool | URL |
|------|-----|
| Seven Domains Hub | /seven_domains.html |
| Domain Assessment | /seven-domains-assessment.html |
| Daily Consciousness Check | /DAILY_CONSCIOUSNESS_CHECK.html |
| Emotional State Checker | /EMOTIONAL_STATE_CHECKER.html |
| Financial Decision Checker | /FINANCIAL_DECISION_CHECKER.html |

---

## ROLE-BASED ACCESS

| Role | Can Deploy | Can Push | Can Edit Brain | Can Admin |
|------|------------|----------|----------------|-----------|
| Commander | ✅ | ✅ | ✅ | ✅ |
| Maggie (Backup) | ✅ | ✅ | ✅ | ✅ |
| C1 Terminal | ✅ | ✅ | ✅ | ❌ |
| C2 Desktop | ❌ | ❌ | ❌ | ❌ (design only) |
| Beta Testers | ❌ | ❌ | ❌ | ❌ (use only) |
| Josh (Philadelphia) | ✅ | ✅ | ❌ | ❌ |
| Public | ❌ | ❌ | ❌ | ❌ |

---

## THE QUICK REFERENCE

### Most Used Commands
```bash
# Deploy
cd ~/100X_DEPLOYMENT && netlify deploy --prod --dir=.

# Query brain
sqlite3 ~/.consciousness/cyclotron_core/atoms.db "SELECT * FROM atoms WHERE content LIKE '%topic%' LIMIT 10"

# Git cycle
git pull && git add -A && git commit -m "message" && git push

# Start Claude
claude
```

### Key URLs
- **Live Site:** consciousnessrevolution.io
- **Netlify Dashboard:** app.netlify.com/sites/verdant-tulumba-fa2a5a
- **GitHub Org:** github.com/overkor-tek
- **Bug Tracker:** github.com/overkor-tek/consciousness-bugs

---

## THE PATTERN

Every ability follows the same structure:
1. **Tool** - What software enables it
2. **Command** - How to invoke it
3. **Access** - Who is authorized
4. **Location** - Where it lives

If you can't find an ability, it either:
- Doesn't exist yet (build it)
- Exists but isn't documented (add it here)
- Requires higher access (ask Commander)
