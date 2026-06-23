---
phase: Migration Planning
date: 2026-06-22
status: IDEATION
related: Phase-19-Harvest-Pipeline, Droplet-Deployment
---

# Droplet + Paperspace A4000 Integration Plan

## 1.0 HIGH-LEVEL ARCHITECTURE

text

┌─────────────────────────────────────────────────────────────────────────────┐
│                    CADMIES HYBRID DEPLOYMENT ARCHITECTURE                     │
│                                                                              │
│  ┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐   │
│  │  LOCAL (Fedora)  │     │  DROPLET ($18/mo) │     │  PAPERSPACE (A4000) │   │
│  │  Dev + Light Test│     │  Public Gateway   │     │  AI Inference        │   │
│  │                  │     │                   │     │                      │   │
│  │  • Code editing  │     │  • Nginx (80/443) │     │  • Mistral 7B        │   │
│  │  • Git push/pull │     │  • Mycelium Map   │     │  • Codestral 22B     │   │
│  │  • Concept dev   │     │  • Dr. Mistral UI │     │  • Harvest Pipeline  │   │
│  │  • Testing       │     │  • MongoDB        │     │  • Relationship Gen  │   │
│  │                  │     │  • Willie Chat    │     │  • 6-hr session limit│   │
│  └────────┬────────┘     │  • Health Checks  │     │                      │   │
│           │              │                   │     │                      │   │
│           │   GitHub     │  Node API :4002   │     │  Gradient API        │   │
│           └──────────────┤                   │◄───►│                      │   │
│           Source of Truth│  PM2 Process Mgr  │     │  Start/Stop/Monitor  │   │
│                          │                   │     │                      │   │
│                          └───────────────────┘     └──────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

---

## 2.0 DOCTOR MISTRAL AVAILABILITY PATTERN

text

Session 1:  ████████████████████████████████░░  5.5 hrs active, 30 min cooldown
Reset:                                      ██  Shutdown → Restart (2-3 min)
Session 2:  ████████████████████████████████░░  5.5 hrs active, 30 min cooldown
Reset:                                      ██  Repeat
Session N:  ████████████████████████████████░░  Infinite loop via cron

Gap between sessions: ~2-3 minutes every 5.5 hours = 99.1% uptime during active hours

User-facing message: "THE DOCTOR IS OUT — BACK IN 2:48"
Willie commentary: Rotating Scottish groundskeeper roasts during downtime

---

## 3.0 COMPONENTS TO BUILD

| # | Component | Location | Description |
|---|---|---|---|
| 1 | Paperspace API controller | Droplet | Start/stop A4000, monitor session time, trigger resets |
| 2 | Job queue manager | Droplet | Queue harvest/relationship requests during downtime |
| 3 | Session timer display | Droplet (frontend) | "Doctor is in/out" status on all pages |
| 4 | Willie commentary engine | Droplet (frontend) | Rotating Scottish-accented status messages |
| 5 | Health check integration | Droplet | Track Paperspace status, log session history |
| 6 | Deployment scripts | GitHub → Droplet | Pull, build, restart PM2 for updates |

---

## 4.0 WILLIE CONCEPT BOARD

Character: Scottish groundskeeper, lives in the server rack
Tone: Grumpy, loyal, complains about electricity, mocks the Doctor
Function: Frontend status character during GPU downtime

Sample dialogue:
- "Och, the doctor's stepped away! Grease yourself up and wait like the rest of us!"
- "Still bootin', aye. That GPU's colder than a wee haggis in a snowdrift."
- "D'ye think the doctor cares about yer query? Nah, he's off ponderin' the cosmos!"
- "Back in two minutes or I'm no' worth me porridge."
- "The pipes are hummin' again. Doctor's in. Try not to break anything this time."

---

## 5.0 MIGRATION STEPS (Rough Order)

1. CADMIES repo → pull to droplet
2. Configure Nginx to serve mycelium map and gateway
3. Set up Node API endpoint for Paperspace communication
4. Build Paperspace API controller script
5. Implement job queue for downtime requests
6. Add Doctor/Willie frontend status component
7. Test full cycle: submit query → queue → GPU process → response
8. Set up cron for automated session cycling
9. Public launch

---

## 6.0 OPEN QUESTIONS

- Keep Paperspace Pro ($8/mo) or migrate to DO GPU droplet?
- Webhook from GitHub to auto-deploy on push, or manual pull?
- MongoDB schema for job queue vs. file-based queue?
- Willie: text-only or tiny sprite/animation?
- Dr. Mistral chat: streaming responses or full-response delivery?

---

## 7.0 COST PROJECTION

| Service | Monthly |
|---|---|
| Droplet | $18 |
| Paperspace Pro | $8 |
| GitHub | Free |
| **Total** | **$26/mo** |

Optional: DO GPU droplet instead of Paperspace (~$0.15-0.50/hr, only when active)