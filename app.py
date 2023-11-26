import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Function to load CPI data from CSV
def load_cpi_data(file_path):
    cpi_data = pd.read_csv(file_path)
    cpi_data['Date'] = pd.to_datetime(cpi_data['Date'])
    return cpi_data

# Function to load stock data from Excel
def load_stock_data(file_path):
    stock_data = pd.read_excel(file_path)
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    return stock_data

# Function to fetch monthly CPI data for a given date range
def fetch_monthly_cpi_data(cpi_data, start_date, end_date):
    mask = (cpi_data['Date'] >= start_date) & (cpi_data['Date'] <= end_date)
    return cpi_data.loc[mask]

# Function to fetch daily stock data for a given date range
def fetch_daily_stock_data(stock_data, start_date, end_date):
    mask = (stock_data['Date'] >= start_date) & (stock_data['Date'] <= end_date)
    return stock_data.loc[mask]

# Function to calculate correlation between inflation and stock close price
def calculate_correlation(inflation_data, stock_data):
    merged_data = pd.merge(inflation_data, stock_data, on='Date', how='inner')
    correlation = merged_data['Inflation'].corr(merged_data['Close'])
    return correlation

# Function to plot and save the correlation and percentage change graph
def plot_correlation_percentage_change_graph(inflation_data, stock_data):
    merged_data = pd.merge(inflation_data, stock_data, on='Date', how='inner')

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plotting stock close price
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Close Price', color=color)
    ax1.plot(merged_data['Date'], merged_data['Close'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Creating a secondary y-axis to plot inflation
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Inflation', color=color)
    ax2.plot(merged_data['Date'], merged_data['Inflation'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Stock Close Price and Inflation Correlation')

    return plt

# Function to save correlation result to a text file
def save_correlation_result(correlation, save_path):
    with open(save_path, 'w') as file:
        file.write(f'Correlation between Inflation and Stock Close Price: {correlation}')

# Streamlit app
def main():
    st.title("Stock and Inflation Correlation App")

    # File paths
    cpi_file_path = 'CPI.csv'
    stock_folder_path = 'Stock_Data/'

    # Load data
    cpi_data = load_cpi_data(cpi_file_path)

    # User input
    stock_symbols = st.selectbox("Select stock symbol:", sorted(st.file_uploader("Choose a stock file", type=['xlsx']).name))
    start_date_str = st.date_input("Select start date:")
    end_date_str = st.date_input("Select end date:")

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Load stock data
    stock_data = load_stock_data(stock_symbols)

    # Fetch monthly CPI data
    monthly_cpi_data = fetch_monthly_cpi_data(cpi_data, start_date, end_date)

    # Fetch daily stock data
    daily_stock_data = fetch_daily_stock_data(stock_data, start_date, end_date)

    # Calculate correlation
    correlation = calculate_correlation(monthly_cpi_data, daily_stock_data)

    # Print and save correlation result
    st.write(f'Correlation between Inflation and Stock Close Price: {correlation}')
    save_path = f'{stock_symbols}_correlation_result.txt'
    save_correlation_result(correlation, save_path)

    # Plot and display correlation graph
    st.pyplot(plot_correlation_percentage_change_graph(monthly_cpi_data, daily_stock_data).gcf())

if __name__ == "__main__":
    main()
