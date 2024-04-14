import requests
import argparse
import json

def fetch_children(parent, page=0):
	try:
		r = requests.get(f"https://ordinals.com/r/children/{parent}/{page}")
		if (not r.ok):
			raise Exception(f"HTTP Request returned error: {r.status_code}")
		return r.json()
	except Exception as e:
		print("An error occured.", e)

def add_to_collection(collection, ids, name):
	# default name template: "NAME #INDEX"

	for id in ids:
		collection.append({
			"id": id,
			"meta": {
				"name": f"{name} #{len(collection)}"
			}
		})
	
	return collection

def main():
	parser = argparse.ArgumentParser(description="Parent/child utility")

	parser.add_argument('parent', type=str, help="Parent inscription ID")
	parser.add_argument('--output', type=str, help="Output file path. Default to collection.json")
	parser.add_argument('--name', type=str, help="Collection item name.", required=True)

	args = parser.parse_args()

	output = "collection.json" if not args.output else args.output
	name = args.name

	collection = []

	# First request

	children = fetch_children(args.parent)

	collection = add_to_collection(collection, children['ids'], name)

	more = children['more']
	page = children['page']

	while more:
		children = fetch_children(args.parent, page+1)
		collection = add_to_collection(collection, children['ids'], name)
		more = children['more']
		page = children['page']
		print("Page", page)
	
	# Save to JSON
	with open(output, 'w') as collection_json:
		json.dump(collection, collection_json, indent=2)


if __name__ == "__main__":
	main()