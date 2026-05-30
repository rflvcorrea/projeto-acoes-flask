# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server (debug mode, auto-reload)
python app.py

# Run production server (as deployed)
gunicorn app:app
```

## Architecture

Single-file Flask app (`app.py`) with one route (`/`) that fetches live stock data on every request and renders it into `templates/index.html`.

**Data flow per request:**
1. `buscar_dados()` — calls `yf.download()` for the three tickers (PETR4.SA, ITUB4.SA, VALE3.SA), hardcoded date range 2025-01-01 → 2026-01-01, returns a DataFrame with company names as columns.
2. `calcular_resumo(df)` — computes open/close/high/low/variation per stock, formats values as BRL strings with sign.
3. `grafico_historico(df)` — raw price chart (Plotly Scatter), returns HTML fragment with Plotly.js loaded from CDN.
4. `grafico_retorno(df)` — base-100 normalized return chart (Plotly.js reused from the first chart's CDN load, `include_plotlyjs=False`).
5. All three outputs are injected into the Jinja2 template as `resumo`, `graf_hist`, and `graf_ret`.

**Key constants in `app.py`:**
- `ACOES` — maps display names to Yahoo Finance ticker symbols; add/remove stocks here.
- `CORES` — per-stock line colors used in both charts.

**Deployment:** `Procfile` targets Heroku/Railway-style platforms via `gunicorn app:app`.

## GitHub

Repositório: https://github.com/rflvcorrea/projeto-acoes-flask

**Auto-sync:** toda alteração feita pelo Claude Code via Edit ou Write é automaticamente commitada e enviada ao GitHub via hook configurado em `.claude/settings.json`. Não é necessário fazer push manualmente.

Para atualizar manualmente:
```bash
git add -A
git commit -m "mensagem"
git push origin master
```
