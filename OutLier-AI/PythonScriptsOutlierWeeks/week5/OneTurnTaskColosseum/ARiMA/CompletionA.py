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

# Fetch past data
asset_symbol = "GOOGL"
past_data = yf.download(asset_symbol, start="2023-01-01", end="2024-01-30")

# Compute daily log returns
daily_log_returns = np.log(past_data['Close'] / past_data['Close'].shift(1))
daily_log_returns.dropna(inplace=True)
daily_log_returns.index = pd.DatetimeIndex(daily_log_returns.index).to_period('D')

# Setup Monte Carlo simulation parameters
forecast_horizon = 38  # Days
simulations = 10000
starting_price = past_data['Close'].iloc[-1]

# Initiate simulation
np.random.seed(24)
simulated_prices = np.zeros((forecast_horizon, simulations))
simulated_prices[0] = starting_price

# Perform Stochastic Volatility with a checked volatility shock threshold
curr_volatility = daily_log_returns.std()
vol_shock_intensity = 0.35  # Volatility of volatility
peak_volatility = curr_volatility * 2  # Max limit to control explosion

for t in range(1, forecast_horizon):
    # Random shock for volatility capped
    vol_shock = np.random.normal(0, vol_shock_intensity, simulations)
    curr_volatility = np.abs(curr_volatility + vol_shock)
    curr_volatility = np.minimum(curr_volatility, peak_volatility)

    # Geometric Brownian Motion with adjusted volatility
    norm_returns = np.random.normal(daily_log_returns.mean() - (curr_volatility ** 2) / 2, curr_volatility / np.sqrt(252),
                                    simulations)

    # Update simulated prices
    simulated_prices[t] = simulated_prices[t - 1] * np.exp(norm_returns)

# Visualization of simulation
plt.figure(figsize=(10, 6))
for i in range(simulations):
    plt.plot(simulated_prices[:, i], linewidth=0.5, alpha=0.2, color='gray')
plt.plot(simulated_prices.mean(axis=1), color='blue', linewidth=2, label='Average Path')
plt.title(f"Monte Carlo Simulation of {asset_symbol} Over {forecast_horizon} Days")
plt.xlabel("Days")
plt.ylabel("Price")
plt.legend()
plt.show()

# Estimating the price using Monte Carlo
predicted_price_mc = simulated_prices[-1].mean()
print(f"The predicted price of {asset_symbol} {forecast_horizon} days ahead is around: ${predicted_price_mc:.2f}")

# Computing VaR and ES for Monte Carlo
confidence_interval_mc = 0.95
sorted_prices_mc = np.sort(simulated_prices[-1])
VaR_mc = np.percentile(sorted_prices_mc, (1 - confidence_interval_mc) * 100)
ES_mc = sorted_prices_mc[sorted_prices_mc <= VaR_mc].mean()

print(f"Monte Carlo Value at Risk (95% confidence): ${VaR_mc:.2f}")
print(f"Monte Carlo Expected Shortfall: ${ES_mc:.2f}")

# ARIMA model for Returns Prediction
arima_model = ARIMA(daily_log_returns, order=(5, 0, 2))  # Example parameters; tweak as needed for your dataset
arima_result = arima_model.fit()
arima_prediction = arima_result.forecast(steps=38)  # Predicting next 30 days

# GARCH for Volatility Prediction
garch_model = arch_model(daily_log_returns*100, mean='Zero', vol='Garch', p=1, q=1)  # Scaling by 100
garch_result = garch_model.fit(update_freq=5, disp='off')
garch_prediction = garch_result.forecast(horizon=38)
predicted_volatility = np.sqrt(garch_prediction.variance.values[-1, :]) / 100  # Rescaling by dividing by 100

# Combining ARIMA and GARCH forecasts for a unified prediction
predicted_log_return = arima_prediction.sum()
predicted_price_arima_garch = starting_price * np.exp(predicted_log_return / 100)
print(f"Predicted price using ARIMA-GARCH: ${predicted_price_arima_garch:.2f}")

