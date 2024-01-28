import joblib
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd

file = open(r"ai_data/2022_Q1_OR_Utilization.csv")
text = file.read()
text = text.split()
for i in range(len(text)):
    text[i] = text[i].replace('"',"")

file_path = 'ai_data/2022_Q1_OR_Utilization.csv'
date_columns = ['Date', 'OR Schedule','Wheels In', 'Start Time','End Time','Wheels Out']
data = pd.read_csv(file_path, parse_dates=date_columns)
data['Service'] = data['Service'].astype("string")
data['CPT Description'] = data['CPT Description'].astype("string")
data['Actual_time'] = (data['End Time'] - data['Start Time']).dt.total_seconds().div(60).astype(int)

features = ['CPT Code', 'Booked Time (min)', 'Service', 'CPT Description']
X = data[features]
y = data['Actual_time']
categorical_features = ['Service', 'CPT Description']
X_encoded = X.copy()
label_encoders = {}
for feature in categorical_features:
    le = LabelEncoder()
    X_encoded[feature] = le.fit_transform(X_encoded[feature])
    label_encoders[feature] = le


def export_model(model, filename):
    try:
        joblib.dump(model, filename)
        print(f"Model saved to {filename}")
    except Exception as e:
        print(f"Error saving model: {str(e)}")

def get_actual_time_estimate(input_features, label_encoders, trained_model):
    try:
        input_df = pd.DataFrame(input_features, columns=['CPT Code', 'Booked Time (min)', 'Service', 'CPT Description'])

        for feature, encoder in label_encoders.items():
            input_df[feature] = encoder.transform(input_df[feature])

        estimated_actual_time = trained_model.predict(input_df)

        return estimated_actual_time
    except Exception as e:
        print(f"Error getting actual time estimate: {str(e)}")



model = joblib.load('ai_data/trained_regression_model.joblib')
input_features = [
    [28110, 30, 'Podiatry', 'Lapidus bunionectomy']
]

def predict_time(cpt, est, sector, procedure):
  print(cpt, est, sector, procedure)
  input_feats = [[cpt, est, sector, procedure],]
  print(input_feats)
  print(input_features)
  estimated_times = get_actual_time_estimate(input_feats, label_encoders, model)
  return estimated_times[0]

if __name__ == '__main__':
  estimated_times = get_actual_time_estimate(input_features, label_encoders, model)
  print("Estimated Actual Times:")
  print(estimated_times)

