import json


with open("sample-data.json", "r") as file:
    data = json.loads(file.read())

# Header
print(f"{'Interface Status':^88}\n{'='*88}\n{'DN':<50} {'Description':<20} {'Speed':<9} {'MTU':<6}")
print(f"{'-'*50} {'-'*20} {'-'*9} {'-'*6}")

for attr in data["imdata"]:
    attr = attr["l1PhysIf"]["attributes"]
    print(f"{attr['dn']:<50} {attr['descr']:<20} {attr['speed']:<9} {attr['mtu']:<6}")