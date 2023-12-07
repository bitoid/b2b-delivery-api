# b2b-delivery-api

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/b2bapi.git
```

2. Navigate to the project directory:
```
cd b2bapi
```

3. Create and activate virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

4. Install the requirements:
```
pip install -r requirements.txt
```

5. Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```

6. Start the Django development server:
```
python manage.py runserver
```

7. Access the API at: 
`http://127.0.0.1:8000/api/`