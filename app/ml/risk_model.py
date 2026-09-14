import pandas as pd 

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


df = pd.read_csv("app/ml/data/underwriting_data.csv")

x = df.drop("loan_status", axis=1)
y = df["loan_status"]


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(x_train, y_train)

prediction = model.predict(x_test)
print("Predictions:", prediction)

risk_score = model.predict_proba(x_test)[:, 1]

print(risk_score)