---
name: day-trader-skill
description: Suite of 11 modular day trading skills for US equities — scan thousands of charts, track SEC breaking news, time entries and exits, replay Monte Carlo odds with Time Machine, size positions, enforce risk limits, and paper trade with zero external dependencies.
category: finance
risk: safe
source: community
source_repo: "Jakeschincariol/day-trader-skill"
author: "Jake Schincariol"
tags: ["day-trading", "finance", "stocks", "market-scanner", "sec-edgar", "risk-management", "alpaca", "monte-carlo"]
date_added: "2026-10-26"
---

# The Day Trader Skill Suite

A complete suite of 11 modular skills for day trading US equities: scan thousands of charts, track breaking news, time entries and exits, and replay every outcome before risking a dollar.

Free, open-source (MIT), zero external dependencies (pure Python 3.8+ using standard library), no API keys required for public market data.

## The 11 Sub-Skills

| Skill / Command | Subpath | Role | Description |
| --- | --- | --- | --- |
| `/trader-scanner` | `day-trader-skill/trader-scanner` | Chart Scanner | Scans thousands of charts for setups: opening-range breakouts, flags, oversold bounces. |
| `/trader-news` | `day-trader-skill/trader-news` | News Monitor | Tracks breaking news on every stock you watch and flags SEC 8-K filings. |
| `/trader-entry` | `day-trader-skill/trader-entry` | Entry Timer | Watches a setup bar by bar and alerts the exact moment to enter. |
| `/trader-exit` | `day-trader-skill/trader-exit` | Exit Planner | Sets stop-loss and take-profit targets before entry. |
| `/trader-timemachine` | `day-trader-skill/trader-timemachine` | Time Machine | Replays 10,000 Monte Carlo sessions from recent 5-min bars to evaluate setup odds. |
| `/trader-risk` | `day-trader-skill/trader-risk` | Risk Manager | Enforces max loss, daily limits, position caps, and trading windows. |
| `/trader-budget` | `day-trader-skill/trader-budget` | Budget Manager | Sizes position to budget and creates Alpaca bracket order specifications. |
| `/trader-broker` | `day-trader-skill/trader-broker` | Order Executor | Routes paper/live orders with explicit user confirmation cards. |
| `/trader-alerts` | `day-trader-skill/trader-alerts` | Price Alerts | Tracks price levels, stop triggers, and NYSE market open/close bells. |
| `/trader-analyst` | `day-trader-skill/trader-analyst` | Earnings Analyst | Summarizes XBRL metrics from SEC EDGAR (10-Q/10-K). |
| `/trader-pelosi` | `day-trader-skill/trader-pelosi` | Pelosi Tracker | Monitors congressional stock trade filings (STOCK Act PTRs). |

## Trading Workflow Pipeline

All skills collaborate through a structured pipeline storing state in the local `trader/` directory:

```text
scanner -> news -> entry -> exit -> timemachine -> budget -> risk -> broker   (one trade cycle)
alerts: stop, target, flat by the close                                       (while open)
news / analyst / pelosi                                                        (scheduled background)
```

## Quick Start Runbook

```bash
# 1. Scan pre-market or intraday opening-range breakouts
python3 skills/day-trader-skill/trader-scanner/scan.py daily

# 2. Monitor breaking news on watchlist
python3 skills/day-trader-skill/trader-news/news.py check

# 3. Time breakout entry on 5-min bars
python3 skills/day-trader-skill/trader-entry/entry.py watch TSLA

# 4. Plan risk-defined exit levels
python3 skills/day-trader-skill/trader-exit/exit.py plan TSLA --entry 364.18

# 5. Run Time Machine Monte Carlo simulation
python3 skills/day-trader-skill/trader-timemachine/timemachine.py run TSLA

# 6. Size position to maximum dollar risk
python3 skills/day-trader-skill/trader-budget/size.py calculate

# 7. Validate risk constraints
python3 skills/day-trader-skill/trader-risk/check.py validate

# 8. Dispatch order (Paper trading default)
python3 skills/day-trader-skill/trader-broker/ticket.py preview
```

> **Disclaimer**: For educational and paper-trading purposes only. Not financial advice. Past performance and simulated Monte Carlo runs do not guarantee future returns.
