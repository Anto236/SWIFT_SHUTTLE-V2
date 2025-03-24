# Swift School Shuttle API

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python and `pip` installed, then install required dependencies:
```sh
pip install -r requirements.txt
```

### 2. Configure Database
Update `settings.py` to use MySQL on **port 3306**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'swift_shuttle_db',
        'USER': 'root',
        'PASSWORD': '',  # Update if necessary
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 3. Apply Migrations
Run the following commands to create database tables:
```sh
python manage.py makemigrations
python manage.py migrate
```

### 4. Start the Server
Run the Django development server:
```sh
python manage.py runserver 8000
```
Admin user is automatically created on startup.

## Authentication & API Testing

### Bearer Token Authentication
This API uses **JWT Authentication**. To access protected endpoints:

1. **Login to get a token**:
```http
POST /api/auth/login/
```
Request Body (JSON):
```json
{
  "username": "admin",
  "password": "admin123"
}
```
Response:
```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

2. **Use the token in requests**:
   - Add this header to API requests:
   ```
   Authorization: Bearer your_access_token
   ```

### Registration API
```http
POST /api/auth/register/
```
#### Request Body (JSON):
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "securepassword",
  "role": "parent",
  "is_active": true
}
```

### View API Endpoints
API documentation is available at:
👉 **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

🚀 **Use Postman for testing instead of Swagger.**

