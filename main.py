import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

class VIXAnalysisApp:
    # ... [rest of your class code remains the same]

    def draw_gauge(self, value):
        fig, ax = plt.subplots()

        # Define the gauge sectors
        wedges = [
            Wedge(center=(0, 0), r=1, theta1=0, theta2=180, color='green'),
            Wedge(center=(0, 0), r=1, theta1=180, theta2=252, color='yellow'),
            Wedge(center=(0, 0), r=1, theta1=252, theta2=360, color='red')
        ]

        for w in wedges:
            ax.add_patch(w)

        # Convert the value to an angle
        angle = 180 * value / 5

        # Draw the needle
        plt.plot([0, np.cos(np.radians(angle))], [0, np.sin(np.radians(angle))], color='black', lw=2)

        ax.set_xlim(-1, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')  # Turn off the axis

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

        # Display the gauge plot for the normalized percentile
        normalized_percentile = self.calculate_ratio_percentile()
        st.write(f"Normalized VIX9D/VIX Ratio Percentile: {normalized_percentile:.2f} (1: Safest, 5: Riskiest)")
        gauge_fig = self.draw_gauge(normalized_percentile)
        st.pyplot(gauge_fig)

if __name__ == "__main__":
    app = VIXAnalysisApp()
    app.run_streamlit_app()
