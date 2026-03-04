import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from numpy import log, sqrt, exp
import matplotlib.pyplot as plt
import seaborn as sns

#######################
# Page configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")


# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #90ee90; /* Light green background */
    color: black; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 10px; /* Rounded corners */
}

.metric-put {
    background-color: #ffcccb; /* Light red background */
    color: black; /* Black font color */
    border-radius: 10px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
}

</style>
""", unsafe_allow_html=True)

# (Include the BlackScholes class definition here)

class BlackScholes:
    def __init__(
        self,
        time_to_maturity: float,
        strike: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
        t0_option_price: float,
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate
        self.t0_option_price = t0_option_price

    def calculate_prices(
        self,
    ):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate
        t0_option_price = self.t0_option_price

        d_pos = (
            (
                1/(volatility * sqrt(time_to_maturity))
        )*(
            log(current_price / strike) + (interest_rate + (0.5 * volatility ** 2)) * time_to_maturity
        )
        )

        #d2
        d_neg = (
            d_pos - (sqrt(time_to_maturity) * volatility)
        )

        call_price = (
            current_price * norm.cdf(d_pos) - (
                strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(d_neg)
            )
        )

        put_price = (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(-d_neg)
        )- current_price * norm.cdf( -d_pos)

        self.call_price = call_price
        self.put_price = put_price

        #PROFIT AND LOSS

        call_pnl =(
            t0_option_price - call_price
        )

        put_pnl = (
            put_price - t0_option_price
        )

        self.call_pnl = call_pnl
        self.put_pnl = put_pnl


        #THE GREEKS

        #DELTA
        self.call_delta = norm.cdf(d_pos)
        self.put_delta = norm.cdf(d_pos) - 1

        #GAMMA
        self.call_gamma = norm.pdf(d_pos) / (
            current_price * volatility * sqrt(time_to_maturity)
        )
        self.put_gamma = self.call_gamma

        #VEGA
        self.call_vega = current_price * norm.pdf(d_pos) * sqrt(time_to_maturity)
        self.put_vega = self.call_vega

        #THETA
        self.call_theta = (
            -(current_price * norm.pdf(d_pos) * volatility) / (2 * sqrt(time_to_maturity))
            - interest_rate * strike * exp(-interest_rate * time_to_maturity) * norm.cdf(d_neg)
            )
        
        self.put_theta = (
            -(current_price * norm.pdf(d_pos) * volatility) / (2 * sqrt(time_to_maturity)) 
            + interest_rate * strike * exp(-interest_rate * time_to_maturity) * norm.cdf(-d_neg)
            )

        #RHO
        self.call_rho = strike * time_to_maturity * exp(-(interest_rate * time_to_maturity))*norm.cdf(d_neg)
        self.put_rho = -(strike * time_to_maturity * exp(-(interest_rate * time_to_maturity)) * norm.cdf(-d_neg))

        return call_price, put_price, call_pnl, put_pnl

# Function to generate heatmaps
# ... your existing imports and BlackScholes class definition ...


# Sidebar for User Inputs
with st.sidebar:
    st.title("📊 Black-Scholes Model Visualiser")
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/michail-khasaev/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Michail Khasaev`</a>', unsafe_allow_html=True)

    current_price = st.number_input("Current Asset Price", value=100.0)
    strike = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)
    t0_option_price = st.number_input("Current Option Price", value= 8)

    st.markdown("---")
    calculate_btn = st.button('Heatmap Parameters')
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)
    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)



def plot_heatmap(bs_model, spot_range, vol_range, strike):
    call_pnls = np.zeros((len(vol_range), len(spot_range)))
    put_pnls = np.zeros((len(vol_range), len(spot_range)))
    
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time_to_maturity=bs_model.time_to_maturity,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=bs_model.interest_rate,
                t0_option_price = t0_option_price
            )
            bs_temp.calculate_prices()
            call_pnls[i, j] = bs_temp.call_pnl
            put_pnls[i, j] = bs_temp.put_pnl

    # Plotting Call Price Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_pnls, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn",center = 0, ax=ax_call)
    ax_call.set_title('CALL')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')
    
    # Plotting Put Price Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_pnls, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn",center = 0, ax=ax_put)
    ax_put.set_title('PUT')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')
    
    return fig_call, fig_put


# Main Page for Output Display
st.title("Black-Scholes Pricing Model")

# Table of Inputs
input_data = {
    "Current Asset Price": [current_price],
    "Strike Price": [strike],
    "Time to Maturity (Years)": [time_to_maturity],
    "Volatility (σ)": [volatility],
    "Risk-Free Interest Rate": [interest_rate],
    "Current Option Price": [t0_option_price],
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

# Calculate Call and Put values
bs_model = BlackScholes(time_to_maturity, strike, current_price, volatility, interest_rate, t0_option_price)
call_price, put_price, call_pnl, put_pnl = bs_model.calculate_prices()

#Greeks Dashboard
st.title("Option Greeks Dashboard")

st.subheader("Call Greeks")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Delta Δ", f"{bs_model.call_delta:.4f}")
c2.metric("Gamma Γ", f"{bs_model.call_gamma:.4f}")
c3.metric("Theta Θ", f"{bs_model.call_theta:.4f}")
c4.metric("Vega ν", f"{bs_model.call_vega:.4f}")
c5.metric("Rho ρ", f"{bs_model.call_rho:.4f}")

st.subheader("Put Greeks")

p1, p2, p3, p4, p5 = st.columns(5)

p1.metric("Delta Δ", f"{bs_model.put_delta:.4f}")
p2.metric("Gamma Γ", f"{bs_model.put_gamma:.4f}")
p3.metric("Theta Θ", f"{bs_model.put_theta:.4f}")
p4.metric("Vega ν", f"{bs_model.put_vega:.4f}")
p5.metric("Rho ρ", f"{bs_model.put_rho:.4f}")

# Display Call and Put Values in colored tables
col1, col2, col3, col4= st.columns(4)

with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL P&L</div>
                <div class="metric-value">${call_pnl:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT P&L</div>
                <div class="metric-value">${put_pnl:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.title("Options P&L - Interactive Heatmap")
st.info("Explore how option profit and losses fluctuate with varying 'Spot Prices and Volatility' levels using interactive heatmap parameters, all while maintaining a constant 'Strike Price' and 'Current Option Price'. Greeks measure how option prices respond to changes in market variables such as price, volatility, time and interest rates.")

# Interactive Sliders and Heatmaps for Call and Put Options
col1, col2 = st.columns([1,1], gap="small")

with col1:
    st.subheader("Call P&L Heatmap")
    heatmap_fig_call, _ = plot_heatmap(bs_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_call)

with col2:
    st.subheader("Put P&L Heatmap")
    _, heatmap_fig_put = plot_heatmap(bs_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_put)



