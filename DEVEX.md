# HOP: Developer Experience Report

BNB Hack: Tokenized Stocks Edition
Builder: Andy Cormican (solo)
Repo: https://github.com/andycormican-hub/hop
Demo: https://andycormican-hub.github.io/hop/HOP.html
Video: linked from README

Updated 15 Oct 2026. The first version of this report was written before I had made a successful call. Everything under "Measured" below comes from real calls to the RWA tokens endpoint on BNB Chain (chain 56). Everything under "Not measured" is still a hypothesis.

## What I built

HOP is a treasury policy demo. It checks whether a firm's own on-chain cash can move into a yielding sleeve and be pulled back before a payment is due. It refuses the hop when settlement cannot complete (allowlist, cut-off, weekend, market not in its regular session).

For this hack the stand-in sleeve is a tokenized stock on BSC (Ondo, bStocks and similar), because that is what the RWA data feed covers. The real sleeves I care about are tokenized T-bill and money-market funds.

It is a single-file demo page with four tabs: Policy, Preview, Ledger, Markets. Balances are dummy. No wallet, no live transfer. That is deliberate: HOP must not look like it moves funds.

The Markets tab reads a live feed built from the RWA tokens endpoint. It is read-only. No trades.

## Onboarding

I am a solo builder, not a full-time engineer. I started from the hackathon page and the Binance Web3 docs list.

Time from opening the docs to a first working signed request: not measured. I did not time it. I made the product decision layer first and the API call second, which was the right order for the product and the wrong order for this scoring rubric.

First successful signed call: by 7 Oct 2026 (the premarket capture saved in the repo).

Docs opened:

- https://www.bnbchain.org/en/hackathons/tokenized-stocks
- https://web3.binance.com/en/dev-docs/introduction
- https://web3.binance.com/en/dev-docs/authentication
- https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data
- Dev portal: https://web3.binance.com/en/dev-portal

## Documentation issues

- The stack is split across web3.binance.com/en/dev-docs, developers.binance.com (Agentic Wallet) and the hackathon page. I had to reconstruct "start here" myself.
- Authentication and RWA Data are separate pages. There is no one-page path from "create a key" to "list tokenized stocks on BSC with their status".
- It is not obvious from the landing docs which module answers "can this tokenized stock become stablecoins tonight?", which is the question HOP asks.
- I could not find where the market status values are listed. I saw premarket, regular, postmarket, closed, offhours and paused, and some tokens with no status at all. If there is a documented list, I did not find it.

## API pitfalls (measured)

1. **Geo-block with an unhelpful error.** The same signed call that worked from my Mac in Ireland returned `code=40304, Service not available due to compliance restriction` when run from GitHub Actions (US-hosted servers). Nothing in the error says which regions are served. A clearer message, or a list of supported regions, would have saved a day of debugging. The key was fine, the request was fine, and the host's location was the problem.
2. **`paused` is an undocumented stage, as far as I can tell.** On 13 and 14 Oct I called the endpoint every 30 to 120 seconds across the US open and close. At both ends the status goes through `paused` with reason `MARKET_PAUSED`, for roughly 2 to 4 minutes, staggered across tokens. I do not know why a market is paused.
3. **Some tokens have no market status.** 46 of 488 tokens returned no status all day, while their reason was `TRADING`. In the rows I inspected they were bstock tokens. I have not checked every row. HOP refuses these rather than guessing.
4. **`next_open` and `next_close` describe the next extended session, not the next regular session**, as far as I can tell. HOP uses its own regular-hours calendar instead.
5. **`UNSUPPORTED` as a reason.** Tokens can read `postmarket` with reason `UNSUPPORTED`, which I interpret as "not supported in the current session even though the market is open". 122 of 442 tokens did this after the close. I would like to confirm that reading.
6. **The feed leaves `regular` about a minute before 16:00 New York.** On 14 Oct the first `paused` reading was at 20:59 Irish time. HOP now treats the last 2 minutes of the session as closed. This is one session, not a rule.
7. **Reliability.** 30 calls at 30-second intervals on 14 Oct, no errors seen. I did not measure latency or rate limits.

### What the feed did at the open and close (counts, 442 tokens with a status)

Open, Tue 13 Oct, Irish time:

| Time | Regular | Paused | Premarket |
|---|---|---|---|
| 14:27 | 0 | 39 | 403 |
| 14:29 | 0 | 325 | 117 |
| 14:31 | 424 | 18 | 0 |
| 14:33 | 442 | 0 | 0 |

Close, Wed 14 Oct, Irish time:

| Time | Regular | Paused | Postmarket (trading / unsupported) |
|---|---|---|---|
| 20:58:33 | 442 | 0 | 0 |
| 20:59:04 | 129 | 313 | 0 |
| 20:59:36 | 1 | 441 | 0 |
| 21:00:08 | 0 | 442 | 0 |
| 21:00:39 | 0 | 442 | 0 |
| 21:01:10 | 0 | 109 | 265 / 68 |
| 21:01:42 | 0 | 84 | 290 / 68 |
| 21:02:13 | 0 | 0 | 320 / 122 |

## AI stack

Not used in the demo at runtime. No Agentic Wallet, no Wallet Skills CLI, no BNB Agent Studio.

I used AI to help write the spec, the local HTML demo, and the feed script. That is development help, not an integration.

If HOP later executes, an agent should explain a blocked hop and draft a policy. It should not be the signer.

## Tokenized-stock specifics

Measured: the status behaviour above, and that 442 of 488 tokens read `regular` at 15:44 New York on 12 Oct.

Not measured, still hypothesis:

- Whether an on-chain quote and a sell that actually completes differ off-hours.
- Liquidity, slippage, or reference-price gaps. I have not pulled them and will not claim them.
- Tokenized stocks can trade when the US cash market is closed, but a treasury still cannot treat that as instant spendable cash if eligibility, venue hours or redemption windows disagree.
- Ondo, bStocks and xStocks are different wrappers for a similar idea. HOP needs one settle-now flag per wrapper, not one flag for "stocks".

## If I rebuilt the developer platform

1. One "first call in 15 minutes" page: create a key, copy a curl that lists tokenized stocks on BSC with their market status, copy a second curl that quotes a spot sell to USDT.
2. A documented list of every market status and reason code, including `paused`, `UNSUPPORTED` and the no-status case.
3. A single field on each asset: tradable now, next regular cut-off, sell allowed off-hours yes or no. That is HOP's input.
4. Clear errors for blocked regions, naming the cause.
5. A dry-run response that says blocked-and-why in plain English, not only a numeric code.
6. Keep RWA Data, Trading and Transaction on one worked example for the same ticker across Ondo, bStocks and xStocks.

## Requested capabilities

- `canSettleNow(asset, side, wallet)`: eligibility, market hours and sell window.
- The same underlying ticker across the three wrappers in one response.
- A paper or simulate mode that does not require broadcasting.
- The next regular open and close, separate from the extended sessions.

## What I did and what is next

Done:

1. Created the Web3 API key.
2. Made RWA Data calls and saved the raw JSON in the repo (`rwa-platforms.json`, `rwa-tokens-bsc.json`).
3. Mapped the market status onto HOP: each token gets Allow only when the feed reads `regular`, the clock agrees, the feed is fresh and a regular window remains. Everything else is refused with a reason.
4. Captured the feed across the open and close, and put the timelines on the Markets tab.

Next: a weekend capture, per-sleeve rules for real T-bill funds (USYC, BUIDL, BENJI), an always-on host for the feed, and conversations with treasury teams.

HOP is a policy demo with a live read-only data feed. It does not execute trades or move funds.
