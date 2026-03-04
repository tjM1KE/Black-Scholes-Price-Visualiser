# Black–Scholes Profit & Loss Heatmap Model

[Black-Scholes Pricing App](https://black-scholes-by-mike.streamlit.app/)

A quantitative finance tool that evaluates option pricing and visualizes **profit & loss (P&L)** across different market scenarios using the **Black–Scholes model**. The project generates **heatmaps for call and put P&L** and computes the corresponding **Greeks** for a given set of option parameters.

The goal is to provide an intuitive way to understand how option positions behave as **underlying price and time to maturity change**.

---

## Features

* **Black–Scholes pricing engine**

  * Computes theoretical prices for European **call and put options**
* **Profit & Loss visualization**

  * Heatmaps showing option P&L across a range of underlying prices and time values
* **Greeks calculation**

  * Delta
  * Gamma
  * Theta
  * Vega
  * Rho
* **Scenario analysis**

  * Evaluate sensitivity to changes in:
  * underlying price
  * volatility
  * time to expiration
  * interest rates
* **Visual analytics**

  * Heatmaps help quickly identify profitable and risky regions for option positions

---

## Model Overview

The model uses the **Black–Scholes–Merton framework** to price European options.

Key assumptions include:

* Log-normally distributed underlying prices
* Constant volatility
* Constant risk-free interest rate
* No dividends (unless explicitly modeled)
* European exercise (only at expiration)

The pricing equations are used to compute both **option value** and **Greeks**, which quantify sensitivities to market variables.

---

## Inputs

The model accepts the following parameters:

| Parameter   | Description                    |
| ----------- | ------------------------------ |
| S           | Current underlying asset price |
| K           | Option strike price            |
| T           | Time to maturity (years)       |
| r           | Risk-free interest rate        |
| σ           | Implied volatility             |
| option_type | Call or Put                    |
| option_price| Current option Price           |


These inputs are used to generate **P&L surfaces** across ranges of:

* underlying prices
* time to expiration

---

## Outputs

The model produces:

* **Call option P&L heatmap**
* **Put option P&L heatmap**
* **Greek values**

  * Delta
  * Gamma
  * Theta
  * Vega
  * Rho

These outputs help analyze **risk exposure and profitability under different market conditions**.

---

## Example Use Case

This tool is useful for:

* Understanding **option payoff profiles**
* Visualizing **risk exposure across price/time scenarios**
* Educational demonstrations of **option Greeks**
* Rapid **scenario analysis** for trading strategies

---

## Project Structure

```
project/
│
├─ .streamlit
├─ BlackScholes.py
├─ requirements.txt
├─ streamlit_app.py
└─ README.md
```

*(Structure may vary depending on implementation.)*

---

## Future Improvements

* Support for extraction of data into a database

---

