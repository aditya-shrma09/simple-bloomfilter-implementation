
import pandas as pd
import time
import ipaddress
import random
import sys
from bloom_filter import BloomFilter

# Load data
df = pd.read_csv("ip__bf_data.csv")
df.columns = df.columns.str.strip()

ips = df["Source IP"].dropna().unique().tolist()

print("Total records:", len(df))
print("Unique IPs:", len(ips))

# Create Bloom Filter
bf = BloomFilter(n=len(ips), p=0.01)

# Insert IPs
start = time.perf_counter()

for ip in ips:
    bf.add(ip)

ins_time = time.perf_counter() - start

print("\nBloom Filter Results")
print("Bit array size:", bf.size, "bits")
print("Hash functions:", bf.hash_count)
print("Memory:", len(bf.bit_array), "bytes")
print("Insertion time:", round(ins_time, 6), "seconds")

# Check false negatives
fn = 0

for ip in ips:
    if not bf.contains(ip):
        fn += 1

print("False negatives:", fn)

# Generate IPs not present in the data
ip_set = set(ips)
rng = random.Random(42)
test_ips = set()

while len(test_ips) < 10000:
    num = rng.randrange(2**32)
    ip = str(ipaddress.IPv4Address(num))

    if ip not in ip_set:
        test_ips.add(ip)

# Test Bloom Filter
fp = 0

start = time.perf_counter()

for ip in test_ips:
    if bf.contains(ip):
        fp += 1

q_time = time.perf_counter() - start
fpr = fp / len(test_ips)

print("\nFalse Positive Test")
print("Test queries:", len(test_ips))
print("False positives:", fp)
print("Measured FPR:", round(fpr * 100, 4), "%")
print("Total query time:", round(q_time, 6), "seconds")
print("Average query time:",
      round(q_time / len(test_ips) * 1000000, 3),
      "microseconds")

# Compare with Python set
start = time.perf_counter()
s = set(ips)
s_time = time.perf_counter() - start

s_mem = sys.getsizeof(s)

for ip in s:
    s_mem += sys.getsizeof(ip)

# Query the set using the same test IPs
start = time.perf_counter()

res = [ip in s for ip in test_ips]

sq_time = time.perf_counter() - start

print("\nBloom Filter vs Python Set")
print("Set build time:", round(s_time, 6), "seconds")
print("Set memory:", s_mem, "bytes")
print("Bloom Filter memory:", len(bf.bit_array), "bytes")
print("Set query time:", round(sq_time, 6), "seconds")
print("Set average query:",
      round(sq_time / len(test_ips) * 1000000, 3),
      "microseconds")
print("Set false positives:", sum(res))
