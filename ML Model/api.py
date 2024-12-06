from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Initialize the Flask application
app = Flask(__name__)

# Load the dataset
file_path = 'Dataset/Crop_recommendation.csv'
df = pd.read_csv(file_path)

# Prepare data (same as your original script)
X = df.drop(columns=['label'])  
y = df['label']                 
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train the model (same as your original script)
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train, y_train)

# Save the trained model to a file for future use
with open('rf_model.pkl', 'wb') as f:
    pickle.dump(rf_clf, f)
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

# Load model and label encoder function (for inference)
def load_model():
    with open('rf_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('label_encoder.pkl', 'rb') as le_file:
        encoder = pickle.load(le_file)
    return model, encoder

# Create an endpoint to handle predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the request
    data = request.get_json()  # Expecting data in JSON format
    
    # Extract features (assuming data contains feature values for prediction)
    features = np.array([data['features']])
    print(features)
    
    # Load model
    model, encoder = load_model()
    
    # Predict using the model
    prediction = model.predict(features)
    
    # Decode prediction to original label
    predicted_label = encoder.inverse_transform(prediction)
    print(predicted_label)
    # Return the prediction in JSON format
    return jsonify({'prediction': predicted_label[0]})

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)