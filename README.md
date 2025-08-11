# Django Code Generator

A Python-based tool that automates the creation of Django CRUD components, reducing repetitive development tasks and speeding up project setup.

This generator is designed to **append** generated code to existing files (not overwrite them), making it safe to integrate into ongoing projects.

---

## 🚀 Vision

The **Django Code Generator** aims to generate:

* **Models** – Django model classes based on user input.
* **Forms** – Django forms for creating and editing model data.
* **Views** – Django class-based or function-based CRUD views.
* **URLs** – Django URL patterns linking views to routes.
* **Templates** – HTML templates for create, read, update, and delete pages.

---

## 📌 Current Phase (Phase 1)

In **Phase 1**, we are focusing on generating **View files** with dynamic user input:

* Ask the user for required details through the terminal (or later via a simple UI).
* Append the generated view code into existing Django files instead of creating new ones.
* Keep the generated code reusable and easy to customize.

---

## 🛠 How It Works (Phase 1)

1. **Run the script** from the terminal.
2. **Provide details** such as:

   * App name
   * Model name
   * View type (class-based or function-based)
3. The script **appends** the generated CRUD view code into the target file.

---

## 📂 Project Structure (Phase 1)

```
crud_gen/
│── generator.py        # Main Python script for code generation  
│── templates/          # Predefined code templates (optional for later phases)  
│── README.md           # Project documentation  
```

---

## ⚡ Planned Features (Next Phases)

* Full CRUD generation (Models, Forms, Views, URLs, Templates).
* Integration with Django admin.
* UI-based code generation interface.
* Template customization support.

---

## 📋 Requirements

* Python 3.8+
* Django 4.x+


If you want, I can also make a **shorter, marketing-friendly version** of this README that’s more eye-catching for GitHub.
Do you want me to prepare that too?
