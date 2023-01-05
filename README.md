# Dunn Family Recipe Book

## Project Structure
```
eml/
	*.eml              # downloaded emails from ios app
img/
	*.jpg              # all recipe images
json/
	family/*.json      # family recipes in schema.org JSON format
	ios_app/*.json     # ios app recipes in schema.org JSON format
src/
	eml_to_json.py     # helper script for converting email recipes to JSON
	generate_tex.py    # generate recipe TeX file from JSON recipes
tex/
	recipes.tex        # TeX source for recipe book
	recipes.pdf        # final PDF of recipe book
```

## RecipeSage Recipe App
https://recipesage.com/#/list/main

#### Recipe Format
https://developers.google.com/search/docs/appearance/structured-data/recipe
https://schema.org/Recipe

#### Questions for Mom
Coconut Shrimp: 1 cup coconut, 1 cup breadcrumbs, or 2 cups coconut?
Second Chicken Cordon Bleu?
Pizza/Mozzerella Bites?
