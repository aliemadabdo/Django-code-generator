# Django CRUD Code Generation Plan

## Overview
Through this file, we want to **automate the generation** of code for pages that use CRUD operations.  
We will generate **4 pages**:  
- **Add**  
- **Search**  
- **Edit**  
- **Delete**  

For each feature (when necessary), we will create:  
- A **Form**  
- A **View**  
- A **Template**  

---

## Information Required from Programmer
1. **Base directory of the app** and the name of the folder inside the app (if it exists).  
2. **Model name** to be used for CRUD generation.  

---

## Tasks for the Programmer
The programmer must manually:  
1. Create the app or directory with all needed files:  
   - `models.py`  
   - `forms.py`  
   - `views.py`  
   - `urls.py`  
   - `templates/` directory  
2. Write the model with its **fields** and **constraints**.  
3. Run `makemigrations` and `migrate` to apply database changes.  

---

## Guidelines
- **Append** to `forms.py`, `urls.py`, and `views.py` if the file exists.  
  - If the file does **not** exist, raise an error message.  
- Create a **template** for each page in the app’s `templates` directory.  
- Create a **base.html** file in the templates directory and **extend** it in other templates.  
- Create a **form** for each feature in `forms.py`.  
- Create a **view** for each feature in `views.py`.  
- Create a **URL** for each view in `urls.py`.  

---

## Feature Details

### 1. Add Feature
- Create a form with the model’s fields.  
- Create a view that handles **GET** and **POST** requests:  
  - Display the form.  
  - Handle form submission and save data to the database.  
- Create a template that:  
  - Extends `base.html`.  
  - Displays the form with a **Save** button.  
- Create a URL mapping to the view.  

---

### 2. Search Feature
- Create a form with the model’s fields.  
- Create a view that handles **GET** and **POST** requests:  
  - Display the form.  
  - Search the database.  
- Create a template that:  
  - Extends `base.html`.  
  - Displays the form and **search results**.  
  - Links to **Edit** and **Delete** features.  
  - Has dynamic table columns based on user choice.  
  - Includes a nested **Order By** feature.  
- Create a URL mapping to the view.  

---

### 3. Edit Feature
- Reuse the **Add** form with the model’s fields.  
- Create a view that handles **GET** and **POST** requests:  
  - Display the form pre-filled with existing data.  
  - Update the database on submission.  
- Create a template that:  
  - Extends `base.html`.  
  - Displays the form with a **Save** button.  
- Create a URL mapping to the view.  

---

### 4. Delete Feature
- Create a view that handles **GET** and **POST** requests:  
  - Display a confirmation page.  
  - Delete the data from the database.  
- Create a template that:  
  - Extends `base.html`.  
  - Displays a confirmation message with a **Delete** button.  
- Create a URL mapping to the view.  
