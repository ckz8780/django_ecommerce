# Django E-commerce

A small e-commerce app using Django 2

# Step by Step

### Initial Setup:

*Note: Some steps may be slightly different depending on your OS/virtualenv choice. This assumes Ubuntu Linux and [virtualenvwrapper's mkproject](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html#project-directory-management)*

- Create a virtualenv/environment to work in

		mkproject -p python3 <project_folder>
- Install Django:
		
		pip install django
- Create a new Django project
		
		django-admin startproject <project_name> .
		cd <project_name>
- Create `.gitignore`:

		touch <project_name>/.gitignore
- Populate `.gitignore` w/ content:

		*.sqlite3
		*.pyc
		__pycache__
- Create `README.md`:

		touch README.md
- Test run: 

		cd <project_folder>
		python manage.py runserver

		# Visit http://127.0.0.1:8000, verify project is running
- Stop server and run initial migrations:

		ctrl+C
		python manage.py migrate

- Create superuser:

		python manage.py createsuperuser
		python manage.py runserver

		# Enter username, email, password
		# Visit http://127.0.0.0:8000/admin/, verify superuser login

- Initialize git and push initial commit:

		ctrl+C
		git init
		git add .
		git commit -m "initial commit"
		git remote add origin git@github.com:<username>/<repo_name>.git
		git push -u origin master

----------

### Initial Authentication Setup with [django-allauth](https://django-allauth.readthedocs.io/en/latest):

- Install allauth:

		pip install django-allauth
- Update settings per [docs here](https://django-allauth.readthedocs.io/en/latest/installation.html) We're not using any social providers at this point. **Make sure to add `SITE_ID = 1`**
- Add allauth URLs to `<project_name>/urls.py`

		from django.urls import path, include

		urlpatterns = [
			# ...
			path('accounts/', include('allauth.urls')),
			# ...
		]

- Run allauth migrations:

		python manage.py migrate
- Run the server and navigate to http://127.0.0.1:8000/admin/sites/ and update the default example.com site:

		python manage.py runserver

		# Domain Name: 127.0.0.1:8000
		# Display Name: localhost
- Logout of the admin (so we can test login in a moment)
- Add additional allauth config in `settings.py`:

		# Additional django-allauth settings:

		AUTHENTICATION_BACKENDS = (
			# Needed to login by username in Django admin, regardless of `allauth`
			'django.contrib.auth.backends.ModelBackend',
			# `allauth` specific authentication methods, such as login by e-mail
			'allauth.account.auth_backends.AuthenticationBackend',
		)

		# Log emails to console in dev
		EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

		ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
		ACCOUNT_EMAIL_REQUIRED = True
		ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
		ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
		ACCOUNT_USERNAME_MIN_LENGTH = 4
		LOGIN_URL = '/accounts/login/'
		LOGIN_REDIRECT_URL = '/'

		SITE_ID = 1
- Navigate to http://127.0.0.1:8000/accounts/login/ and login w/ the superuser. You'll be redirected to `/accounts/confirm-email/` if allauth is set up properly
- Navigate to http://127.0.0.1:8000/admin/ and login w/ the superuser
- Create an `EmailAddress` in the `ACCOUNTS` app in the admin, tied to your superuser's user ID (use the search icon) and mark it as `verified` and `primary`. The email itself doesn't matter, as long as it's not blank
- Logout of the admin again, navigate back to http://127.0.0.1:8000/accounts/login/ and login with the superuser again. Now you will get a 404 as allauth attempts to redirect you to `/` which currently has no URL
- Create allauth templates directory:

		mkdir ./<project_name>/templates
		mkdir ./<project_name>/templates/allauth
- Freeze requirements:

		pip freeze > <project_folder>/requirements.txt
- Commit:

		git add .
		git commit -m "initial allauth setup"
		git push
		