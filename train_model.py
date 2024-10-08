import pandas as pd
from sklearn.linear_model import LinearRegression 
import joblib
#load data
data = pd.read_csv('sales_data.csv')

#Prepare the features and target
x = data[['Month', 'Year']]
y = data['Sales']

#Create and train the model
model = LinearRegression()
model.fit(x,y)

#Save the model
joblib.dump(model, 'Sales_forecasting_model.pkl')