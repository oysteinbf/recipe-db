CREATE TABLE recipe (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    introduction TEXT,
    prep_time INTEGER,
    cook_time INTEGER,
    total_time INTEGER,
    difficulty TEXT,
    child_friendly INTEGER,
    leftover_friendly INTEGER,
    source TEXT,
    tags TEXT,
    n_servings INTEGER DEFAULT 4 NOT NULL,
    isFav INTEGER DEFAULT 0
);

CREATE TABLE ingredient (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    category TEXT
);

CREATE TABLE bridge_recipe_ingredient (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER,
    ingredient_id INTEGER,
    amount REAL,
    unit TEXT,
    preparation_info TEXT,
    multiplication_factor INTEGER,
    FOREIGN KEY (recipe_id)
      REFERENCES recipe (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (ingredient_id)
      REFERENCES ingredient (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

CREATE TABLE method (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER NOT NULL, -- FK
    step_number INTEGER,
    step_description INTEGER
);

CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    symbol TEXT,
    color_code TEXT
);

CREATE TABLE bridge_recipe_category (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (recipe_id)
      REFERENCES recipe (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (category_id)
      REFERENCES category (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);
