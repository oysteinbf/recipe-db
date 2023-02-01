from typing import Union, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

class Ingredient(BaseModel):
    name: str
    amount: Union[int, None] = None
    unit: Union[str, None] = None
    preparation_info: Union[str, None] = None

class Recipe(BaseModel):
    name: str
    introduction: Union[str, None] = None
    prep_time: Union[int, None] = None
    cook_time: Union[int, None] = None
    total_time: Union[int, None] = None
    difficulty: Union[str, None] = None
    child_friendly: Union[bool, None] = None
    leftover_friendly: Union[bool, None] = None
    source: Union[str, None] = None
    tags: Union[str, None] = None
    n_servings: int
    ingredients: List[Ingredient] = []
    method: List[str] = []
    categories: List[str] = []

class FavIDs(BaseModel):
    ids: List[int] = []

app = FastAPI()

# Allow CORS, ref. https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/recipe")
def create_recipe(data: Recipe):
    """Add recipe

        Example body:
       {
        "name": "Avocado Salad",
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
        } 
"""
    with sqlite3.connect('food.db') as con:
        con.execute('PRAGMA foreign_keys = ON;') # Enable foreign key support
        cur = con.cursor()
        # First get a list of existing ingredients. Insert into table if new ingredient does not exist.
        cur.execute('SELECT name FROM ingredient')
        ingredients = [x[0] for x in cur.fetchall()]  # ["Avokado", "Chili", ...]
        ingredient_pks = []
        ingredient_names = [x.name for x in data.ingredients]
        for x in ingredient_names:
            if x not in ingredients:
                cur.execute('INSERT INTO ingredient (name) VALUES (?)', (x,))
            # Get PKs for later insertion into bridge table
            cur.execute('SELECT id FROM ingredient WHERE name = ?', (x,))
            ingredient_pks.append(cur.fetchone()[0])
        # Now insert the recipe info

        recipe_info = (data.name, data.introduction, data.prep_time, data.cook_time, data.total_time,
                       data.difficulty, data.child_friendly, data.leftover_friendly,
                       data.source, data.tags, data.n_servings)
        sql_recipe = """
        INSERT INTO recipe (name, introduction, prep_time, cook_time, total_time, difficulty,
         child_friendly, leftover_friendly, source, tags, n_servings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cur.execute(sql_recipe, recipe_info)
        # Get PK for later insertion into other tables
        cur.execute('SELECT id from recipe where name = ?', (data.name,))
        recipe_pk = cur.fetchone()[0]

        # Insert data into bridge table (now we have all PKs)
        sql_bri = """INSERT INTO bridge_recipe_ingredient
                    (recipe_id, ingredient_id, amount, unit, preparation_info)
                     VALUES (?, ?, ?, ?, ?) """
        for i in range(0, len(ingredient_pks)):
            ingredient_info = (recipe_pk, ingredient_pks[i], data.ingredients[i].amount,
                 data.ingredients[i].unit, data.ingredients[i].preparation_info)
            cur.execute(sql_bri, ingredient_info)

        # Get a list of existing categories. Insert into table if new category does not exist.
        cur.execute('SELECT name FROM category')
        existing_categories = [x[0] for x in cur.fetchall()]  # ["Suppe", "Fisk", ...]
        category_pks = []
        #category_names = [x for x in data.categories]
        for x in data.categories:#category_names:
            if x not in existing_categories:
                cur.execute('INSERT INTO category (name) VALUES (?)', (x,))
            # Get PKs for later insertion into bridge table
            cur.execute('SELECT id FROM category WHERE name = ?', (x,))
            category_pks.append(cur.fetchone()[0])

        # Insert data into bridge table (now we have all PKs)
        sql_brc = """INSERT INTO bridge_recipe_category
                    (recipe_id, category_id)
                     VALUES (?, ?) """
        for i in range(0, len(category_pks)):
            category_info = (recipe_pk, category_pks[i])
            cur.execute(sql_brc, category_info)

        # Add the method descriptions
        sql_method = """INSERT INTO method (recipe_id, step_number, step_description)
                VALUES (?, ?, ?)"""
        for i, step_description in enumerate(data.method):
            cur.execute(sql_method, (recipe_pk, i, step_description))

        con.commit()
    return data

@app.put("/favourites")
def update_favourites(favids: FavIDs):
    """Update favourites (isFav) for the recipes
       The field isFav is changed by the frontend application,
       and is persisted in the database by this function
    """
    sql1 = """UPDATE recipe SET isFav=0 WHERE 1=1""" # First set all to 0
    sql2 = """UPDATE recipe SET isFav=1 WHERE id = ?"""
    with sqlite3.connect('food.db') as con:
        cur = con.cursor()
        cur.execute(sql1)
        for favid in favids.ids:
            cur.execute(sql2, (favid,))
            con.commit()
    return {"favids": favids.ids}

@app.get("/recipes")
def read_recipes():
    """Get all recipes"""
    with sqlite3.connect('food.db') as con:
        con.row_factory = dict_factory
        # https://docs.python.org/3.8/library/sqlite3.html#sqlite3.Connection.row_factory
        cur = con.cursor()
        cur.execute('SELECT * FROM recipe')
        recipes = cur.fetchall()
        # Convert to boolean (not supported by SQLite)
        for r in recipes:
            r['isFav'] = False if r['isFav'] == 0 else True
    return recipes

@app.get("/ingredients")
def read_ingredients():
    """Get all ingredients"""
    sql = """
          SELECT r.id, i.name , bri.amount, bri.unit, bri.preparation_info
             from recipe r JOIN bridge_recipe_ingredient bri 
                ON r.id = bri.recipe_id
            JOIN ingredient i 
                ON i.id = bri.ingredient_id 
          """
    with sqlite3.connect('food.db') as con:
        con.row_factory = dict_factory
        # https://docs.python.org/3.8/library/sqlite3.html#sqlite3.Connection.row_factory
        cur = con.cursor()
        cur.execute(sql)
        ingredients = cur.fetchall()

    return ingredients

@app.get("/ingredient/{id}")
def read_ingredient(id: int):
    """Get the ingredients for a specific recipe"""
    sql = """
          SELECT i.name , bri.amount, bri.unit, bri.preparation_info, bri.multiplication_factor
             from recipe r JOIN bridge_recipe_ingredient bri
                ON r.id = bri.recipe_id
            JOIN ingredient i 
                ON i.id = bri.ingredient_id 
            WHERE r.id=?
          """
    with sqlite3.connect('food.db') as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(sql, (id,))
        ingredients = cur.fetchall()
    return ingredients


@app.get("/method/{id}")
def read_method(id: int):
    """Get the method for a specific recipe"""
    sql = """
          select id, step_description from method where recipe_id = ? order by step_number
          """
    with sqlite3.connect('food.db') as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(sql, (id,))
        method = cur.fetchall()
    return method


@app.get("/category/{id}")
def read_category(id: int):
    """Get the categories for a specific recipe"""
    sql = """
          SELECT
              c.name,
              c.symbol,
              c.color_code
          from
              category c
          JOIN bridge_recipe_category brc
                      ON
              c.id = brc.category_id
          JOIN recipe r 
                      ON
              r.id = brc.recipe_id
          WHERE
              r.id = ?
          """
    with sqlite3.connect('food.db') as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(sql, (id,))
        categories = cur.fetchall()
    return categories

@app.get("/groceries")
def read_groceries():
    """Get the grocery list for all recipes marked as favourite"""
    sql = """
          with ingredients AS
          (SELECT i.name,
                   i.category,
                   bri.amount,
                   bri.unit
          FROM ingredient i
          JOIN bridge_recipe_ingredient bri
              ON i.id = bri.ingredient_id
          JOIN recipe r
              ON bri.recipe_id = r.id
          WHERE r.isFav = 1)
          SELECT name,
                   category,
                   sum(amount) AS amount,
                   unit
          FROM ingredients
          GROUP BY  name, category, unit
          ORDER BY  category, name;
          """
    with sqlite3.connect('food.db') as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(sql)
        groceries = cur.fetchall()

    return groceries
