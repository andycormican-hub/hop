# HOP

HOP moves treasury cash between spendable dollars (USDC-class payment stablecoins) and earning dollars (approved tokenized T-bill / money-market sleeves). It pulls cash back before a payment is due. It refuses the hop if settlement cannot complete. v1 is for a firm's own on-chain treasury — crypto treasury, market maker, or venue desk. Not retail. Not other people's money. Not fake 24/7 redemption.

---

## 2. Who it is for / who it is not for

**For:**
- Treasury ops at a crypto-native firm running its own on-chain treasury.
- A market maker or venue desk holding working capital in payment stablecoins.
- A finance or ops person who already does this move by hand and wants the timing enforced by policy instead of memory.

**Not for:**
- Retail users managing personal savings.
- Asset managers, fund admins, or anyone moving other people's money.
- Anyone who expects instant redemption with no cutoffs, no allowlists, no weekend limits.
- Anyone looking for a new stablecoin, a token, a wallet app, or a savings/wellness product.

---

## 3. v1 scope

**Must include:**
- Policy screen: spendable floor, yield sleeve selection, pull-back lead time, weekend rule.
- Preview screen: one proposed action (park or recall), a can-it-settle-now check, a reason when the answer is no, and a Queue vs Blocked routing.
- Ledger screen: a log of actions with status Queued / Settled / Blocked / Refused.
- One payment stablecoin (USDC-class) and one demo yield sleeve (labeled USYC/BUIDL-class, dummy data only).
- A visible Refused state — this is a feature, not an error screen.

**Must not include:**
- Wallet connect, key custody, or signing flows.
- Smart contracts or any real on-chain execution.
- Multiple currencies, multiple chains, or multiple sleeves in v1.
- Yield paid on the payment stablecoin itself — illegal under the GENIUS Act, and not what HOP does.
- Retail, consumer, wallet, token-sale, or wellness framing of any kind.
- Real custody, redemption, or brokerage integration.

---

## 4. Three screens, in spec form

### Screen 1 — Policy

Purpose: set the rules HOP enforces before it will move anything.

| Field | Type | Description |
|---|---|---|
| Spendable floor | dollar amount | Minimum USDC balance that must always remain spendable. HOP will not recommend a park that drops the balance below this. |
| Yield sleeve | dropdown, single-select | The approved tokenized T-bill / MMF product holding earning dollars. v1 shows one option: "Demo T-bill sleeve (USYC-class)." |
| Pull-back lead time | hours or business days | How far in advance of a scheduled payment HOP must have cash back in spendable form. |
| Weekend rule | dropdown: Allow / Block / Delay to next business day | Whether HOP will attempt a recall over the weekend, or hold it until the sleeve's redemption window reopens. |

UI copy:
- Section header: "Set the rules. HOP follows them — it doesn't improvise."
- Save button: "Save policy"
- Confirmation toast: "Policy saved. HOP will check every proposed hop against these rules."

### Screen 2 — Preview

Purpose: show one proposed action and whether it can actually settle.

Layout:
- Proposed action: "Park $70,000 to Demo T-bill sleeve" or "Recall $25,000 to spendable USDC"
- Can it settle now: **YES** / **NO**, shown as a single, unmissable badge
- If NO, one plain-language reason directly under the badge
- Routing: **Queue** (timing will resolve on its own — proceed automatically when conditions are met) or **Blocked** (needs a manual fix before HOP will proceed)
- Buttons: "Confirm" (disabled when NO) / "Cancel"

UI copy:
- YES state: "Settlement can complete now. Confirm to proceed."
- NO state (Blocked example): "Cannot settle. Destination wallet is not on the allowlist. Add it in Settings, then retry."
- NO state (Queue example): "Cannot settle yet. Recall window opens Monday 09:00. This will retry automatically."

### Screen 3 — Ledger

Purpose: a plain record of every hop and what happened to it.

Columns: Date/time, Action, Amount, Status, Reason (if not Settled)

Status values:
- **Queued** — condition not yet met (a lead-time window, a redemption cutoff); HOP will retry automatically.
- **Settled** — cash moved and confirmed.
- **Blocked** — a fixable problem is stopping the hop (e.g., allowlist); needs manual action.
- **Refused** — HOP declined to attempt the hop because it could not guarantee settlement in time. This is HOP protecting the payment, not a system failure.

UI copy:
- Empty state: "No hops yet. Set a policy and propose one."
- Row detail on click: plain sentence restating the reason column.

---

## 5. Dummy demo numbers

- Spendable floor: **$50,000**
- Starting USDC: **$120,000**
- Proposed park: **$70,000** (leaves exactly $50,000 spendable — right at the floor)

Ledger, populated:

| Date/time | Action | Amount | Status | Reason |
|---|---|---|---|---|
| Mon 09:02 | Park to Demo T-bill sleeve | $70,000 | Settled | — |
| Tue 14:10 | Recall to spendable USDC | $15,000 | **Blocked** | Destination wallet not on allowlist |
| Sat 08:00 | Recall to spendable USDC | $25,000 | **Refused** | Weekend recall — sleeve redemption window closed until Monday 09:00; payment due Monday 08:00 cannot be guaranteed |
| Sun 20:00 | Recall to spendable USDC | $10,000 | Queued | Pull-back lead time not yet reached; will retry when window opens |
| Wed 09:00 | Recall to spendable USDC | $70,000 | Settled | Recalled 24h ahead of Thursday payment per policy |

