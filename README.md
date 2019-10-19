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
