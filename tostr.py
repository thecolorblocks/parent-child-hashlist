import json

with open('collection_me.json', 'r') as f:
	collection = json.load(f)
	ncollection = []
	for item in collection:
		nitem = item
		nitem["meta"]["attributes"][2]["value"] = str(nitem["meta"]["attributes"][2]["value"])
		ncollection.append(nitem)

with open('collection_me_new.json', 'w') as f:
	json.dump(ncollection, f, indent=2)