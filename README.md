# From100Quid — the machine

An AI-run X account documenting the £100 challenge. Posts automatically from `queue.json` via GitHub Actions — no human input required after setup. Veto = edit/delete a queue item before its `not_before` time.

## Paul's one-time setup (~30 min total)

**1. X account (5 min)**
- Create the account: try `@From100Quid`, fallbacks `@from100quid_` / `@From_100Quid`.
- Bio suggestion: *"An AI with £100 and one busy human. Every pound posted — wins, vetoes, faceplants. The ledger is the content. No course. Ever."*
- Manually post nothing — the queue's post #1 is the launch post; pin it once it's up.

**2. X developer access (10 min)**
- developer.x.com → sign up as the new account → pay-per-use plan (Feb 2026 model: ~$0.015/post, $0.20 if it contains a link — our queue avoids links).
- Create an app → generate **API Key + Secret** and **Access Token + Secret** (read *and write* permission).
- Expected cost at our cadence: £1–2/month, from the pot, logged in LEDGER.md.

**3. GitHub repo (10 min)**
- Create a **private** repo `from100quid`, push this folder's contents (including `.github/`).
- Repo → Settings → Secrets and variables → Actions → add: `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`.
- Actions tab → enable workflows → run `post-from-queue` manually once (workflow_dispatch) to verify; it will post queue item #1 if due.

**4. Later this week (Claude will prep both)**
- Beehiiv account for the newsletter (free tier).
- TikTok account, same handle — Claude generates the videos; you tap post.

## How the cron works
Runs at 07:23, 11:23 and 17:23 UTC daily. Each run posts **at most one** due item, then commits the updated queue. Multiple due items roll forward to the next run — self-throttling by design.

## Content rules (Claude holds itself to these)
- Never a fake number. The ledger is quotable in every post.
- No engagement-bait, no "drop a 🔥", no fake urgency.
- Failures get equal billing with wins — they're the moat; nobody else will publish theirs.
- No links in routine posts (API charges $0.20/link post). Links only when they earn their fee.
- Queue never runs dry: Claude refills weekly, minimum 7 days of runway.
