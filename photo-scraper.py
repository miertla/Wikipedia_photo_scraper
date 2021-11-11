from flask import Flask, json, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import urllib
import regex as re
import requests

app = Flask(__name__)

# referenced: https://www.dataskunkworks.com/

#prevents the raising of restrictions due to CORS 
CORS(app) 

def get_wikipedia_image(ingredient):
	ingredient_url = []
	urlpage = 'https://en.wikipedia.org/wiki/' + ingredient
	# query website and return html
	page = requests.get(urlpage).text
	# parse html using beautiful soup
	parsed_html = BeautifulSoup(page, 'html.parser')
	for raw_img in parsed_html.find_all('img'):
		link = raw_img.get('src')
	# first image on the page with the URL structure below is usually the image inside the infobox. 
	# Excluded any .svg images as they're vector graphics common to all wikipedia pages
	if re.search('wikipedia/.*/thumb/', link) and not re.search('.svg', link):
		ingredient_url = [ingredient, link]
		# break out of the loop once the first image has been found
		break
	return ingredient_url

@app.route('/wikipediaImageScraper/<string:ingredient>', methods=['Get'])
def wikipediaImageScraper(ingredient: str):
	response = get_wikipedia_image(ingredient)
	return jsonify(response) 

if __name__ == '__main__':
	app.run()
