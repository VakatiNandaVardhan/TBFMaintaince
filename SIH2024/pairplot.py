import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load the data
datas = pd.read_csv("DATSET.csv")

# Select features (X) and target (y)
X = datas[["rpm","temperature", "humidity", "gasdiff"]]
y = datas["status"]

# Pairplot without scaling
sns.pairplot(datas, vars=["rpm","temperature", "humidity", "gasdiff"], hue="status")
plt.title("Pairplot without Scaling")
plt.show()

# Apply scaling using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
scaled_data = pd.DataFrame(X_scaled, columns=["rpm","temperature", "humidity", "gasdiff"])
scaled_data["status"] = y  # Add the 'status' column back

# Pairplot after scaling
sns.pairplot(scaled_data, vars=["rpm","temperature", "humidity", "gasdiff"], hue="status")
plt.title("Pairplot with Scaling")
plt.show()
