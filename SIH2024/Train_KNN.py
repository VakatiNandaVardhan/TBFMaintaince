import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Seaborn for heatmap
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import joblib

# Load the CSV file
ds = pd.read_csv("DATSET.csv")

# Features (X) and Target (y)
X = ds[["rpm", "temperature", "humidity", "gasdiff"]]
y = ds['status']

# Update label mapping
label_mapping = {
    'normal': 0,
    'error with rpm': 1,
    'error with temp': 2,
    'error with humidity': 3,
    'error with gasdiff': 4
}
y = y.map(label_mapping)

# Apply scaling only to the feature columns
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize the KNN classifier
knn = KNeighborsClassifier(weights="uniform", n_neighbors=5)

# Train the model
model = knn.fit(X_train, y_train)

# Make predictions on the test set
pred = model.predict(X_test)

# Calculate accuracy
acc = accuracy_score(y_test, pred)
print("Accuracy:", acc)

# Generate and display the confusion matrix
conf_matrix = confusion_matrix(y_test, pred)
print("Confusion Matrix:\n", conf_matrix)

# Plot heatmap of confusion matrix
plt.figure(figsize=(8,6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="coolwarm", xticklabels=label_mapping.keys(), yticklabels=label_mapping.keys())
plt.title("Confusion Matrix Heatmap")
plt.ylabel('Actual Label')
plt.xlabel('Predicted Label')
plt.show()

# Generate and display the classification report
class_report = classification_report(y_test, pred, target_names=label_mapping.keys())
print("Classification Report:\n", class_report)

# Save the model and scaling factors to a file
joblib.dump({'scaler': scaler, 'model': model}, "secret.pkl")
