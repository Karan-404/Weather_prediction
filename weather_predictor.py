#weather_predictor
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import sys

def load_data(sample_weather.txt):
    dates = []
    temps = []

    with open(sample_weather.txt, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            try:
                date = datetime.strptime(parts[0], "%Y%m%d")
                temp = float(parts[1])
                dates.append(date)
                temps.append(temp)
            except:
                continue

    df = pd.DataFrame({"date": dates, "temp": temps})
    df = df.sort_values("date")
    df["days"] = (df["date"] - df["date"].min()).dt.days
    return df

def build_model():
    model = keras.Sequential([
        keras.layers.Dense(32, activation='relu', input_shape=(1,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def predict_future(model, scaler, last_day, n=7):
    future_days = np.array([last_day + i for i in range(1, n + 1)]).reshape(-1, 1)
    scaled_days = scaler.transform(future_days)
    preds = model.predict(scaled_days).flatten()
    start_date = datetime.strptime("20060201", "%Y%m%d")  # adjust as per your dataset
    dates = [start_date + timedelta(days=int(d)) for d in future_days.flatten()]
    return list(zip([d.strftime("%Y-%m-%d") for d in dates], preds))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 weather_nn_predictor.py daily_avg_temp.txt")
        sys.exit(1)

    df = load_data(sys.argv[1])
    X = df["days"].values.reshape(-1, 1)
    y = df["temp"].values

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    model = build_model()
    model.fit(X_scaled, y, epochs=200, verbose=0)

    last_day = df["days"].max()
    future = predict_future(model, scaler, last_day)

    print("\nPredicted Temperatures (Neural Network):")
    for date, temp in future:
        print(f"{date} -> {round(temp, 2)} °F")
