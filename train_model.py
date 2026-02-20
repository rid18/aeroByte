import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import pickle

df = pd.read_csv("data/delhi_aqi.csv")
df['lag_1'] = df['AQI'].shift(1)
df['lag_2'] = df['AQI'].shift(2)
df['lag_3'] = df['AQI'].shift(3)

df = df.dropna()

X = df[['lag_1', 'lag_2', 'lag_3']]
y = df['AQI']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

model = XGBRegressor()
model.fit(X_train, y_train)

pickle.dump(model, open("model/aqi_model.pkl", "wb"))

print("Model trained and saved successfully.")
