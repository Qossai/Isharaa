import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

class VIXAnalysisApp:
    def __init__(self):
        # Update symbols with caret (^) prefix
        self.symbols = ["^VIX9D", "^VIX", "^VIX3M", "^VIX6M"]

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
        st.title("Al-Ishara")  # Change page title to "Al-Ishara" and centralize it

        prices = self.fetch_data()
        color = self.analyze_data(prices)

        # Define background color based on the analysis result
        background_color = {"Green": "green", "Yellow": "yellow", "Red": "red"}

        # Define text style for the colored result
        text_style = "font-size: 24px; font-weight: bold; color: black;"

        # Display the result with colored background, larger text, and bold
        if color in background_color:
            st.markdown(f"<div style='background-color: {background_color[color]}; padding: 10px; border-radius: 5px;'><p style='{text_style}'>{color}</p></div>", unsafe_allow_html=True)
        else:
            st.write(f"Condition Result: {color}")

        # Create a nice table for prices without indexes
        st.write("Prices:")
        price_table = [(key[1:], prices[key]) for key in prices if key != "^SVIX"]  # Remove "^SVIX" from visualization and "^" from symbol names
        st.table(price_table)

        # Visualization
        fig, ax = plt.subplots()
        ax.bar([key[1:] for key in prices if key != "^SVIX"], [prices[key] for key in prices if key != "^SVIX"])  # Remove "^" from symbol names
        ax.set_ylabel('Prices')
        ax.set_title('VIX Prices Visualization')

        st.pyplot(fig)

if __name__ == "__main__":
    app = VIXAnalysisApp()
    app.run_streamlit_app()
