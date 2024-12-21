# Mofa's Kitchen Buddy

Mofa's Kitchen Buddy is a backend system designed to simplify ingredient management and suggest recipes based on what you have at home. It features a chatbot powered by a Large Language Model (LLM) that provides personalized recipe recommendations tailored to user preferences.

---

## Techonolgies used:
- Backend stack: Django, Django Rest Framework 
- Database: SQLite3
- Additional: python requests
- LLM APIs: OpenAI api, Gemini API
- Tools: Postman, VScode

## API Documentation

## Base URL
- **`http://127.0.0.1:8000/`**

---

## Endpoints

### **Ingredient Managing**

#### 1. **GET Ingredients**
- **URL:** `{{baseURL}}ingredient/`
- **Method:** `GET`
- **Query Parameters:** 
  - `id` (optional, disabled in sample)

#### 2. **Create an Ingredient**
- **URL:** `{{baseURL}}ingredient/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "ingredient_name": "Eggs",
      "quantity": 12,
      "unit": "pieces",
      "price": 150
  }
  ```

#### 3. **Update an Ingredient**
- **URL:** `{{baseURL}}ingredient/1`
- **Method:** `PUT`
- **Request Body:**
  ```json
  {
      "ingredient_name": "Flour",
      "quantity": 4,
      "unit": "KG",
      "price": 120
  }
  ```

#### 4. **Delete an Ingredient**
- **URL:** `{{baseURL}}ingredient/2`
- **Method:** `DELETE`
- **Request Body:**
  ```json
  {
      "ingredient_name": "Flour",
      "quantity": 4,
      "unit": "KG",
      "price": 120
  }
  ```

---

### **Recipe Managing**

#### 1. **GET All Recipes**
- **URL:** `{{baseURL}}recipe_retrieval/recipes/`
- **Method:** `GET`

#### 2. **Add a Recipe**
- **URL:** `{{baseURL}}recipe_retrieval/recipes/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "name": "Spaghetti Carbonara",
      "taste": "5/5",
      "cuisine_type": "Italian",
      "preparation_time": "25 minutes",
      "reviews": 500
  }
  ```

#### 3. **Add a Recipe with Image**
- **URL:** `{{baseURL}}recipe_retrieval/recipes/?ocr=true`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "image_url": "https://i.ibb.co.com/sg5BmYy/Screenshot-2024-12-21-at-9-26-08-PM.png"
  }
  ```

---

### **Retrieve Recipe by Chatbot**

#### 1. **Chat**
- **URL:** `{{baseURL}}recipe_retrieval/chat/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "message": "hello! i wanna eat something cheap"
  }
  ```

---

### Variables
- **`baseURL`**: Default value is `http://127.0.0.1:8000/`.
