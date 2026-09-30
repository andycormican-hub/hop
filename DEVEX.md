# Hop — Developer Experience Report
BNB Hack: Tokenized Stocks Edition
Builder: Andy Cormican (solo)
Repo: https://github.com/andycormican-hub/hop
Demo: HOP.html in the repo
Video: linked from README

## What I built
Hop is a treasury policy demo. It parks idle stablecoins into a yielding sleeve and pulls them back before a payment. It refuses the hop when settlement cannot be guaranteed (allowlist, cutoff, weekend).

For this hack the intended sleeve is a tokenized stock on BSC (Ondo / bStocks / xStocks), paired with a spendable stablecoin. v1 is a local three-screen app: Policy, Preview, Ledger. Dummy balances. No wallet. No live transfer. That is deliberate. Hop must not look like it moved client funds.

## Onboarding
I am a solo builder, not a full-time engineer. I started from the hackathon page and the Binance Web3 docs list.

I have not completed a first successful authenticated API call yet. Time from opening the docs to a working signed request is therefore not measured. That is the main gap in this report.

Docs opened:
- https://www.bnbchain.org/en/hackathons/tokenized-stocks
- https://web3.binance.com/en/dev-docs/introduction
- https://web3.binance.com/en/dev-docs/authentication
- https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data
- Dev portal: https://web3.binance.com/en/dev-portal

Where I am stuck before a first call:
1. Need a Binance account or wallet on the developer portal for an API key.
2. Authentication page is written for people who already sign requests. I do not yet have a working HMAC / Ed25519 snippet in my own project.
3. I built the product decision layer first (when to hop, when to refuse) instead of starting at the API. That was the right product order and the wrong order for this scoring rubric.

## Documentation issues
I can only report what blocked me before a call, not a failed response body.

- The stack is split across web3.binance.com/en/dev-docs, developers.binance.com (Agentic Wallet), and the hackathon page. I had to reconstruct “start here” myself.
- Authentication and RWA Data are separate pages. There is no one-page “list Ondo / bStocks / xStocks for NVDA, then dry-run a spot buy” path for a first-hour builder.
- It is not obvious from the landing docs which module answers “can this tokenized stock become stablecoins tonight?” which is the question Hop actually asks.

## API pitfalls
None measured. No latency, no error codes, no signed-request failures in my logs. I will not invent them.

## AI stack
Not used in the demo. No Agentic Wallet, no Wallet Skills CLI, no BNB Agent Studio runtime.

I used AI to write the spec and the local HTML demo. That is allowed. It is not an integration.

If Hop later executes, the agent should explain a blocked hop and draft a policy. It should not be the signer.

## Tokenized-stock specifics
Not measured on live BSC books. Product hypothesis only:

- Tokenized stocks can trade when the US cash market is closed.
- A treasury still cannot treat that as instant spendable cash if eligibility, venue hours, or redemption/sell windows disagree.
- Ondo / bStocks / xStocks are different wrappers for a similar economic idea. Hop needs one settle-now flag per wrapper, not one flag for “stocks.”
- Weekend behaviour is the point of the product. I have not yet printed the difference between an on-chain quote and a sell that actually completes off-hours.

I will not claim liquidity, slippage, or reference-price gaps I have not pulled.

## If I rebuilt the developer platform
1. One “first call in 15 minutes” page: create key, copy a curl that lists tokenized stocks on BSC, copy a second curl that quotes a spot sell to USDT.
2. A single field on each asset: tradable now, next cutoff, sell allowed off-hours yes/no. That is the Hop input.
3. A dry-run transaction response that says blocked-and-why in plain English, not only a numeric code.
4. Keep RWA Data, Trading, and Transaction on one worked example for the same ticker across Ondo, bStocks, and xStocks.

## Requested capabilities
- canSettleNow(asset, side, wallet) — eligibility + market-hours + sell window.
- Same underlying ticker across the three wrappers in one response.
- Paper / simulate mode that does not require broadcasting.

## What I will do before 11 Oct if time allows
1. Create the Web3 API key.
2. Make one RWA Data call for an Ondo or bStocks ticker.
3. Put the raw JSON in the repo.
4. Map one field onto Hop Preview: settle-now YES/NO from real data instead of the toggle.

Until that lands, judges should treat Hop as a policy demo aimed at tokenized stocks, not as a Binance Web3 integration.