---

## 6. 90-second demo script

"This is HOP. It moves treasury cash between spendable dollars — USDC — and earning dollars, a tokenized T-bill sleeve. It's for a firm's own treasury. Not retail, not custody for anyone else.

Here's the policy screen. We've set a spendable floor of fifty thousand dollars, a pull-back lead time of twenty-four hours, and a weekend rule that blocks recalls until Monday morning. That's because payment stablecoins can't pay yield under the GENIUS Act — that's the whole reason this hop exists — and the T-bill sleeve still has real redemption cutoffs. Instant isn't real unless there's a buffer.

Preview screen. We start with a hundred and twenty thousand dollars in USDC. HOP proposes parking seventy thousand into the demo sleeve — that leaves exactly the fifty-thousand floor spendable. It checks: can this settle now? Yes. Confirm.

Now the ledger. That park settled. Here's a recall that's Blocked — the destination wallet isn't on the allowlist, so HOP won't move money into an unapproved address. And here's one that's Refused — someone asked for a weekend recall, but the sleeve's redemption window is closed until Monday, and a payment is due before that window opens. HOP refuses rather than promise a settlement it can't guarantee.

That's the product. Queued, Settled, Blocked, Refused. Four honest states, no exceptions."

---

## 7. Builder prompt (paste into Lovable, Bolt, v0, or Replit)

```
Build a three-screen demo web app called HOP. Dummy data only — no wallet connect, no blockchain libraries, no smart contracts, no real backend. All data lives in local state or a static JSON file.

HOP moves treasury cash between "spendable dollars" (a USDC-class payment stablecoin) and "earning dollars" (a demo tokenized T-bill sleeve, labeled "Demo T-bill sleeve (USYC-class)" — this is a label only, not a real integration).

Screen 1 — Policy:
A form with four fields: Spendable floor (dollar input), Yield sleeve (dropdown, one option: "Demo T-bill sleeve (USYC-class)"), Pull-back lead time (number + unit: hours/business days), Weekend rule (dropdown: Allow / Block / Delay to next business day). A "Save policy" button and a confirmation toast on save.

Screen 2 — Preview:
Shows one proposed action as a card: "Park $70,000 to Demo T-bill sleeve" (or a recall). Below it, a large YES/NO badge answering "Can it settle now?" If NO, show one plain-language reason line. Below that, a routing tag: "Queue" or "Blocked". A "Confirm" button (disabled if NO) and a "Cancel" button.

Screen 3 — Ledger:
A table with columns: Date/time, Action, Amount, Status, Reason. Status is one of exactly four values, each with a distinct color/badge: Queued (gray/blue), Settled (green), Blocked (orange), Refused (red). Seed it with this data:
- Mon 09:02 | Park to Demo T-bill sleeve | $70,000 | Settled | —
- Tue 14:10 | Recall to spendable USDC | $15,000 | Blocked | Destination wallet not on allowlist
- Sat 08:00 | Recall to spendable USDC | $25,000 | Refused | Weekend recall — sleeve redemption window closed until Monday 09:00; payment due Monday 08:00 cannot be guaranteed
- Sun 20:00 | Recall to spendable USDC | $10,000 | Queued | Pull-back lead time not yet reached
- Wed 09:00 | Recall to spendable USDC | $70,000 | Settled | Recalled 24h ahead of Thursday payment per policy

Starting USDC balance shown in the app header: $120,000. Spendable floor: $50,000.

Tone: plain, operator-facing, no marketing copy, no hype. Simple nav between the three screens (tabs or sidebar). No auth, no login. Add a fixed footer line on every screen: "Demo only. Does not move client funds. Not an offer of securities."
```

---

## 8. Disclaimer

Demo only. Does not move client funds. Not an offer of securities.

---

## Checklist — confirm these visually once the demo is generated

1. Header shows starting balance of $120,000 and spendable floor of $50,000.
2. Policy screen has exactly four fields: spendable floor, yield sleeve, pull-back lead time, weekend rule.
3. Yield sleeve dropdown shows only "Demo T-bill sleeve (USYC-class)" — no other tokens, no wallet, no mint claim anywhere.
4. Preview screen shows one proposed action at a time, not a list.
5. YES/NO can-it-settle-now badge is large and unambiguous, not buried in text.
6. A NO result always shows a one-line reason directly below the badge.
7. Queue vs Blocked are visually distinct and both appear somewhere in the demo.
8. Ledger shows all four status values: Queued, Settled, Blocked, Refused — each with a distinct visual treatment.
9. The Blocked row reads "wallet not allowlisted" and the Refused row reads "weekend recall" — both present, worded plainly.
10. Disclaimer line appears on every screen, unmodified: "Demo only. Does not move client funds. Not an offer of securities."
