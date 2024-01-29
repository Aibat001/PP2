import json

with open('sample-data.json') as f:
    data = json.load(f)

header = "Interface Status\n" + "=" * 80 + "\n"
header += "{:<50}{:<25}{:<12}{}\n".format("DN", "Description", "Speed", "MTU")
header += "-" * 80 + "\n"

body = ""
for interface in data["data"]:
    body += "{:<50}{:<25}{:<12}{}\n".format(interface["DN"], interface["Description"], interface["Speed"],
                                           interface["MTU"])

print(header + body)