# Calculating Value at Risk (VaR) and Expected Shortfall (ES) for ARIMA-GARCH
confidence_interval = 0.95
z_value = norm.ppf(confidence_interval)

VaR_arima_garch = starting_price - (starting_price * np.exp(-z_value * predicted_volatility[-1]))
ES_arima_garch = starting_price - (starting_price * np.exp(-z_value * predicted_volatility[-1] / (1 - confidence_interval)))
print(f"Value at Risk using ARIMA-GARCH (95% confidence): ${VaR_arima_garch:.2f}")
print(f"Expected Shortfall using ARIMA-GARCH: ${ES_arima_garch:.2f}")

# =============================================================================
# BACKTESTING SECTION
# =============================================================================

def backtest_models(asset_symbol, base_end_date, forecast_days=30, historical_spans=[180, 252, 365, 500, 730]):
    """
    Backtest both Monte Carlo and ARIMA-GARCH models over different historical data spans
    
    Parameters:
    - asset_symbol: Stock symbol to analyze
    - base_end_date: The date to use as the "prediction point"
    - forecast_days: Number of days to forecast ahead
    - historical_spans: List of historical data spans (in days) to test
    """
    
    print("\n" + "="*80)
    print("BACKTESTING ANALYSIS")
    print("="*80)
    
    results = []
    
    for span in historical_spans:
        print(f"\nTesting with {span} days of historical data...")
        
        try:
            # Calculate training period dates
            train_start = pd.to_datetime(base_end_date) - pd.Timedelta(days=span)
            train_end = base_end_date
            
            # Fetch training data
            train_data = yf.download(asset_symbol, start=train_start.strftime('%Y-%m-%d'), 
                                   end=train_end, progress=False)
            
            if len(train_data) < 50:  # Skip if insufficient data
                print(f"Insufficient data for {span} days span")
                continue
            
            # Compute log returns for training
            train_log_returns = np.log(train_data['Close'] / train_data['Close'].shift(1))
            train_log_returns.dropna(inplace=True)
            
            train_starting_price = train_data['Close'].iloc[-1]
            
            # Fetch actual future data for comparison
            future_start = pd.to_datetime(base_end_date) + pd.Timedelta(days=1)
            future_end = pd.to_datetime(base_end_date) + pd.Timedelta(days=forecast_days + 10)  # Buffer for weekends
            
            future_data = yf.download(asset_symbol, start=future_start.strftime('%Y-%m-%d'), 
                                    end=future_end.strftime('%Y-%m-%d'), progress=False)
            
            if len(future_data) < forecast_days:
                print(f"Insufficient future data for validation")
                continue
            
            # Get actual price after forecast_days (accounting for weekends/holidays)
            if len(future_data) >= forecast_days:
                actual_future_price = future_data['Close'].iloc[forecast_days-1]
            else:
                actual_future_price = future_data['Close'].iloc[-1]
            
            # =============================================================================
            # MONTE CARLO PREDICTION
            # =============================================================================
            np.random.seed(42)  # For reproducibility in backtesting
            mc_simulated_prices = np.zeros((forecast_days, simulations))
            mc_simulated_prices[0] = train_starting_price
            
            mc_curr_volatility = train_log_returns.std()
            mc_vol_shock_intensity = 0.35
            mc_peak_volatility = mc_curr_volatility * 2
            
            for t in range(1, forecast_days):
                vol_shock = np.random.normal(0, mc_vol_shock_intensity, simulations)
                mc_curr_volatility = np.abs(mc_curr_volatility + vol_shock)
                mc_curr_volatility = np.minimum(mc_curr_volatility, mc_peak_volatility)
                
                norm_returns = np.random.normal(
                    train_log_returns.mean() - (mc_curr_volatility ** 2) / 2, 
                    mc_curr_volatility / np.sqrt(252), 
                    simulations
                )
                
                mc_simulated_prices[t] = mc_simulated_prices[t - 1] * np.exp(norm_returns)
            
            mc_predicted_price = mc_simulated_prices[-1].mean()
            
            # =============================================================================
            # ARIMA-GARCH PREDICTION
            # =============================================================================
            try:
                # ARIMA model
                arima_model = ARIMA(train_log_returns, order=(5, 0, 2))
                arima_result = arima_model.fit()
                arima_prediction = arima_result.forecast(steps=forecast_days)
                
                # GARCH model
                garch_model = arch_model(train_log_returns*100, mean='Zero', vol='Garch', p=1, q=1)
                garch_result = garch_model.fit(update_freq=5, disp='off')
                
                predicted_log_return = arima_prediction.sum()
                arima_garch_predicted_price = train_starting_price * np.exp(predicted_log_return / 100)
                
            except Exception as e:
                print(f"ARIMA-GARCH failed for {span} days: {e}")
                arima_garch_predicted_price = train_starting_price  # Fallback
            
            # =============================================================================
            # CALCULATE ACCURACY METRICS
            # =============================================================================
            
            # Direction accuracy
            actual_direction = 1 if actual_future_price > train_starting_price else -1
            mc_predicted_direction = 1 if mc_predicted_price > train_starting_price else -1
            ag_predicted_direction = 1 if arima_garch_predicted_price > train_starting_price else -1
            
            mc_direction_correct = (actual_direction == mc_predicted_direction)
            ag_direction_correct = (actual_direction == ag_predicted_direction)
            
            # Percentage error
            mc_percentage_error = abs(mc_predicted_price - actual_future_price) / actual_future_price * 100
            ag_percentage_error = abs(arima_garch_predicted_price - actual_future_price) / actual_future_price * 100
            
            # Store results
            result = {
                'Historical_Days': span,
                'Starting_Price': train_starting_price,
                'Actual_Price': actual_future_price,
                'MC_Predicted': mc_predicted_price,
                'AG_Predicted': arima_garch_predicted_price,
                'MC_Direction_Correct': mc_direction_correct,
                'AG_Direction_Correct': ag_direction_correct,
                'MC_Percentage_Error': mc_percentage_error,
                'AG_Percentage_Error': ag_percentage_error,
                'Actual_Return': (actual_future_price - train_starting_price) / train_starting_price * 100
            }
            results.append(result)
            
            # Print results for this span
            print(f"Historical span: {span} days")
            print(f"Starting price: ${train_starting_price:.2f}")
            print(f"Actual price after {forecast_days} days: ${actual_future_price:.2f}")
            print(f"Monte Carlo predicted: ${mc_predicted_price:.2f}")
            print(f"ARIMA-GARCH predicted: ${arima_garch_predicted_price:.2f}")
            print(f"MC Direction correct: {mc_direction_correct}")
            print(f"AG Direction correct: {ag_direction_correct}")
            print(f"MC Percentage error: {mc_percentage_error:.2f}%")
            print(f"AG Percentage error: {ag_percentage_error:.2f}%")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error processing {span} days span: {e}")
            continue
    
    # =============================================================================
    # SUMMARY STATISTICS
    # =============================================================================
    if results:
        results_df = pd.DataFrame(results)
        
        print("\n" + "="*80)
        print("BACKTESTING SUMMARY")
        print("="*80)
        
        print(f"\nDirection Accuracy:")
        print(f"Monte Carlo: {results_df['MC_Direction_Correct'].mean()*100:.1f}% ({results_df['MC_Direction_Correct'].sum()}/{len(results_df)})")
        print(f"ARIMA-GARCH: {results_df['AG_Direction_Correct'].mean()*100:.1f}% ({results_df['AG_Direction_Correct'].sum()}/{len(results_df)})")
        
        print(f"\nAverage Percentage Error:")
        print(f"Monte Carlo: {results_df['MC_Percentage_Error'].mean():.2f}%")
        print(f"ARIMA-GARCH: {results_df['AG_Percentage_Error'].mean():.2f}%")
        
        print(f"\nBest performing historical span (lowest avg error):")
        best_mc_span = results_df.loc[results_df['MC_Percentage_Error'].idxmin(), 'Historical_Days']
        best_ag_span = results_df.loc[results_df['AG_Percentage_Error'].idxmin(), 'Historical_Days']
        print(f"Monte Carlo: {best_mc_span} days")
        print(f"ARIMA-GARCH: {best_ag_span} days")
        
        # Detailed results table
        print(f"\nDetailed Results:")
        print(results_df.to_string(index=False, float_format='%.2f'))
        
        return results_df
    else:
        print("No successful backtests completed.")
        return None

