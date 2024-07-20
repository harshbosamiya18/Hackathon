import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('ecommerce_sales_analysis.csv')

features = ['category', 'price','review_score', 'sales_month_12']
target = 'review_count'

X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test) 

import xgboost as xgb
from sklearn.metrics import mean_squared_error

model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=5)

model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict_price', methods=['POST'])
def predict_price():
    data = request.json
    input_features = [data['price'], data['competitor_price'], data['seasonality'], data['marketing_spend']]
    input_scaled = scaler.transform([input_features])
    predicted_demand = model.predict(input_scaled)
    return jsonify({'predicted_demand': predicted_demand[0]})

if __name__ == '__main__':
    app.run(debug=True)