from bs4 import BeautifulSoup
import json
import requests

baseurl = "https://ordinals.com/content/"
stroke_styles = {
	"s": "Square",
	"c": "Circle",
	"i": "Lemniscate",
	"f": "Flora",
	"b": "Butterfly"
}
collection_me = []

def fetch_webpage(url):
	r = requests.get(url)
	return r.text

def extract_json_trait(html_content):
	soup = BeautifulSoup(html_content, "html.parser")
	script = soup.find("script", id="p")
	script_text = script.string
	params_json = script_text.replace("let p=", "")
	params = json.loads(params_json)
	trait = [
		{
			"trait_type": "Ideographic Family",
			"value": params["if"]
		},
		{
			"trait_type": "Initial Stroke Style",
			"value": stroke_styles[params["iss"]],
		},
		{
			"trait_type": "Steps",
			"value": str(params["steps"])
		},
		{
			"trait_type": "Color",
			"value": params["color"]
		}
	]
	return trait

with open('collection.json', 'r') as collection_file:
	collection = json.load(collection_file)

startindex = 1957

for item in collection[startindex:]:
	item_url = baseurl+item["id"]
	html_string = fetch_webpage(item_url)
	trait = extract_json_trait(html_string)
	new_item = item
	new_item["meta"]["attributes"] = trait
	collection_me.append(new_item)
	print(item["meta"]["name"], "completed")

with open("collection_me.json", "w") as collection_file:
	json.dump(collection_me, collection_file, indent=2)
	print("Wrote to file.")