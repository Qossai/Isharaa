import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

class VIXAnalysisApp:
    def __init__(self):
        self.symbols = ["^VIX9D", "^VIX", "^VIX3M", "^VIX6M"]

    def fetch_data(self):
        prices = {}
        for symbol in self.symbols:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                price = round(data['Close'].iloc[-1], 2)
                prices[symbol[1:]] = price  # Remove '^' from symbol for display
            else:
                print(f"{symbol}: No data found")
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

        # Calculate ratios
        prices['VIX9D/VIX Ratio'] = round(prices['VIX9D'] / prices['VIX'], 2) if prices['VIX'] != 0 else float('inf')
        prices['VIX/VIX3M Ratio'] = round(prices['VIX'] / prices['VIX3M'], 2) if prices['VIX3M'] != 0 else float('inf')

        # Create a DataFrame for prices including the new ratios
        st.write("Prices:")
        price_df = pd.DataFrame([prices])
        st.table(price_df.T)  # Transpose for better display

        # Visualization
        fig, ax = plt.subplots()
        ax.bar(prices.keys(), prices.values())
        ax.set_ylabel('Prices and Ratios')
        ax.set_title('VIX Prices and Ratios Visualization')

        st.pyplot(fig)

if __name__ == "__main__":
    app = VIXAnalysisApp()
    app.run_streamlit_app()
