from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json
import os
from werkzeug.utils import secure_filename

# Load configuration parameters
with open('configure.json', 'r') as c:
    params = json.load(c)["params"]

# Initialize Flask app
app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail'],
    MAIL_PASSWORD=params['gp']
)

mail = Mail(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_server']
app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = params['upload_path']
db = SQLAlchemy(app)

# Define database models
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(15), nullable=False)
    msg = db.Column(db.String(10000000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement =True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    img_file = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
# @app.route('/')
# def home():
#     posts = Posts.query.all()
#     last = len(posts)//params['no_of_posts']
    
#     page = int(request.args.get('page'))
#     if (str(page).isdigit()):
#         page = 0
    
#     if (page==1):
#         prev = '#'
#         next = '/?number='+str(page+1)
        
#     elif (page==last):
#         prev = '/?number='+str(page-1)
#         next = '#'
    
#     else:
#         prev = '/?number='+str(page-1)
#         next = '/?number='+str(page+1)

#     return render_template('index.html', params=params, posts=posts)



@app.route('/')
def home():
    posts_per_page = params.get('no_of_posts', 10)  # Default to 10 posts per page if not specified
    posts = Posts.query.all()
    
    # Calculate pagination variables
    total_posts = len(posts)
    last_page = (total_posts + posts_per_page - 1) // posts_per_page  # Calculate the last page number
    
    page = int(request.args.get('page', 1))  # Default to page 1 if not specified
    if page < 1:
        page = 1
    if page > last_page:
        page = last_page
    
    start = (page - 1) * posts_per_page
    end = start + posts_per_page
    paginated_posts = posts[start:end]

    # Define prev and next links
    if page == 1:
        prev = '#'
    else:
        prev = f'/?page={page - 1}'
    
    if page == last_page:
        next = '#'
    else:
        next = f'/?page={page + 1}'
    
    return render_template('index.html', params=params, posts=paginated_posts, prev=prev, next=next)




@app.route('/about')
def about():
    return render_template('about.html', params=params)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')

@app.route('/uploader', methods=['GET','POST'])
def uploader():
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return 'Uploaded successfully'

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)
    
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('password')
        if username == params['admin_user'] and password == params['admin_password']:
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)
            
    return render_template('login.html', params=params)

@app.route('/delete/<string:sno>')
def delete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashboard')

@app.route('/edit/<string:sno>', methods=['GET','POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            box_title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            
            if sno=='0':
                post = Posts(title=box_title, slug=slug, content=content, img_file=img_file)
                db.session.add(post)
                db.session.commit()
            
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.slug = slug
                post.content = content
                post.img_file = img_file
                db.session.commit()
                return redirect('/edit/'+sno)
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=post)
                

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        entry = Contacts(name=name, phone_num=phone, msg=message, email=email)
        db.session.add(entry)
        db.session.commit()
        
        # Uncomment and configure if you want to enable email sending
        # mail.send_message("New message from " + name,
        #                   sender=email,
        #                   recipients=[params['gmail']],
        #                   body=message + "\n" + phone)
        
    return render_template('contact.html', params=params)

@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
