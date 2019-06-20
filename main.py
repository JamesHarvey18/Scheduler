from app import app
import db_creator
from db_setup import init_db, db_session
from forms import SchedulerDataEntryForm, LocationForm, RegistrationForm, LoginForm
from flask import Flask, flash, render_template, redirect, url_for, request, session, make_response
from models import Schedule, User, Password
from tables import Results
import datetime
from functools import wraps
from validate_email import validate_email


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


@app.route('/schedules/master', methods=['GET', 'POST'])
def search():
    qry = db_session.query(Schedule)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = User()
    if request.method == 'POST':
        user.password = request.form['pass']
        user.username = request.form['email']
        print('test ', user.username)
        if user.verify():
            session['logged_in'] = True
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            flash('Incorrect Password.')
    return render_template('login.html')


@app.route('/schedules/AMCH', methods=['GET', 'POST'])
def amch():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'AMCH')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/DELC', methods=['GET', 'POST'])
def delc():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'DELC')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/DGAS', methods=['GET', 'POST'])
def dgas():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'DGAS')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/DGUI', methods=['GET', 'POST'])
def dgui():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'DGUI')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/DMCH', methods=['GET', 'POST'])
def dmch():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'DMCH')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/DPLC', methods=['GET', 'POST'])
def dplc():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'DPLC')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/DPRC', methods=['GET', 'POST'])
def dprc():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'DPRC')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/EDFT', methods=['GET', 'POST'])
def edft():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'EDFT')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/MDFT', methods=['GET', 'POST'])
def mdft():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'MDFT')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/PSOP', methods=['GET', 'POST'])
def psop():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'PSOP')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/TEST', methods=['GET', 'POST'])
def test():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'TEST')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Schedule).filter(Schedule.id == id)
    entry = qry.first()

    if entry:
        form = SchedulerDataEntryForm(formdata = request.form, obj=entry)
        if request.method == 'POST':
            save_changes(form)
            flash('Schedule updated successfully')
            return redirect('/search')
        return render_template('edit.html', form=form)
    else:
        return 'Error loading #{id}. Please report this issue.'.format(id=id)


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


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        qry = db_session.query(Schedule).filter(Schedule.id == id)
        entry = qry.first()

        if entry:
            db_session.delete(entry)
            db_session.commit()
            flash('Entry deleted')
            return redirect('/search')
        else:
            return 'ERROR DELETING #{id}'.format(id=id)

    return render_template('delete.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            user = User()
            username = request.form['username']
            email = request.form['email']
            print(email)
            password = user.hash_password(request.form['pass'])
            confirm_password = user.hash_password(request.form['confirm_pass'])

            qry = db_session.query(User).filter(User.username == username)
            qry_email = db_session.query(User).filter(User.email == email)

            qry = qry.first()
            qry_email = qry_email.first()

            if qry is not None or qry_email is not None:
                flash('Username/email is already taken, please choose another.')
                return render_template('register.html')
            
            if not validate_email(email):
                flash("Invalid email address.")
                return render_template('register.html')

            if email[-17:] != '@cvdequipment.com':
                flash('Please enter a valid CVD email address')
                return render_template('register.html')

            if password != confirm_password:
                flash('Passwords do not match.')
                return render_template('register.html')

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

    except Exception as e:
        return str(e)

    return render_template('register.html')


def preprocess_date(date):
    month = int(date[5:7])
    day = int(date[8:10])
    year = int(date[0:4])
    # date = year + "-" + month + "-" + day
    return datetime.date(year, month, day)


def save_changes(form):
    schedule = Schedule()
    dt = datetime.datetime.now()
    release_wo = form.job_number.data + ' ' + form.work_number.data

    schedule.part_number = form.part_number.data.upper()  # Manual
    schedule.due_date = preprocess_date(form.due_date.data)  # Manual
    schedule.part_description = schedule.get_description()  # Jobscope
    schedule.job_number = form.job_number.data.upper()  # Manual
    schedule.work_number = form.work_number.data.upper()  # Manual
    try:
        schedule.part_quantity = schedule.get_quantity(form.part_number.data, release_wo)  # Jobscope
    except:
        schedule.part_quantity = 0
    schedule.part_location = request.cookies.get('location').upper()  # Auto
    schedule.entry_time = dt.strftime("%H:%M:%S")  # Auto
    schedule.entry_date = datetime.date.today()  # Auto
    schedule.comments = form.comments.data.upper()  # Manual
    schedule.revision = form.revision.data.upper()  # Manual
    schedule.machine_center = schedule.get_machine_center()  # schedule.get_machine_center()  # Manual
    schedule.original_estimated_time = form.original_estimated_time.data.upper()  # Time Estimate ( Manual )
    schedule.quantity_complete = form.quantity_complete.data  # Manual

    qry = db_session()
    qry.add(schedule)
    qry.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, threaded=True, debug=True)
