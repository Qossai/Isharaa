import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

class VIXAnalysisApp:
    def __init__(self):
        self.symbols = ["^VIX9D", "^VIX", "^VIX3M", "^VIX6M"]

    def fetch_data(self):
        prices = {}
        for symbol in self.symbols:
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="1d")
                if not data.empty:
                    price = round(data['Close'].iloc[-1], 2)
                    prices[symbol[1:]] = price  # Remove '^' from symbol for display
                else:
                    st.error(f"{symbol}: No data found")
            except Exception as e:
                st.error(f"Error fetching data for {symbol}: {e}")
        return prices

    def analyze_data(self, prices):
        required_keys = ["VIX9D", "VIX", "VIX3M", "VIX6M"]
        if not all(key in prices for key in required_keys):
            return "Data Incomplete"

        vix9d = prices.get("VIX9D", float('inf'))
        vix = prices.get("VIX", float('inf'))
        vix3m = prices.get("VIX3M", float('inf'))
        vix6m = prices.get("VIX6M", float('inf'))

        if vix9d < vix < vix3m < vix6m:
            return "Green"
        elif vix9d > vix:
            return "Yellow"
        elif vix > vix3m:
            return "Red"
        else:
            return "Neutral"

    def calculate_ratio_percentile(self):
        vix9d_data = yf.download('^VIX9D', start='2010-01-01', interval='1mo')
        vix_data = yf.download('^VIX', start='2010-01-01', interval='1mo')
        historical_ratios = (vix9d_data['Close'] / vix_data['Close']).dropna()
        current_prices = self.fetch_data()
        current_ratio = current_prices['VIX9D'] / current_prices['VIX']
        percentile = sum(historical_ratios < current_ratio) / len(historical_ratios) * 100
        normalized_percentile = 1 + (percentile / 100) * 4
        return normalized_percentile

    def draw_gauge(self, value, min_val=0, max_val=5):
        # Ensure value is within bounds
        value = max(min(value, max_val), min_val)

        # Create a new figure with a white face color
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw={'aspect': 'auto'}, facecolor='white')

        # Define the angle for each zone based on the value ranges
        green_zone_angle = 180 * 2.5 / max_val
        yellow_zone_angle = 180 * 3.5 / max_val

        # Create the arcs
        arc1 = Wedge(center=(0.5, 0.5), r=0.4, theta1=0, theta2=green_zone_angle, width=0.1, facecolor='green',
                     transform=ax.transAxes)
        arc2 = Wedge(center=(0.5, 0.5), r=0.4, theta1=green_zone_angle, theta2=yellow_zone_angle, width=0.1,
                     facecolor='yellow', transform=ax.transAxes)
        arc3 = Wedge(center=(0.5, 0.5), r=0.4, theta1=yellow_zone_angle, theta2=180, width=0.1, facecolor='red',
                     transform=ax.transAxes)

        # Add arcs to the plot
        for arc in [arc1, arc2, arc3]:
            ax.add_patch(arc)

        # Convert value to angle using interpolation
        angle = np.interp(value, [min_val, max_val], [0, 180])

        # Draw the needle
        needle_x = 0.5 + 0.4 * np.cos(np.radians(180 - angle))
        needle_y = 0.5 + 0.4 * np.sin(np.radians(180 - angle))
        ax.plot([0.5, needle_x], [0.5, needle_y], color='black', lw=2, transform=ax.transAxes)

        # Draw a small circle at the base of the needle
        ax.plot([0.5], [0.5], color='black', marker='o', transform=ax.transAxes)

        # Set the aspect of the plot to be equal
        ax.set_aspect('equal')

        # Remove the axes
        ax.axis('off')

        # Add a text label below the gauge for the value
        ax.text(0.5, 0.1, f'{value:.2f}', horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12, fontweight='bold')

        return fig

    def run_streamlit_app(self):
        st.title("Al-Ishara")
        prices = self.fetch_data()
        color = self.analyze_data(prices)
        background_color = {"Green": "green", "Yellow": "yellow", "Red": "red"}
        text_style = "font-size: 24px; font-weight: bold; color: black;"

        if color in background_color:
            st.markdown(f"<div style='background-color: {background_color[color]}; padding: 10px; border-radius: 5px;'><p style='{text_style}'>{color}</p></div>", unsafe_allow_html=True)
        else:
            st.write(f"Condition Result: {color}")

        prices['VIX9D/VIX Ratio'] = round(prices['VIX9D'] / prices['VIX'], 2) if prices['VIX'] != 0 else float('inf')
        prices['VIX/VIX3M Ratio'] = round(prices['VIX'] / prices['VIX3M'], 2) if prices['VIX3M'] != 0 else float('inf')

        st.write("Prices:")
        price_df = pd.DataFrame([prices])
        st.table(price_df.T)

        fig, ax = plt.subplots()
        ax.bar(prices.keys(), prices.values())
        ax.set_ylabel('Prices and Ratios')
        ax.set_title('VIX Prices and Ratios Visualization')
        st.pyplot(fig)

        normalized_percentile = self.calculate_ratio_percentile()
        st.write(f"Normalized VIX9D/VIX Ratio Percentile: {normalized_percentile:.2f} (1: Safest, 5: Riskiest)")
        gauge_fig = self.draw_gauge(normalized_percentile)
        st.pyplot(gauge_fig)

# This line should be completely unindented and outside the class definition
if __name__ == "__main__":
    app = VIXAnalysisApp()
    app.run_streamlit_app()
