from flask import Flask, render_template
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

ACOES = {
    "Petrobras": "PETR4.SA",
    "Itaú": "ITUB4.SA",
    "Vale": "VALE3.SA",
}

CORES = {
    "Petrobras": "#1f77b4",
    "Itaú": "#ff7f0e",
    "Vale": "#2ca02c",
}


def buscar_dados():
    tickers = list(ACOES.values())
    df = yf.download(tickers, start="2025-01-01", end="2026-01-01", auto_adjust=True)["Close"]
    df.rename(columns={v: k for k, v in ACOES.items()}, inplace=True)
    df = df.dropna(how="all")
    return df


def calcular_resumo(df):
    resumo = []
    for nome in ACOES:
        serie = df[nome].dropna()
        if serie.empty:
            continue
        preco_inicial = serie.iloc[0]
        preco_final = serie.iloc[-1]
        variacao = ((preco_final - preco_inicial) / preco_inicial) * 100
        resumo.append({
            "nome": nome,
            "inicial": f"R$ {preco_inicial:.2f}",
            "final": f"R$ {preco_final:.2f}",
            "variacao": f"{variacao:+.2f}%",
            "positivo": variacao >= 0,
            "maxima": f"R$ {serie.max():.2f}",
            "minima": f"R$ {serie.min():.2f}",
        })
    return resumo


def grafico_historico(df):
    fig = go.Figure()
    for nome in ACOES:
        serie = df[nome].dropna()
        fig.add_trace(go.Scatter(
            x=serie.index,
            y=serie.values,
            name=nome,
            line=dict(color=CORES[nome], width=2),
            hovertemplate=f"<b>{nome}</b><br>Data: %{{x|%d/%m/%Y}}<br>Preço: R$ %{{y:.2f}}<extra></extra>",
        ))
    fig.update_layout(
        title="Histórico de Preços — 2025",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        legend=dict(orientation="h", y=-0.2),
        hovermode="x unified",
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI, sans-serif"),
        margin=dict(l=50, r=20, t=60, b=80),
    )
    return pio.to_html(fig, full_html=False, include_plotlyjs="cdn")


def grafico_retorno(df):
    fig = go.Figure()
    for nome in ACOES:
        serie = df[nome].dropna()
        normalizada = (serie / serie.iloc[0]) * 100
        fig.add_trace(go.Scatter(
            x=normalizada.index,
            y=normalizada.values,
            name=nome,
            line=dict(color=CORES[nome], width=2),
            hovertemplate=f"<b>{nome}</b><br>Data: %{{x|%d/%m/%Y}}<br>Retorno: %{{y:.1f}}<extra></extra>",
        ))
    fig.add_hline(y=100, line_dash="dot", line_color="gray", opacity=0.5)
    fig.update_layout(
        title="Retorno Comparativo — Base 100 em 01/01/2025",
        xaxis_title="Data",
        yaxis_title="Retorno (base 100)",
        legend=dict(orientation="h", y=-0.2),
        hovermode="x unified",
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI, sans-serif"),
        margin=dict(l=50, r=20, t=60, b=80),
    )
    return pio.to_html(fig, full_html=False, include_plotlyjs=False)


@app.route("/")
def index():
    df = buscar_dados()
    resumo = calcular_resumo(df)
    graf_hist = grafico_historico(df)
    graf_ret = grafico_retorno(df)
    return render_template("index.html", resumo=resumo, graf_hist=graf_hist, graf_ret=graf_ret)


if __name__ == "__main__":
    app.run(debug=True)
