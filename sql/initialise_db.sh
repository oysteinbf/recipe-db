#cat drop_tables.sql | sqlite3 ../food.db
cat create_tables.sql | sqlite3 ../food.db

# Insert some dummy data:
data='{ "name": "Avocado Salad",
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

curl -d "$data" -H "Content-Type: application/json" -X POST http://localhost:8000/recipe
