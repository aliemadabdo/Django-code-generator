**Quick Summary — Django Static Files**

* **`STATIC_URL`** → The URL prefix used in templates to access static files (e.g., `/static/`).
* **`STATICFILES_DIRS`** → Extra folders Django searches for static files **during development** (along with each app’s `static/` folder).
* **`STATIC_ROOT`** → The single folder where all static files are collected **for production** using `python manage.py collectstatic`.

**Key point:** In development, Django serves static files directly from `STATICFILES_DIRS` and app `static/` folders.
`STATIC_ROOT` is **only used in production** and may be empty until `collectstatic` is run.
