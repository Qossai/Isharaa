import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

class VIXAnalysisApp:
    # ... [rest of your class code] ...

    def calculate_ratio_percentile(self):
        # Fetch historical data for VIX9D and VIX
        vix9d_data = yf.download('^VIX9D', start='2010-01-01', interval='1mo')
        vix_data = yf.download('^VIX', start='2010-01-01', interval='1mo')

        # Calculate historical VIX9D/VIX ratios
        historical_ratios = (vix9d_data['Close'] / vix_data['Close']).dropna()

        # Fetch current prices
        current_prices = self.fetch_data()
        current_ratio = current_prices['VIX9D'] / current_prices['VIX']

        # Explicitly calculate the percentile
        percentile = sum(historical_ratios < current_ratio) / len(historical_ratios) * 100

        # Normalize the percentile to a 1-5 scale
        normalized_percentile = 1 + (percentile / 100) * 4  # Adjusted normalization formula
        return normalized_percentile

    # ... [rest of your Streamlit app code] ...

if __name__ == "__main__":
    app = VIXAnalysisApp()
    app.run_streamlit_app()
