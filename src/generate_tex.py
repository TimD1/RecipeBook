import os, json
from collections import defaultdict

f = open("../tex/recipes.tex", "w")
json_dir = "../json"
categories = [
		"Appetizers",
		"Salads",
		"Soups",
		"Sides",
		"Breakfasts",
		"Dips",
		"Seafood",
		"Steak",
		"Pork",
		"Chicken",
		"Pastas",
		"Breads",
		"Pies",
		"Cookies",
		"Cakes",
		"Desserts",
		"Classic"
]
directories = [
        # "ios_app",
		"family"
		]


def add_to_toc(recipe, table_of_contents):
	cats = recipe["recipeCategory"].split(", ")
	classic = False
	for cat in cats:
		if cat == "classic":
			classic = True
			continue
		if len(table_of_contents[cat]):
			table_of_contents[cat] += "\n"
		name_id = recipe["name"].lower().replace(" ", "-")
		table_of_contents[cat] += f"{recipe['name']}" + r"\hrulefill\pageref{" + name_id + r"}\\"


def add_recipe(recipe, recipes):
	cats = recipe["recipeCategory"].split(", ")
	for cat in cats:
		if cat == "classic":
			continue

	name_id = recipe["name"].lower().replace(" ", "-")
	recipes[cat] += r"\noindent\begin{minipage}[t]{\linewidth}%" + "\n"
	recipes[cat] += r"{\Large\textbf{" + recipe["name"] + r"}} \label{" + name_id + r"}"
	recipes[cat] += r"\hfill\textit{" + recipe["author"]["name"] + r"}\\" + "\n"
	if recipe["description"] != "description of recipe":
		recipes[cat] += r"\textit{``" + recipe["description"] + r"''}\\" + "\n"
	if recipe["recipeYield"] != "yield":
		recipes[cat] += r"\textbf{Yield:} \textit{" + recipe["recipeYield"] + r"}\\" + "\n"

	recipes[cat] += r"\noindent\begin{minipage}[t]{0.78\linewidth}%" + "\n"
	recipes[cat] += r"\textbf{Ingredients}:\vspace{-3mm}" + "\n"
	recipes[cat] += r"\begin{multicols}{2}" + "\n"
	recipes[cat] += r"\begin{itemize}\setlength\itemsep{-1mm}" + "\n"
	for ingr in recipe["recipeIngredient"]:
		recipes[cat] += r"\item " + ingr + "\n"
	recipes[cat] += r"\end{itemize}" + "\n"
	recipes[cat] += r"\end{multicols}" + "\n"
	recipes[cat] += r"\end{minipage}" + "\n"

	recipes[cat] += r"\noindent\begin{minipage}[t]{0.18\linewidth}" + "\n"
	recipes[cat] += r"\centering \strut\vspace*{-\baselineskip}\newline" + "\n"
	recipes[cat] += r"\includegraphics[width=0.9\linewidth]{" + recipe["image"][0] + r"}\\" + "\n"
	recipes[cat] += r"\end{minipage}\vspace{3mm}" + "\n"

	recipes[cat] += r"\textbf{Directions}:" + "\n"
	recipes[cat] += r"\vspace{-3mm}\begin{enumerate}\setlength\itemsep{-1mm}" + "\n"
	for step in recipe["recipeInstructions"]:
		recipes[cat] += r"\item " + step["text"] + "\n"
	recipes[cat] += r"\end{enumerate}" + "\n"
	recipes[cat] += r"\end{minipage}\vspace{8mm}" + "\n"


def write_recipe_book(f, toc, recipes):
	print(r"\documentclass[11pt, twoside, openany]{book}", file=f)
	print(r"\usepackage[margin=0.5in]{geometry}", file=f)
	print(r"\usepackage{graphicx}", file=f)
	print(r"\usepackage{multicol}", file=f)
	print(r"\setlength{\parindent}{0pt}", file=f)
	print(r"\title{ \LARGE \textbf{Dunn Family Recipe Book}}", file=f)
	print(r"\begin{document}", file=f)
	print(r"\maketitle", file=f)
	print(r"\section*{Table of Contents}", file=f)
	for cat in categories:
		print(r"{~\vspace{2mm}\\ \Large \textbf{" + f"{cat}" + r"}}" + r"\hfill\textbf{\pageref{" + cat.lower() + r"}}" + "\n", file=f)
		print(toc[cat.lower()], file=f)
	for cat in categories:
		print(r"{\newpage \LARGE \textbf{" + f"{cat}" + r"}} \label{" + cat.lower() + r"}\\", file=f)
		print(recipes[cat.lower()], file=f)
	print(r"\end{document}", file=f)


# create strings
table_of_contents = {}
recipes = {}
for cat in categories:
	table_of_contents[cat.lower()] = ""
	recipes[cat.lower()] = ""

# add all recipes to book
for this_dir in directories:
	for json_fn in sorted(list(os.listdir(f"{json_dir}/{this_dir}"))):
		recipe = json.load(open(f"{json_dir}/{this_dir}/{json_fn}"))
		add_to_toc(recipe, table_of_contents)
		add_recipe(recipe, recipes)

# write book
write_recipe_book(f, table_of_contents, recipes)
