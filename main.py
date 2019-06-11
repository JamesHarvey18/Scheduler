from app import app
import db_creator
from db_setup import init_db, db_session
from forms import SchedulerDataEntryForm, LocationForm, RegistrationForm, PasswordForm
from flask import Flask, flash, render_template, redirect, url_for, request, session, make_response
from models import Schedule, User, Password
from tables import Results
import datetime
from functools import wraps


init_db()


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You must log in to update location.")
            return redirect(url_for('login'))
    return wrap

# @login_required
@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    if request.cookies.get('location') is None:
        flash("Enter your location.")
        return redirect(url_for('add_location'))

    form = SchedulerDataEntryForm(request.form)

    if request.method == 'POST':

        try:
            save_changes(form)
        except Exception as e:
            return str(e)

        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    qry = db_session.query(Schedule)
    table = Results(qry)
    table.border = True
    print(qry.first())
    return render_template('search.html', table=table)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = PasswordForm(request.form)
    user = User()
    if request.method == 'POST':
        input_password = form.password.data
        username = form.username.data
        stored_password = user.get_stored_password(username)
        if user.verify_password(stored_password, input_password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Incorrect Password.')
    return render_template('login.html')



@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    pass


@app.route('/location', methods=['GET', 'POST'])
def add_location():
    form = LocationForm(request.form)
    location = form.location.data
    form.location.data = ''

    if request.method == 'POST':
        if location:
            res = make_response(redirect(url_for('index')))
            flash('Location updated.')
            res.set_cookie("location", location.upper(), expires=datetime.datetime.now() + datetime.timedelta(days=5000))
            return res
        else:
            flash('Enter a valid location.')

    return render_template('add_location.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        form = RegistrationForm(request.form)

        if request.method == 'POST':
            user = User()
            username = form.username.data
            email = form.email.data
            password = user.hash_password(form.password.data)

            qry = db_session.query(User).filter(User.username == username)
            qry = qry.first()

            if qry is not None:
                flash("Username is already taken, please choose another.")
                return render_template('register.html', form=form)
            else:
                user.username = username
                user.email = email
                user.password = password
                qry = db_session()
                qry.add(user)
                qry.commit()

                flash("Registration Successful")
                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('index'))

            return render_template('register.html', form=form)

    except Exception as e:
        return str(e)


def save_changes(form):
    schedule = Schedule()
    dt = datetime.datetime.now()

    schedule.part_number = form.part_number.data.upper()
    schedule.due_date = form.due_date.data
    schedule.part_description = 'PLACE HOLDER'
    schedule.job_number = form.job_number.data.upper()
    schedule.work_number = form.work_number.data.upper()
    schedule.part_quantity = form.part_quantity.data.upper()
    schedule.part_location = request.cookies.get('location').upper()
    schedule.entry_time = dt.strftime("%H:%M:%S")
    schedule.entry_date = datetime.date.today()
    schedule.employee_id = form.employee_id.data.upper()
    schedule.comments = form.comments.data.upper()
    schedule.revision = form.revision.data.upper()
    schedule.material_status = form.material_status.data.upper()
    schedule.machine_center = form.machine_center.data.upper()
    schedule.original_estimated_time = form.original_estimated_time.data.upper()
    schedule.revised_estimated_time = form.revised_estimated_time.data.upper()
    schedule.quantity_complete = form.quantity_complete.data
    schedule.actual_time = form.actual_time.data.upper()
    schedule.mtl = form.mtl.data.upper()

    qry = db_session()
    qry.add(schedule)
    qry.commit()


def get_description(part_number):
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, threaded=True, debug=True)
