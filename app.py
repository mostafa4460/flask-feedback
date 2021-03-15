from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def index():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User.register(
            username = form.username.data,
            password = form.password.data,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data
        )
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username

        flash(f"Welcome to our janky website {new_user.username}", "success")
        return redirect(f'/users/{new_user.username}')

    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)
        if user:
            session["username"] = user.username
            flash(f"Welcome back {user.username}!", "success")
            return redirect(f'/users/{user.username}')
        else:
            form.password.errors.append("Incorrect username/password. Please try again")
    return render_template("login.html", form=form)

@app.route('/users/<username>')
def user_details(username):
    if "username" in session:
        user = User.query.get_or_404(username)
        if session["username"] == user.username:
            return render_template("user.html", user=user)
        else:
            flash("You are not authorized to view this page", "danger")
    else:
        flash("Please log in to view this page", "danger")
        
    return redirect('/login')

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if "username" in session:
        user = User.query.get_or_404(username)
        cur_username = session["username"]

        if user.username == cur_username:
            Feedback.query.filter_by(username=user.username).delete()
            db.session.delete(user)
            db.session.commit()
            session.pop("username")
            flash("Successfully deleted user", "primary")
            return redirect('/')
        else:
            flash("You are not authorized to do this", "danger")
            return redirect(f"/users/{cur_username}")
    else:
        flash("You need to login to be able to do this", "danger")
        return redirect("/login")


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    if "username" in session:
        user = User.query.get_or_404(username)

        if user.username == session["username"]:
            form = FeedbackForm()

            if form.validate_on_submit():
                f = Feedback(
                    title = form.title.data,
                    content = form.content.data,
                    username = user.username
                )
                db.session.add(f)
                db.session.commit()
                flash("Feedback successfully added", "success")
                return redirect(f"/users/{user.username}")
            else:
                return render_template("add-feedback-form.html", form=form)
        else:
            cur_username = session["username"]
            flash("You are not authorized to view this page", "danger")
            return redirect(f"/users/{cur_username}")
    else:
        flash("Please log in to view this page", "danger")
        return redirect("/login")

@app.route('/feedback/<int:id>/update', methods=["GET", "POST"])
def update_feedback(id):
    if "username" in session:
        feedback = Feedback.query.get_or_404(id)

        if feedback.user.username == session["username"]:
            form = FeedbackForm(obj=feedback)

            if form.validate_on_submit():
                feedback.title = form.title.data
                feedback.content = form.content.data
                db.session.commit()
                flash("Feedback updated successfully", "success")
                return redirect(f"/users/{feedback.user.username}")
            else:
                return render_template("update-feedback-form.html", form=form)
        else:
            cur_username = session["username"]
            flash("You are not authorized to view this page", "danger")
            return redirect(f"/users/{cur_username}")
    else:
        flash("Please log in to view this page", "danger")
        return redirect("/login")

@app.route('/feedback/<int:id>/delete', methods=["POST"])
def delete_feedback(id):
    if "username" in session:
        feedback = Feedback.query.get_or_404(id)
        cur_username = session["username"]

        if feedback.user.username == cur_username:
            db.session.delete(feedback)
            db.session.commit()
            flash("Feedback successfully deleted", "primary")
            return redirect(f"/users/{cur_username}")
        else:
            flash("You are not authorized to do that", "danger")
            return redirect(f"/users/{cur_username}")
    else:
        flash("Please log in to view this page", "danger")
        return redirect("/login")

@app.route('/logout')
def logout():
    session.pop("username")
    flash("Successfully logged out, please come back soon!", "success")
    return redirect('/')