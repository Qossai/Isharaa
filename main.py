import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

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
                prices[symbol] = price
            else:
                print(f"{symbol}: No data found")
        return prices

    def analyze_data(self, prices):
        required_keys = ["^VIX9D", "^VIX", "^VIX3M", "^VIX6M"]
        if not all(key in prices for key in required_keys):
            return "Data Incomplete"

        vix9d = prices.get("^VIX9D", float('inf'))
        vix = prices.get("^VIX", float('inf'))
        vix3m = prices.get("^VIX3M", float('inf'))
        vix6m = prices.get("^VIX6M", float('inf'))

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

        # Calculate ratios and add them to the prices dictionary
        vix9d_vix_ratio = prices["^VIX9D"] / prices["^VIX"] if prices["^VIX"] != 0 else float('inf')
        vix_vix3m_ratio = prices["^VIX"] / prices["^VIX3M"] if prices["^VIX3M"] != 0 else float('inf')
        prices["VIX Ratios"] = f"VIX9D/VIX: {vix9d_vix_ratio:.2f}, VIX/VIX3M: {vix_vix3m_ratio:.2f}"

        # Create a table for prices including the new ratios
        st.write("Prices:")
        price_table = [(key[1:], prices[key]) for key in prices]
        st.table(price_table)

        # Visualization
        fig, ax = plt.subplots()
        ax.bar([key[1:] for key in prices], [prices[key] if isinstance(prices[key], float) else 0 for key in prices])  # Handle non-float value in ratios
        ax.set_ylabel('Prices')
        ax.set_title('VIX Prices Visualization')

        st.pyplot(fig)

if __name__ == "__main__":
    app = VIXAnalysisApp()
    app.run_streamlit_app()
