DROP TABLE IF EXISTS post_tags;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS tags;

CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tags (
    tag_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    tag VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    category INT,
    createdAt DATETIME NOT NULL,
    updatedAt DATETIME NOT NULL,
    FOREIGN KEY (category) REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS post_tags (
    post_id INT,
    tag_id INT,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
);


-- For categories
INSERT INTO categories (category) VALUES ("Technology");
INSERT INTO categories (category) VALUES ("Lifestyle");
INSERT INTO categories (category) VALUES ("Health & Fitness");
INSERT INTO categories (category) VALUES ("Travel");
INSERT INTO categories (category) VALUES ("Food & Recipes");
INSERT INTO categories (category) VALUES ("Personal Development");
INSERT INTO categories (category) VALUES ("Business & Finance");
INSERT INTO categories (category) VALUES ("Education");
INSERT INTO categories (category) VALUES ("Entertainment");
INSERT INTO categories (category) VALUES ("Science");

-- Technology Tags
INSERT INTO tags (tag) VALUES ('Gadgets');
INSERT INTO tags (tag) VALUES ('Tech News');
INSERT INTO tags (tag) VALUES ('AI');
INSERT INTO tags (tag) VALUES ('Apps');
INSERT INTO tags (tag) VALUES ('Coding');

-- Lifestyle Tags
INSERT INTO tags (tag) VALUES ('Minimalism');
INSERT INTO tags (tag) VALUES ('Work-Life Balance');
INSERT INTO tags (tag) VALUES ('Mindfulness');
INSERT INTO tags (tag) VALUES ('Fashion');
INSERT INTO tags (tag) VALUES ('Home Decor');

-- Health & Fitness Tags
INSERT INTO tags (tag) VALUES ('Nutrition');
INSERT INTO tags (tag) VALUES ('Workout');
INSERT INTO tags (tag) VALUES ('Mental Health');
INSERT INTO tags (tag) VALUES ('Yoga');
INSERT INTO tags (tag) VALUES ('Healthy Habits');

-- Travel Tags
INSERT INTO tags (tag) VALUES ('Solo Travel');
INSERT INTO tags (tag) VALUES ('Budget Travel');
INSERT INTO tags (tag) VALUES ('Travel Guides');
INSERT INTO tags (tag) VALUES ('Hidden Gems');
INSERT INTO tags (tag) VALUES ('Cultural Experiences');

-- Food & Recipes Tags
INSERT INTO tags (tag) VALUES ('Vegan');
INSERT INTO tags (tag) VALUES ('Quick Meals');
INSERT INTO tags (tag) VALUES ('Desserts');
INSERT INTO tags (tag) VALUES ('Meal Prep');
INSERT INTO tags (tag) VALUES ('Home Cooking');

-- Personal Development Tags
INSERT INTO tags (tag) VALUES ('Habits');
INSERT INTO tags (tag) VALUES ('Goal Setting');
INSERT INTO tags (tag) VALUES ('Motivation');
INSERT INTO tags (tag) VALUES ('Self-Care');
INSERT INTO tags (tag) VALUES ('Growth Mindset');

-- Business & Finance Tags
INSERT INTO tags (tag) VALUES ('Startups');
INSERT INTO tags (tag) VALUES ('Investing');
INSERT INTO tags (tag) VALUES ('Money Tips');
INSERT INTO tags (tag) VALUES ('Entrepreneurship');
INSERT INTO tags (tag) VALUES ('Side Hustles');

-- Education Tags
INSERT INTO tags (tag) VALUES ('E-learning');
INSERT INTO tags (tag) VALUES ('Study Tips');
INSERT INTO tags (tag) VALUES ('Online Courses');
INSERT INTO tags (tag) VALUES ('Exam Prep');
INSERT INTO tags (tag) VALUES ('Learning Tools');

-- Entertainment Tags
INSERT INTO tags (tag) VALUES ('Movies');
INSERT INTO tags (tag) VALUES ('TV Shows');
INSERT INTO tags (tag) VALUES ('Celebrity News');
INSERT INTO tags (tag) VALUES ('Music');
INSERT INTO tags (tag) VALUES ('Book Reviews');

-- Science Tags
INSERT INTO tags (tag) VALUES ('Space');
INSERT INTO tags (tag) VALUES ('Physics');
INSERT INTO tags (tag) VALUES ('Biotech');
INSERT INTO tags (tag) VALUES ('Climate');
INSERT INTO tags (tag) VALUES ('Innovation');

-- Adding a post
-- 1. Check whether the metioned category is present in the categories table
-- 2. If its present, then get the category_id to add in the category column in post

INSERT INTO posts 
(title, content, category, createdAt, updatedAt)
VALUES
(
    "My First Post", 
    "This is my first Post", 
    (SELECT category_id FROM categories WHERE LOWER(category) = LOWER("Health & Fitness")),
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- 3. Adding the relavant tags

INSERT INTO post_tags (post_id, tag_id) VALUES (1, 12);

INSERT INTO post_tags (post_id, tag_id) VALUES (1, 7);
