import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler


file_name = "dataset.csv"
df = pd.read_csv(file_name)

def clean_data(dataframe):
    # Handle missing values
    dataframe.fillna(dataframe.mean(), inplace=True)
    
    # Remove duplicates
    dataframe.drop_duplicates(inplace=True)

def normalize_data(dataframe, columns):
    scaler = MinMaxScaler()
    dataframe[columns] = scaler.fit_transform(dataframe[columns])

def feature_engineering(dataframe):
    # Create a new feature: price_range
    dataframe['price_range'] = dataframe['high'] - dataframe['low']
    
    # Create a new feature: daily_return
    dataframe['daily_return'] = dataframe.groupby('company')['close'].pct_change()

def aggregate_data(dataframe):
    aggregation_functions = {
        'volume': 'mean',
        'price_range': 'mean',
        'daily_return': 'mean',
        'high': 'max',
        'low': 'min'
    }
    aggregated_dataframe = dataframe.groupby('company').agg(aggregation_functions)
    return aggregated_dataframe

def summarize_data(aggregated_dataframe):
    print("Aggregated Data Summary")
    print(aggregated_dataframe.describe())

# Apply custom functions to the dataset
clean_data(df)
normalize_data(df, ['volume', 'high', 'low', 'close', 'open'])
feature_engineering(df)

# Aggregate and summarize the data
aggregated_df = aggregate_data(df)
summarize_data(aggregated_df)

# Connect to the SQLite database
conn = sqlite3.connect("stock_data_mart.db")

# Create a table for the data mart
df.to_sql("stock_data", conn, if_exists="replace", index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()
