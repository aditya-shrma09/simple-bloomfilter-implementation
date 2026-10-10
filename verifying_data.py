import pandas as pd

ip_data = pd.read_csv("ip__bf_data.csv")

print("Total IP records:", len(ip_data))
print("Unique IP addresses:", ip_data["Source IP"].nunique())
print("Missing IPs:", ip_data["Source IP"].isna().sum())
print("\nSample IPs:")
print(ip_data.head())