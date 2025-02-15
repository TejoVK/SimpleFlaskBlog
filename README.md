# Flask Blog Application

This Flask application is a simple blogging platform with functionalities such as viewing, adding, editing, and deleting posts, as well as handling user authentication and file uploads. It also includes a contact form and supports email notifications (optional).

## Features

- **Homepage**: Displays a paginated list of blog posts.
- **About Page**: Provides information about the blog.
- **Dashboard**: Admin interface for managing posts (CRUD operations) and file uploads.
- **Contact Form**: Allows users to send messages through the website.
- **User Authentication**: Admin login to access the dashboard.
- **File Uploads**: Allows administrators to upload files.

## Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL database server
- A Gmail account for sending emails (optional)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
2. **Install Dependencies:**

Create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. **Configure PostgreSQL:**

Create a PostgreSQL database for the application.

Update the configure.json file with your PostgreSQL connection details:

```json
{
    "params": {
        "gmail": "your_email@gmail.com",
        "gp": "your_email_password",
        "local_server": "postgresql://username:password@localhost/dbname",
        "upload_path": "uploads",
        "no_of_posts": 5,
        "admin_user": "admin",
        "admin_password": "password"
    }
}
```
Replace username, password, localhost, and dbname with your PostgreSQL credentials and database name. Replace "your_email@gmail.com" and "your_email_password" with your Gmail credentials. Update "upload_path", "no_of_posts", "admin_user", and "admin_password" according to your preferences.

4. **Create the Database Tables:**

Run the following command to create the necessary database tables:

```python
 python main.py
```
Exit the Python shell after the tables are created. the db.create_all() in the main.py will create all the database tables.

5. **Usage**
Run the Application:

```python
 python main.py
```
The application will start on `(http://127.0.0.1:5000)`.

6. **Access the Dashboard:**

Navigate to /dashboard to log in with the admin credentials specified in configure.json.
Use the dashboard to manage posts and upload files.
Contact Form:

Navigate to /contact to send a message.
Optionally configure email sending in the contact route by uncommenting and configuring the mail.send_message line.

7. **File Structure**
   
main.py: Main application file.
configure.json: Configuration file for the application.
requirements.txt: List of Python dependencies.
templates/: Directory containing HTML templates.
static/: Directory for static files (CSS, JavaScript, images).

8. **Contributing**
    
Feel free to fork the repository and submit pull requests. Contributions are welcome!

9. **License**
 
This project is licensed under the MIT License.
