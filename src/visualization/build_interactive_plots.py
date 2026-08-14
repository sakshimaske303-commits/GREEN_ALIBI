"""Interactive Plotly versions of the three headline GREEN ALIBI charts.
Same underlying processed CSVs as the static figures - just Plotly instead
of matplotlib, so every line/point gets a hover tooltip and toggleable
legend instead of being locked into a flat PNG."""

import pandas as pd
import plotly.graph_objects as go
import colorsys
import os

DATA = "data/processed"
OUT = "outputs/interactive_maps/plots"
os.makedirs(OUT, exist_ok=True)

YEAR_COLORS_BASE = "#2FA88C"  # not used directly; per-year palette built below


def distinct_colors(n):
    colors = []
    for i in range(n):
        h = i / n
        r, g, b = colorsys.hls_to_rgb(h, 0.5, 0.65)
        colors.append("#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255)))
    return colors


DARK_LAYOUT = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="#0d1b2a",
    font=dict(family="Poppins, sans-serif", color="#F2F2F5"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    margin=dict(t=70, b=50, l=60, r=30),
)


# ============================================================
# 1. SEASONAL TRAJECTORIES — normalized SIF vs NDVI, per year
# ============================================================
def build_seasonal_trajectories():
    df = pd.read_csv(f"{DATA}/marathwada_sif_ndvi_merged.csv")
    rain = pd.read_csv(f"{DATA}/rainfall_anomaly_summary.csv")
    drought_years = set(rain.loc[rain["anomaly_zscore"] < -0.5, "year"])

    df["sif_norm"] = df.groupby("year")["mean_sif"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
    df["ndvi_norm"] = df.groupby("year")["mean_ndvi"].transform(lambda x: (x - x.min()) / (x.max() - x.min()))

    years = sorted(df["year"].unique())
    default_years = {2015, 2018}  # the two drought years, shown by default

    fig = go.Figure()
    for year in years:
        sub = df[df["year"] == year].sort_values("doy")
        tag = "drought year" if year in drought_years else "normal monsoon year"
        visible = True if year in default_years else "legendonly"
        fig.add_trace(go.Scatter(
            x=sub["doy"], y=sub["sif_norm"], mode="lines+markers", name=f"{year} SIF ({tag})",
            legendgroup=str(year), line=dict(color="#2FA88C", width=2), marker=dict(size=6),
            visible=visible,
            hovertemplate=f"{year} SIF<br>DOY %{{x}}<br>Normalized: %{{y:.3f}}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=sub["doy"], y=sub["ndvi_norm"], mode="lines+markers", name=f"{year} NDVI ({tag})",
            legendgroup=str(year), line=dict(color="#D98E30", width=2, dash="dot"), marker=dict(size=6, symbol="square"),
            visible=visible,
            hovertemplate=f"{year} NDVI<br>DOY %{{x}}<br>Normalized: %{{y:.3f}}<extra></extra>",
        ))

    fig.update_layout(
        title="Seasonal SIF vs. NDVI Trajectories, Marathwada (normalized to own peak)",
        xaxis_title="Day of Year", yaxis_title="Normalized value (0-1 within year)",
        height=560, hovermode="closest", **DARK_LAYOUT,
    )
    fig.write_html(f"{OUT}/seasonal_trajectories.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/seasonal_trajectories.html")


# ============================================================
# 2. LAG BY THRESHOLD — one line per year
# ============================================================
def build_lag_by_threshold():
    df = pd.read_csv(f"{DATA}/sif_ndvi_lag_by_threshold.csv")
    years = sorted(df["year"].unique())
    palette = distinct_colors(len(years))

    fig = go.Figure()
    for i, year in enumerate(years):
        sub = df[df["year"] == year].sort_values("threshold", ascending=False)
        tag = "drought" if sub["is_drought_year"].iloc[0] else "normal"
        fig.add_trace(go.Scatter(
            x=sub["threshold"], y=sub["lag_days"], mode="lines+markers",
            name=f"{year} ({tag})", line=dict(color=palette[i], width=2.5), marker=dict(size=8),
            hovertemplate=f"{year} ({tag})<br>Threshold: %{{x}}<br>Lag: %{{y}} days<extra></extra>",
        ))

    fig.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.4)")
    fig.update_layout(
        title="SIF-to-NDVI Decline Lag, by Threshold and Year — Marathwada",
        xaxis_title="Decline threshold (fraction of seasonal peak)",
        yaxis_title="NDVI lag behind SIF (days)",
        xaxis=dict(autorange="reversed"),
        height=560, hovermode="closest", **DARK_LAYOUT,
    )
    fig.write_html(f"{OUT}/lag_by_threshold.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/lag_by_threshold.html")


# ============================================================
# 3. BOOTSTRAP CI — cross-correlation lag point estimates + 95% CI
# ============================================================
def build_bootstrap_ci():
    df = pd.read_csv(f"{DATA}/cross_correlation_lag_bootstrap_ci.csv").sort_values("year").reset_index(drop=True)

    lower_err = df["point_estimate_lag_days"] - df["ci_2.5pct_days"]
    upper_err = df["ci_97.5pct_days"] - df["point_estimate_lag_days"]
    colors = ["#B23A48" if d else "#2FA88C" for d in df["is_drought_year"]]
    labels = [f"{int(y)}" + (" (drought)" if d else " (normal)") for y, d in zip(df["year"], df["is_drought_year"])]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=df["point_estimate_lag_days"], mode="markers",
        marker=dict(size=14, color=colors, line=dict(color="white", width=1)),
        error_y=dict(type="data", symmetric=False, array=upper_err, arrayminus=lower_err,
                      color="rgba(255,255,255,0.6)", thickness=1.5, width=6),
        customdata=df["pct_replicates_lag_geq_0"],
        hovertemplate="%{x}<br>Point estimate: %{y} days<br>95%% CI replicates ≥0: %{customdata:.1f}%%<extra></extra>",
        showlegend=False,
    ))
    fig.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.4)")
    fig.update_layout(
        title=f"Bootstrap 95% CI on Cross-Correlation Lag ({len(df)} years, 2,000 replicates/year)",
        xaxis_title="Year", yaxis_title="Cross-correlation-maximizing lag, NDVI behind SIF (days)",
        height=560, hovermode="closest", **DARK_LAYOUT,
    )
    fig.write_html(f"{OUT}/bootstrap_lag_ci.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/bootstrap_lag_ci.html")


if __name__ == "__main__":
    build_seasonal_trajectories()
    build_lag_by_threshold()
    build_bootstrap_ci()
