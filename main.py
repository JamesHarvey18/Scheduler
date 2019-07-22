from app import app
import db_creator
from db_setup import init_db, db_session
from forms import SchedulerDataEntryForm, LocationForm
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
            flash('Scan barcode from work order and include finish date.')

        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route('/schedules/master', methods=['GET', 'POST'])
def master():
    qry = db_session.query(Schedule)  #  .group_by(Schedule.job_number).group_by(Schedule.work_number)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = User()
    if request.method == 'POST':
        user.password = request.form['pass']
        user.username = request.form['email']
        if user.verify():
            session['logged_in'] = True
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            flash('Incorrect Password.')
    return render_template('login.html')


@app.route('/schedules/CNCP', methods=['GET', 'POST'])
def cncp():
    qry = db_session.query(Schedule) .filter(Schedule.machine_center == 'CNCP')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/LASR', methods=['GET', 'POST'])
def lasr():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'LASR')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/MNUL', methods=['GET', 'POST'])
def mnul():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'MNUL')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/MS', methods=['GET', 'POST'])
def ms():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'MS')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/MSO', methods=['GET', 'POST'])
def mso():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'MSO')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/NLLG', methods=['GET', 'POST'])
def nllg():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'NLLG')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/NLMD', methods=['GET', 'POST'])
def nlmd():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'NLMD')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/NMLG', methods=['GET', 'POST'])
def nmlg():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'NMLG')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/NMSM', methods=['GET', 'POST'])
def nmsm():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'NMSM')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/PNT', methods=['GET', 'POST'])
def pnt():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'PNT')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/SAWS', methods=['GET', 'POST'])
def saws():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'SAWS')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/SMBK', methods=['GET', 'POST'])
def smbk():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'SMBK')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/SMPC', methods=['GET', 'POST'])
def smpc():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'SMPC')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/WELD', methods=['GET', 'POST'])
def weld():
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'WELD')# .filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules', methods=['GET', 'POST'])
def schedules():
    return render_template('schedules.html')


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Schedule).filter(Schedule.id == id)
    entry = qry.first()

    if entry:
        form = SchedulerDataEntryForm(formdata=request.form, obj=entry)
        if request.method == 'POST':
            edit_entry(form, entry)
            flash('Schedule updated successfully')
            return redirect('/schedules/master')
        return render_template('edit.html', form=form)
    else:
        return 'Error loading #{id}. Please report this issue.'.format(id=id)


@app.route('/work_order/<int:wo>', methods=['GET', 'POST'])
def group(wo):
    qry = db_session.query(Schedule).filter(Schedule.work_number == '0001')
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


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
            return redirect('/')
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
    return datetime.date(year, month, day)


def edit_entry(form, schedule):
    schedule.due_date = preprocess_date(form.due_date.data)  # Manual
    schedule.comments = form.comments.data.upper()  # Manual
    schedule.revision = form.revision.data.upper()  # Manual
    schedule.original_estimated_time = form.original_estimated_time.data.upper()  # Time Estimate ( Manual )
    schedule.quantity_complete = form.quantity_complete.data  # Manual
    schedule.priority = request.form['priority']
    schedule.material_status = request.form['material_status'].upper()

    qry = db_session()
    qry.add(schedule)
    qry.commit()


def save_changes(form):
    schedule = Schedule()
    dt = datetime.datetime.now()
    barcode = form.part_number.data

    schedule.due_date = preprocess_date(form.due_date.data)  # Manual
    schedule.job_number = schedule.get_job_number(barcode).upper()  # Manual
    schedule.work_number = schedule.get_work_order(barcode)  # Manual
    schedule.part_number = schedule.get_part_number()
    schedule.part_description = schedule.get_description()  # Jobscope

    try:
        schedule.part_quantity = schedule.get_quantity()  # Jobscope
    except Exception as e:
        print(str(e))
        schedule.part_quantity = 0

    schedule.part_location = request.cookies.get('location').upper()  # Auto
    schedule.entry_time = dt.strftime("%H:%M:%S")  # Auto
    schedule.entry_date = datetime.date.today()  # Auto
    schedule.comments = form.comments.data.upper()  # Manual
    if form.revision.data == '':
        schedule.revision = schedule.get_revision().upper()
    else:
        schedule.revision = form.revision.data.upper()  # Manual
    schedule.machine_center = schedule.get_machine_center()  # schedule.get_machine_center()  # Manual
    schedule.original_estimated_time = form.original_estimated_time.data.upper()  # Time Estimate ( Manual )
    schedule.quantity_complete = form.quantity_complete.data  # Manual
    schedule.actual_time = schedule.get_actual_time() # Jobscope
    schedule.priority = request.form['priority']
    schedule.material_status = request.form['status'].upper()
    if request.cookies.get('location') == 'QUALITY CONTROL':
        schedule.archived = 1
        for s in db_session.query(Schedule).filter(Schedule.part_number == schedule.part_number).all():
            s.archived = 1
        db_session.commit()
    else:
        schedule.archived = 0
    schedule.finish = request.form['finish']

    qry = db_session()
    qry.add(schedule)
    qry.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, threaded=True, debug=True)
