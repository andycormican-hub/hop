# HOP

**HOP checks whether a firm's own treasury cash can move between spendable USDC and a tokenized T-bill / money-market sleeve, and whether it can come back before a payment is due. If it can't settle, HOP refuses and says why.**

Demo only. Does not move client funds. Not an offer of securities.

Live demo: https://andycormican-hub.github.io/hop/HOP.html

## What it is

- A decision tool for a firm's **own** on-chain treasury: crypto treasuries, market makers, venue desks.
- Four screens: **Policy** (your rules), **Preview** (one proposed hop run through seven checks), **Ledger** (a record of decisions), **Markets** (the live market-status feed with a per-token decision).
- Four verdicts: **Allow**, **Queue**, **Blocked** (fixable, such as an allowlist), **Refuse** (cannot settle in time). Refuse is a feature, not an error.

## What it is not

Not retail. Not for other people's money. No wallets, no key custody, no tokens, no real execution. It does not promise instant 24/7 redemption.

## How it decides

Preview runs seven checks: spendable floor, wallet allowlist, feed against clock, feed freshness, session from the feed, pull-back window, weekend rule. A hop is allowed only when the live feed reads `regular`, the clock agrees, the feed is fresh (under 30 minutes old), and a regular window remains before the pull-back deadline. Anything else is refused or queued, and the page says why. A token that carries no market status is refused, not guessed.

Regular windows are modelled as Mon to Fri 09:30 to 16:00 New York time, with the last 2 minutes held back as a buffer, because on 14 Oct the live feed left `regular` about a minute before 16:00. Holidays and issuer cut-offs are not modelled yet.

## Live data feed

Read-only. No trades.

1. `scripts/fetch_feed.py` makes one signed call to the Binance Web3 RWA Data API (BNB Chain, chain 56) and writes a trimmed `markets.json`.
2. `scripts/refresh_feed.sh` runs it every few minutes and publishes the file to the `feed` branch of this repo.
3. The page reads `markets.json` from the `feed` branch and refreshes every 60 seconds.

The fetch has to run from a region Binance serves. A GitHub Actions version returned `code=40304, Service not available due to compliance restriction` when run on GitHub's servers, so the feed is currently refreshed from a machine in Ireland. The workflow file is kept as a manual-only reference. The feed is only live while that machine runs. When it stops, the page marks the feed stale and HOP refuses.

API keys and tokens live in a private file on the machine running the script (`~/.hop_env`). They are never committed.

## What real data showed

- **7 Oct, premarket** and **8 Oct, postmarket:** the calls read premarket and postmarket, so no Allow could be shown. HOP refused, correctly.
- **12 Oct, 15:44 New York, regular:** 442 tokens `regular`, 46 with no market status.
- **13 Oct, around the open, Irish time:**

| Time | Status counts |
|---|---|
| 14:27 | 403 premarket, 39 paused, 46 no status |
| 14:29 | 117 premarket, 325 paused, 46 no status |
| 14:31 | 424 regular, 18 paused, 46 no status |
| 14:33 | 442 regular, 46 no status |

- **14 Oct, around the close, Irish time (one call every 30 seconds):**

| Time | Regular | Paused | Postmarket (trading / unsupported) | No status |
|---|---|---|---|---|
| 20:58:33 | 442 | 0 | 0 | 46 |
| 20:59:04 | 129 | 313 | 0 | 46 |
| 20:59:36 | 1 | 441 | 0 | 46 |
| 21:00:08 | 0 | 442 | 0 | 46 |
| 21:00:39 | 0 | 442 | 0 | 46 |
| 21:01:10 | 0 | 109 | 265 / 68 | 46 |
| 21:01:42 | 0 | 84 | 290 / 68 | 46 |
| 21:02:13 | 0 | 0 | 320 / 122 | 46 |

- The close mirrors the open. `paused` (reason `MARKET_PAUSED`) brackets the regular session at both ends, and tokens change state at slightly different times over a few minutes, so the feed is briefly mixed. The feed does not say why a market is paused.
- The feed left `regular` about a minute before 16:00 New York, so HOP treats the last 2 minutes of the session as closed. This is one session, so the buffer is a cautious guess, not a measured rule.
- The HOP page followed the feed: after the close it read 442 postmarket, 46 unknown, and refused every token.
- Statuses seen: premarket, regular, postmarket, closed, offhours, paused, and no status. Anything other than `regular` is refused.
- The 46 tokens with no status were all `bstock` tokens in the rows inspected. The `regular` ones were `ondo`. Not yet checked across every row.
- `UNSUPPORTED` means a token is not supported in the current session, even when the market is open.
- The feed's "next open / next close" times describe the next extended session, not the regular one, so HOP uses its own calendar for regular hours.

## What the real sleeves need (research, 12 Oct 2026)

The feed covers tokenized stocks, which is a stand-in. Real sleeves differ:

- **USYC** (Circle / Hashnote): redeem 24/7 via the Teller, but only instantly up to an instant-redemption capacity, then T+0 or T+1. Non-US institutions, $100,000 minimum, wallet whitelisting.
- **BUIDL** (BlackRock / Securitize): daily redemption, tokens must arrive before 3:00 pm ET, USD wire payout, USDC redemptions via service providers, 250,000 USDC redemption minimum, US qualified purchasers, whitelisting.
- **BENJI** (Franklin Templeton): business days only, 2 p.m. Pacific cut-off, bank payout (ACH or wire).

So the real HOP needs per-sleeve rule profiles (cut-off, time zone, business days, minimums, eligibility, allowlist, payout rail) and, for USYC, redemption capacity. Not yet confirmed from the sources: USYC's capacity size, how BUIDL's USDC redemptions work, how BENJI redeems on-chain, how business days are defined. Verify with each issuer before relying on any figure.

## Repo contents

| File | What |
|---|---|
| `HOP.html` | The demo page (single file) |
| `HOP.md` | Original product spec |
| `DEVEX.md` | Developer-experience notes from building on the Binance Web3 API |
| `scripts/fetch_feed.py` | Fetches and trims the feed (Python standard library only) |
| `scripts/refresh_feed.sh` | Runs the fetch on a loop and publishes to the `feed` branch |
| `.github/workflows/update-feed.yml` | Manual-only reference workflow (blocked on GitHub's servers) |
| `rwa-platforms.json`, `rwa-tokens-bsc.json` | Saved early API responses |

## Status and next steps

Early demo. Working: policy-driven decisions, live feed on BNB Chain, real regular-hours data. Next: per-sleeve rule profiles, a permanent always-on feed host, conversations with treasury teams about how they decide today.
