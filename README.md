# EV Expansion Helper

## Who this dashboard is for and what decision it supports

This app is for the **European expansion manager** at an EV charging network operator.
Every quarter he has to decide **which country to prioritize for new charging stations
next quarter**. Today he guesses from scattered feedback from the sales team, has no
unified view of the market, and often re-invests in markets that are already crowded
while missing fast-growing ones.

This app gives him one page showing: how many stations already exist per country,
how fast the selected country is growing month over month, and which connector types
are most common there — so he can put the quarterly budget where it actually matters.

## What I showed, what I cut, and why

**Kept — three charts:**

1. **Stations per country (bar chart)** — directly serves the "which country" decision.
2. **Monthly new stations in the selected country (line chart)** — shows whether the
   market is accelerating or slowing down, so he doesn't enter a fading market.
3. **Connector type distribution** — decides whether to build CCS or Type 2 at new
   sites, which drives hardware purchasing.

**Cut:**

- **Map scatter plot** — the raw data has coordinate errors (e.g. lat/lon both equal
  to 1.0), and it adds no information for a country-level decision. The manager
  chooses countries, not individual points.
- **Town-level breakdown** — too fine-grained. A quarterly budget is not allocated
  per town, and it would only make the page cluttered.
- **Raw data table** — low information density; the manager will not read it row by row.

The design principle is "small and precise": one page answers one question.

## Data refresh frequency

The data should refresh **once every night**. The manager's decision cycle is quarterly,
but new stations appear month by month, so a daily refresh keeps his view current without
the unnecessary cost of real-time streaming. v1 uses a manually uploaded CSV; if the
expansion team grows beyond 5 people, we can switch to an API-based automatic update.

## Known limitations

- The dataset is simulated; findings apply to this data only and do not represent the
  real EV charging market.
- Some records are missing `state` and `connector_types`; these were cleaned at load time.
- Electricity prices and government subsidies are not included, though they also affect
  real expansion decisions.
