import pandas as pd

df = pd.read_csv(
    "C:/Users/Ajay/Downloads/GeneratedLabelledFlows/TrafficLabelling/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
)
df.columns = df.columns.str.strip()
ip_stream = df["Source IP"]

import pandas as pd

df = pd.read_csv(
    r"C:\Users\Ajay\Downloads\GeneratedLabelledFlows\TrafficLabelling\Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
)

df.columns = df.columns.str.strip()

ip_data = df[["Source IP"]]

ip_data.to_csv("ip__bf_data.csv", index=False)

print("IP dataset created!")
print(ip_data.head())