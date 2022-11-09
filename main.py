from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

class Recipe(BaseModel):
    name: str
    introduction: Union[str, None] = None
    prep_time: Union[int, None] = None
    cook_time: Union[int, None] = None
    source: Union[str, None] = None
    tags: Union[str, None] = None
    n_servings: int


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

@app.post("/recipes")
def create_recipe(recipe: Recipe):
    """Add recipe to the database"""
    sql = """
    INSERT INTO recipe (name, introduction, prep_time, cook_time, source, tags, n_servings)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    recipe_info = tuple(vars(recipe).values())
    with sqlite3.connect('food.db') as con:
        cur = con.cursor()
        cur.execute(sql, recipe_info)
        con.commit()
    return recipe

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
          SELECT i.name , bri.amount, bri.unit, bri.preparation_info
             from recipe r JOIN bridge_recipe_ingredient bri 
                ON r.id = bri.recipe_id
            JOIN ingredient i 
                ON i.id = bri.ingredient_id 
            WHERE r.id=?
          """
    with sqlite3.connect('food.db') as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(sql, str(id))
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
        cur.execute(sql, str(id))
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
        cur.execute(sql, str(id))
        categories = cur.fetchall()
    return categories
