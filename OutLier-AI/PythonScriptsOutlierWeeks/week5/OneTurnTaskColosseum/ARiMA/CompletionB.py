import numpy as np
import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model
from scipy.stats import norm
from arch.__future__ import reindexing
import warnings
warnings.filterwarnings('ignore')
import warnings
warnings.filterwarnings("ignore")          # silence statsmodels / arch spam
plt.style.use('seaborn-v0_8')              # nicer plots

# ---------- parameters you may want to tweak ----------------------
look_back_windows = [180, 365, 540, 730]   # days of history to feed the models
forecast_horizon   = 38                    # must match the horizon in main code
mc_paths           = 5_000                 # cut to 5k for speed during back‑test
# ------------------------------------------------------------------


# ------------- helper : Monte‑Carlo forecast ----------------------
def mc_point_forecast(price_series, horizon, n_paths=10_000,
                      seed=24, vol_of_vol=0.35):
    """Return one point forecast (mean of terminal distribution)."""
    np.random.seed(seed)
    last_price = price_series.iloc[-1]
    log_rets   = np.log(price_series/price_series.shift(1)).dropna()

    curr_vol   = log_rets.std()
    peak_vol   = curr_vol*2
    sim_prices = np.zeros((horizon, n_paths))
    sim_prices[0] = last_price

    for t in range(1, horizon):
        vol_shock = np.random.normal(0, vol_of_vol, n_paths)
        curr_vol  = np.abs(curr_vol + vol_shock)
        curr_vol  = np.minimum(curr_vol, peak_vol)

        norm_r    = np.random.normal(log_rets.mean() - (curr_vol**2)/2,
                                     curr_vol/np.sqrt(252), n_paths)
        sim_prices[t] = sim_prices[t-1]*np.exp(norm_r)

    return sim_prices[-1].mean()           # point estimate


# ------------- helper : ARIMA‑GARCH forecast ----------------------
def arima_garch_point_forecast(price_series, horizon):
    """Return one point forecast (ARIMA mean path only)."""
    log_rets = np.log(price_series/price_series.shift(1)).dropna()

    # ARIMA
    arima_res   = ARIMA(log_rets, order=(5,0,2)).fit()
    arima_fcst  = arima_res.forecast(steps=horizon)
    cum_log_ret = arima_fcst.sum()

    # price
    start_price = price_series.iloc[-1]
    return start_price*np.exp(cum_log_ret)  # point estimate


# ------------- back‑test loop -------------------------------------
results = []

# last date used in your original download
anchor_date   = pd.to_datetime("2024-01-30")        # same as end= in main script
anchor_price  = past_data['Close'].iloc[-1]

for window in look_back_windows:
    # training slice
    train_start = (anchor_date - pd.Timedelta(days=window)).strftime('%Y-%m-%d')
    train_end   = anchor_date.strftime('%Y-%m-%d')
    train_df    = yf.download(asset_symbol, start=train_start, end=train_end,
                              progress=False)

    # skip if not enough data
    if len(train_df) < 100:
        continue

    # forecasts
    mc_price   = mc_point_forecast(train_df['Close'], forecast_horizon,
                                   n_paths=mc_paths)
    ag_price   = arima_garch_point_forecast(train_df['Close'], forecast_horizon)

    # fetch the *true* price 38 calendar days later
    true_end   = (anchor_date + pd.Timedelta(days=forecast_horizon)).strftime('%Y-%m-%d')
    true_df    = yf.download(asset_symbol, start=anchor_date, end=true_end,
                             progress=False)

    # if the market was closed on the exact day, take the last available
    true_price = true_df['Close'].iloc[-1]

    # metrics -------------------------------------------------------
    def metrics(pred, actual, start):
        direction_ok = np.sign(pred - start) == np.sign(actual - start)
        pct_err      = (pred - actual)/actual * 100
        return direction_ok, pct_err

    mc_dir, mc_err = metrics(mc_price, true_price, anchor_price)
    ag_dir, ag_err = metrics(ag_price, true_price, anchor_price)

    results.append({
        "look_back_days": window,
        "MC_price": mc_price, "ARIMA_GARCH_price": ag_price,
        "Actual_price": true_price,
        "MC_direction_hit": mc_dir,   "AG_direction_hit": ag_dir,
        "MC_%error": mc_err,          "AG_%error": ag_err
    })

# ------------- summary table --------------------------------------
summary = pd.DataFrame(results)
pd.set_option('display.float_format', '{:,.2f}'.format)
print("\n=== Back‑test results (38‑day horizon) ===")
print(summary[['look_back_days',
               'MC_direction_hit','MC_%error',
               'AG_direction_hit','AG_%error']])

# ------------- quick visual of % errors ---------------------------
if not summary.empty:
    summary.set_index('look_back_days')[['MC_%error','AG_%error']].plot(
        kind='bar', figsize=(10,4), title='Percentage error vs look‑back window')
    plt.axhline(0,color='k',lw=1)
    plt.ylabel('% error')
    plt.show()
