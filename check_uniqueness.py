from bs4 import BeautifulSoup
import json
import requests
import hashlib

baseurl = "https://ordinals.com/content/"
hashlist = []

def fetch_webpage(url):
	r = requests.get(url)
	return r.text

def extract_json_trait(html_content):
	soup = BeautifulSoup(html_content, "html.parser")
	script = soup.find("script", id="p")
	script_text = script.string
	params_json = script_text.replace("let p=", "")
	return params_json

def are_unique(lst):
	return len(lst) == len(set(lst))

with open('collection.json', 'r') as collection_file:
	collection = json.load(collection_file)

for item in collection:
	item_url = baseurl+item["id"]
	html_string = fetch_webpage(item_url)
	params_json = extract_json_trait(html_string)
	hashlist.append(params_json)
	print(item)

print(hashlist)
print(are_unique(hashlist))