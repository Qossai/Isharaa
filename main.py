import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

class VIXAnalysisApp:
    def __init__(self):
        # Update symbols without caret (^) prefix and remove "SVIX"
        self.symbols = ["VIX9D", "VIX", "VIX3M", "VIX6M"]

    def fetch_data(self):
        prices = {}
        for symbol in self.symbols:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                price = round(data['Close'].iloc[-1], 2)  # Round to 2 decimal places
                prices[symbol] = price
            else:
                print(f"{symbol}: No data found")
        return prices

    def analyze_data(self, prices):
        # Ensure all keys are present in the prices dictionary
        required_keys = ["VIX9D", "VIX", "VIX3M", "VIX6M"]
        if not all(key in prices for key in required_keys):
            return "Data Incomplete"

        vix9d = prices.get("VIX9D", float('inf'))
        vix = prices.get("VIX", float('inf'))
        vix3m = prices.get("VIX3M", float('inf'))
        vix6m = prices.get("VIX6M", float('inf'))

        if vix9d < vix < vix3m < vix6m:
            return "Green: Everything should be OK"
        elif vix9d > vix:
            return "Yellow: It's getting risky"
        elif vix > vix3m:
            return "Red"
        else:
            return "Neutral"

    def run_streamlit_app(self):
        st.title("VIX Analysis")  # Revert to the original title

        prices = self.fetch_data()
        color = self.analyze_data(prices)

        # Define background color based on the analysis result
        background_color = {"Green: Everything should be OK": "green", "Yellow: It's getting risky": "yellow", "Red": "red", "Neutral": "gray"}

        # Define text style for the colored result
        text_style = "font-size: 24px; font-weight: bold; color: black;"

        # Display the result with colored background, larger text, and bold
        if color in background_color:
            st.markdown(f"<div style='background-color: {background_color[color]}; padding: 10px; border-radius: 5px;'><p style='{text_style}'>{color}</p></div>", unsafe_allow_html=True)
        else:
            st.write(color)

        # Create a nice table for prices without indexes
        price_table = [(key, prices[key]) for key in prices if key != "SVIX"]  # Remove "SVIX" from visualization
        st.sidebar.table(price_table)  # Display the table in the left sidebar

        # Visualization
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size
        ax.bar(prices.keys(), [prices[key] for key in prices if key != "SVIX"])
        ax.set_ylabel('Prices')
        ax.set_title('VIX Prices Visualization')

        st.pyplot(fig)

if __name__ == "__main__":
    app = VIXAnalysisApp()
    app.run_streamlit_app()