# Run backtesting
print("\nStarting backtesting analysis...")
backtest_results = backtest_models(
    asset_symbol="GOOGL", 
    base_end_date="2024-01-30",  # This should be your prediction date
    forecast_days=30,  # Change this to match your forecast horizon if needed
    historical_spans=[90, 180, 252, 365, 500, 730]  # Different historical data spans to test
)

# Optional: Plot comparison of methods
if backtest_results is not None and len(backtest_results) > 0:
    plt.figure(figsize=(12, 8))
    
    # Plot 1: Percentage Error Comparison
    plt.subplot(2, 2, 1)
    plt.plot(backtest_results['Historical_Days'], backtest_results['MC_Percentage_Error'], 
             'o-', label='Monte Carlo', linewidth=2)
    plt.plot(backtest_results['Historical_Days'], backtest_results['AG_Percentage_Error'], 
             's-', label='ARIMA-GARCH', linewidth=2)
    plt.xlabel('Historical Data Span (Days)')
    plt.ylabel('Percentage Error (%)')
    plt.title('Prediction Error vs Historical Data Span')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Direction Accuracy
    plt.subplot(2, 2, 2)
    plt.bar(backtest_results['Historical_Days'] - 10, backtest_results['MC_Direction_Correct'].astype(int), 
            width=20, alpha=0.7, label='Monte Carlo')
    plt.bar(backtest_results['Historical_Days'] + 10, backtest_results['AG_Direction_Correct'].astype(int), 
            width=20, alpha=0.7, label='ARIMA-GARCH')
    plt.xlabel('Historical Data Span (Days)')
    plt.ylabel('Direction Correct (1=Yes, 0=No)')
    plt.title('Direction Prediction Accuracy')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Predicted vs Actual Prices
    plt.subplot(2, 2, 3)
    plt.scatter(backtest_results['Actual_Price'], backtest_results['MC_Predicted'], 
               alpha=0.7, label='Monte Carlo')
    plt.scatter(backtest_results['Actual_Price'], backtest_results['AG_Predicted'], 
               alpha=0.7, label='ARIMA-GARCH')
    min_price = min(backtest_results['Actual_Price'].min(), 
                   backtest_results['MC_Predicted'].min(), 
                   backtest_results['AG_Predicted'].min())
    max_price = max(backtest_results['Actual_Price'].max(), 
                   backtest_results['MC_Predicted'].max(), 
                   backtest_results['AG_Predicted'].max())
    plt.plot([min_price, max_price], [min_price, max_price], 'k--', alpha=0.5, label='Perfect Prediction')
    plt.xlabel('Actual Price ($)')
    plt.ylabel('Predicted Price ($)')
    plt.title('Predicted vs Actual Prices')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 4: Model Performance Summary
    plt.subplot(2, 2, 4)
    methods = ['Monte Carlo', 'ARIMA-GARCH']
    direction_accuracy = [backtest_results['MC_Direction_Correct'].mean() * 100,
                         backtest_results['AG_Direction_Correct'].mean() * 100]
    avg_error = [backtest_results['MC_Percentage_Error'].mean(),
                backtest_results['AG_Percentage_Error'].mean()]
    
    x = np.arange(len(methods))
    width = 0.35
    
    plt.bar(x - width/2, direction_accuracy, width, label='Direction Accuracy (%)', alpha=0.7)
    plt.bar(x + width/2, avg_error, width, label='Avg Percentage Error (%)', alpha=0.7)
    
    plt.xlabel('Method')
    plt.ylabel('Performance Metric')
    plt.title('Overall Model Performance')
    plt.xticks(x, methods)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
