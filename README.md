# recipe-db
API for managing food recipes, using [FastAPI](https://fastapi.tiangolo.com/) and [SQLite](https://www.sqlite.org/).

## Database model
<img src="img/model_recipes.png" alt="DB model"/>

## Project setup

First install [Poetry](https://python-poetry.org/docs/#installation), then install the defined dependencies:

```
$ poetry install
```

Make sure SQLite is also installed, then create the tables:

```
$ cat sql/create_tables.sql | sqlite3 food.db
```

Start server:

```
$ poetry shell
$ uvicorn main:app --reload
```

## Usage
After having started the server, see http://127.0.0.1:8000/docs for the API documentation.

Some dummy data can e.g. be created as follows:

```
$ data='{ "name": "Avocado Salad",
        "introduction": "A very simple salad",
        "prep_time": 10,
        "cook_time": 0,
        "total_time": 10,
        "difficulty": "Easy",
        "child_friendly": 1,
        "leftover_friendly": 0,
        "source": null,
        "tags": null,
        "n_servings": 4,
        "ingredients": [
            { "name": "Avocado", "amount": 2, "unit": "pcs", "preparation_info": null },
            { "name": "Tomato", "amount": 2, "unit": "pcs", "preparation_info": "finely chopped" },
            { "name": "Garlic", "amount": 1, "unit": "clove", "preparation_info": "minced" }
        ],
        "method": [ "Chop all the ingredients", "Put all the ingredients in a bowl", "Serve" ],
        "categories": [ "Vegetarian", "Salad" ]
        } '

$ curl -d "$data" -H "Content-Type: application/json" -X POST http://localhost:8000/recipe
```
