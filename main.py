import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

class VIXAnalysisApp:
    def __init__(self):
        # Update symbols with caret (^) prefix
        self.symbols = ["^VIX9D", "^VIX", "^VIX3M", "^VIX6M", "SVIX"]

    def fetch_data(self):
        prices = {}
        for symbol in self.symbols:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                price = data['Close'].iloc[-1]
                prices[symbol] = price
            else:
                print(f"{symbol}: No data found")
        return prices

    def analyze_data(self, prices):
        # Ensure all keys are present in the prices dictionary
        required_keys = ["^VIX9D", "^VIX", "^VIX3M", "^VIX6M"]
        if not all(key in prices for key in required_keys):
            return "Data Incomplete"

        if prices.get("^VIX9D", float('inf')) < prices.get("^VIX", float('inf')) < prices.get("^VIX3M", float('inf')) < prices.get("^VIX6M", float('inf')):
            return "Green"
        elif prices.get("^VIX9D", float('inf')) > prices.get("^VIX", 0):
            return "Yellow"
        elif prices.get("^VIX", 0) > prices.get("^VIX3M", float('inf')):
            return "Red"
        else:
            return "Neutral"

    def run_streamlit_app(self):
        st.title("VIX Analysis")

        prices = self.fetch_data()
        color = self.analyze_data(prices)

        st.write("Prices:", prices)
        st.write("Condition Result:", color)

        # Visualization
        fig, ax = plt.subplots()
        ax.bar(prices.keys(), prices.values())
        ax.set_ylabel('Prices')
        ax.set_title('VIX Prices Visualization')

        st.pyplot(fig)

if __name__ == "__main__":
    app = VIXAnalysisApp()
    app.run_streamlit_app()

