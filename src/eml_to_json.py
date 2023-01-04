import os, json
from bs4 import BeautifulSoup

latex = True
recipe_dir = "/home/tim/Documents/projects/recipes"


def save_recipe(title, author, ingredients, directions, image):

	dictionary = {
		"@context": "https://schema.org",
		"@type": "Recipe",
		"name": title,
		"author": {
			"@type": "Person",
			"name": author
		},
		"description": "description of recipe",
		"recipeCategory": "classic, pies",
		"recipeYield": "yield",
		"recipeIngredient": ingredients,
		"recipeInstructions": [],
	}

	if latex: # else, RecipeSage doesn't accept image like this
		dictionary["image"] = [f"{recipe_dir}/img/{image}"]

	# add directions
	for step in directions:
		dictionary["recipeInstructions"].append( {
			"@type": "HowToStep",
			"text": step
		})

	# save results
	with open(f"../json/{title}.json", 'w') as outfile:
		outfile.write(json.dumps(dictionary, indent=4))


eml_dir = "../input"
for eml_fn in os.listdir(eml_dir):
	with open(f"{eml_dir}/{eml_fn}") as f:

		# use only HTML from email
		data = f.read().replace("=\n","").replace("  ", " ").replace("  ", " ") \
				.replace("=C2=B0", "").replace("=C3=B1","n").replace("=C3=A9","e") \
				.replace("=20","").replace("=C2=AE","").replace("=C2=BA","") \
				.replace("=C2=BC","1/4").replace("=C2=BD", "1/2") \
				.replace("=C2=BD","3/4").replace("=E2=80=99","") \
				.replace("=E2=80=94", "-").replace("=C3=97","x")
		start = data.find("<html>")
		end = data.find("</html>")
		data = data[start:end+7]

		# extract HTML
		soup = BeautifulSoup(data, "html5lib")
		html = list(soup.children)[0]
		# print(soup.prettify())

		# get title
		title = [title.getText() for title in html.select("body div b u center")][0]
		if title.find("Website Link") > 0:
			title = title[:-15]

		body = [content.getText() for content in html.select("body div")][0]
		author_str = "I got this recipe from "
		ingredients_str = "Ingredients"
		author = body[body.find(author_str)+len(author_str):
				body.find(ingredients_str)]
		print(f"\n\n{title}: '{author}'")

		# ingredients
		ingredients = []
		try:
			ingrs = html.select("body div ul li")
			ingredients = [ingr.getText() for ingr in ingrs]
		except:
			pass
		print(ingredients)

		# directions
		directions = []
		try:
			dirs = html.select("body div ol")[0]
			directions = [step.getText() for step in dirs.children]
		except:
			pass
		print(directions)

		# image
		image = ""
		try:
			image = html.select("img")[0]['alt'][3:-1]
		except:
			pass
		print(image)

		save_recipe(title, author, ingredients, directions, image)

