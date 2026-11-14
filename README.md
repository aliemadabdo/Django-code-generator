# Django CRUD Code Generator

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)

A Django tool that **writes Django code for you**. You describe a model in a small web UI
(fields, types, foreign keys, choices, constraints), and the generator writes the boilerplate
into a target app: the model, a ModelForm and URL routes today, with CRUD views and admin registration in progress.

I built it because most of my day-to-day Django work started with the same steps for every new
entity: model → admin → form → add/edit/delete/search views → URLs. This automates that step.

## What it generates

For a model such as `Supplier`:

| File        | Generated code                                                                   | Status |
|-------------|----------------------------------------------------------------------------------|--------|
| `models.py` | The model class, with each field's type, `max_length`, `null`/`blank`, `unique`, `default`, `choices`, `verbose_name`, `help_text`, and `ForeignKey` relations | ✅ Done |
| `forms.py`  | A `ModelForm` for the model                                                      | ✅ Done |
| `urls.py`   | Routes for the CRUD views, added to the existing `urlpatterns` (the file is created if it is empty) | ✅ Done |
| `views.py`  | `add_supplier`, `edit_supplier`, `delete_supplier`                               | 🚧 Generators written, not yet called from the UI |
| `admin.py`  | `@admin.register(Supplier)` block                                                | 🚧 Generator written, not yet called from the UI |
| search view | List and filter view                                                             | 📝 Planned |

Generated code is **appended** to existing files, so it does not overwrite code you already wrote.

## How it works

```
 Web UI (forms)  ──▶  ModelField / model definitions stored in the DB
                              │
                              ▼
                 helpers.py: build_field_code(), CreateModel(),
                 create_forms(), create_urls(), create_*_view()
                              │
                              ▼
          Python source written into the target app's files
```

- `generator/forms.py`: forms for adding an app, a model and its fields
- `generator/helpers.py`: turns field definitions into Python source and writes or appends it to the target files
- `generator/configs.py`: the path of the project and app that receive the generated code

## Run it locally

```bash
git clone https://github.com/aliemadabdo/Django-code-generator.git
cd Django-code-generator/crud_gen
python -m venv .venv && source .venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/ and:

1. Set `PROJECT_URL` and `APP_NAME` in `generator/configs.py` to the project and app that should receive the code.
2. Add the fields (`/add_field/`), then the model (`/add_model/`).
3. Check the generated code in the target app, then run `makemigrations` and `migrate`.

## Roadmap

- [ ] Call the view and admin generators from the UI, and implement the search view
- [ ] Read the target path from settings or env instead of `configs.py` (cross-platform paths with `pathlib`)
- [ ] Generate DRF serializers, ViewSets and routers, not only template views
- [ ] Generate tests for each CRUD view
- [ ] Package it as a `manage.py generate_crud` management command

## Notes

Design notes: [`docs/task_automation.md`](docs/task_automation.md) and [`docs/learning_notes.md`](docs/learning_notes.md).
