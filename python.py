import os

target = "extracted_orders.xlsx"
print("Searching for", target, "...")

found = False
# Apne OneDrive documents folder mein search karte hain
search_root = r"C:\Users\arsha\OneDrive\Documents"

for root, dirs, files in os.walk(search_root):
    if target in files:
        print(f"Mil gayi! Full path: {os.path.abspath(os.path.join(root, target))}")
        found = True
        break

if not found:
    print("OneDrive Documents mein nahi mili.")