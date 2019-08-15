from app import app
import db_creator
from db_setup import init_db, db_session
from forms import SchedulerDataEntryForm, LocationForm
from flask import Flask, flash, render_template, redirect, url_for, request, session, make_response
from models import Schedule, User, Password
from tables import Results, ReadOnly, Archived, ReadEdit
import datetime
from functools import wraps
from validate_email import validate_email
import sqlite3
import re

init_db()
referrers = []  # Global list to contain referral urls when editing so the user can return to the same page they were on.


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
    location = request.cookies.get('location')

    if not location:
        flash("Enter your location.")
        return redirect(url_for('add_location'))

    form = SchedulerDataEntryForm(request.form)

    if request.method == 'POST':
        ''' Scanning at QC removing disabled because process was not defined.
        if (location == 'QUALITY CONTROL' or location == 'QC') and :
            try:
                archive(form)
            except Exception as e:
                flash('error: ' + str(e))
        else:
        '''
        try:
            schedule = Schedule()
            schedule.save_changes(form)

            if schedule.is_duplicate():
                flash('The entry you made was a duplicate')
        except Exception as e:
            flash('Scan barcode from work order and include finish date. ' + str(e))

        return redirect(url_for('index'))
    return render_template('index.html', form=form)


def selectTableType(qry):
    if session['level'] == 'Admin':
        return Results(qry)
    elif session['level'] == 'Editor':
        return ReadEdit(qry)
    else:
        return ReadOnly(qry)


@app.route('/schedules/master_read_only', methods=['GET', 'POST'])
def read_only():
    qry = db_session.query(Schedule).filter(Schedule.archived == 0)
    table = ReadOnly(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/master_read_edit', methods=['GET', 'POST'])
def read_edit():
    qry = db_session.query(Schedule).filter(Schedule.archived == 0)
    table = ReadEdit(qry)
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
            user.set_permission_level()
            return redirect(url_for('index'))
        else:
            flash('Incorrect Password.')
    return render_template('login.html')


def home_redirect():
    if session['level'] != 'Admin':
        flash('You must have admin privileges to add to the schedule')
        return redirect(url_for('schedules'))


def edit_redirect():
    if session['level'] != 'Editor' and session['level'] != 'Admin':
        flash('You must have admin or edit privileges to edit the schedule')
        return redirect(url_for('schedules'))


''' All schedule routes '''


@app.route('/schedules/master', methods=['GET', 'POST'])
def master():
    flash('Master Schedule')
    qry = db_session.query(Schedule).filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/archived', methods=['GET', 'POST'])
def archived():
    flash('Archived')
    qry = db_session.query(Schedule).filter(Schedule.archived == 1)
    table = Archived(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/CNCP', methods=['GET', 'POST'])
def cncp():
    flash('CNCP')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'CNCP').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/LASR', methods=['GET', 'POST'])
def lasr():
    flash('LASR')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'LASR').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/MNUL', methods=['GET', 'POST'])
def mnul():
    flash('MNUL')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'MNUL').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/MS', methods=['GET', 'POST'])
def ms():
    flash('MS')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'MS').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/MSO', methods=['GET', 'POST'])
def mso():
    flash('MSO')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'MSO').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/NLLG', methods=['GET', 'POST'])
def nllg():
    flash('NLLG')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'NLLG').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/NLMD', methods=['GET', 'POST'])
def nlmd():
    flash('NLMD')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'NLMD').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/NMLG', methods=['GET', 'POST'])
def nmlg():
    flash('NMLG')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'NMLG').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/NMSM', methods=['GET', 'POST'])
def nmsm():
    flash('NMSM')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'NMSM').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/PNT', methods=['GET', 'POST'])
def pnt():
    flash('PNT')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'PNT').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/SAWS', methods=['GET', 'POST'])
def saws():
    flash('SAWS')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'SAWS').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/SMBK', methods=['GET', 'POST'])
def smbk():
    flash('SMBK')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'SMBK').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/SMPC', methods=['GET', 'POST'])
def smpc():
    flash('SMPC')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'SMPC').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules/WELD', methods=['GET', 'POST'])
def weld():
    flash('WELD')
    qry = db_session.query(Schedule).filter(Schedule.machine_center == 'WELD').filter(Schedule.archived == 0)
    table = Results(qry)
    table.border = True
    return render_template('search.html', table=table)


@app.route('/schedules', methods=['GET', 'POST'])
def schedules():
    return render_template('schedules.html')


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'schedules' in request.headers.get('Referer'):
        referer = request.headers.get('Referer')
        referrers.clear()
        referrers.append(referer)

    qry = db_session.query(Schedule).filter(Schedule.id == id)
    entry = qry.first()

    form = SchedulerDataEntryForm(formdata=request.form, obj=entry)
    form.work_center.data = entry.machine_center
    flash('Part: ' + entry.part_number)

    if request.method == 'POST':
        schedule = Schedule()
        schedule.edit_entry(form, entry)
        try:
            return redirect(referrers[0])
        except LookupError as e:
            return redirect(url_for('master'))
    return render_template('edit.html', form=form)


@app.route('/location', methods=['GET', 'POST'])
def add_location():
    form = LocationForm(request.form)
    location = form.location.data.upper()
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
    qry = db_session.query(Schedule).filter(Schedule.id == id)
    entry = qry.first()

    if entry:
        if entry.archived == 1:
            entry.delete_permanent()
            return redirect(request.headers.get('Referer'))
        else:
            entry.archive()
            return redirect(request.headers.get('Referer'))
    else:
        return 'ERROR DELETING #{id}'.format(id=id)


@app.route('/mass_delete', methods=['GET', 'POST'])
def mass_delete():
    if request.method == 'POST':
        job = request.form['job'].upper()
        work = request.form['work'].upper()

        if not job and not work:
            sql = ''
            flash('No entry specified.')
        elif job and not work:
            sql = 'UPDATE schedule SET archived = 1 WHERE job_number = "' + job + '"'
        elif job and work:
            sql = 'UPDATE schedule SET archived = 1 WHERE job_number = "' + job + '" AND work_number = "' + '"'
        else:
            sql = ''

        con = sqlite3.connect("scheduler.db")
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()
        return redirect(url_for('mass_delete'))

    return render_template('mass_delete.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    form = SchedulerDataEntryForm(request.form)
    if request.method == 'POST':
        if str(request.form['date']) is not None and str(request.form['date']) != '':
            job = request.form['job'].upper()
            work = request.form['work'].upper()
            work_center = form.work_center.data

            if job == '' and work == '':
                sql = ''
                flash('Enter a valid job number and/or work order.')
            elif job != '' and work == '':
                sql = 'UPDATE schedule ' \
                      'SET due_date = "' + request.form['date'] + '", ' \
                      'quantity_complete = "' + request.form['qty'] + '", ' \
                      'original_estimated_time = "' + request.form['time'] + '", ' \
                      'comments = "' + request.form['notes'].upper() + '", ' \
                      'priority = "' + request.form['priority'] + '", ' \
                      'material_status = "' + request.form['status'].upper() + '", ' \
                      'finish = "' + request.form['finish'].upper() + '", ' \
                      'machine_center = "' + work_center + '" ' \
                      'WHERE job_number = "' + job + '"'
            elif job != '' and work != '':
                sql = 'UPDATE schedule ' \
                      'SET due_date = "' + request.form['date'] + '", ' \
                      'quantity_complete = "' + request.form['qty'] + '", ' \
                      'original_estimated_time = "' + request.form['time'] + '", ' \
                      'comments = "' + request.form['notes'].upper() + '", ' \
                      'priority = "' + request.form['priority'] + '", ' \
                      'material_status = "' + request.form['status'].upper() + '", ' \
                      'finish = "' + request.form['finish'].upper() + '", ' \
                      'machine_center = "' + work_center + '" ' \
                      'WHERE job_number = "' + job + '" AND work_number = "' + work + '"'
            else:
                sql = ''
                flash('Invalid entry')

            con = sqlite3.connect("scheduler.db")
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            con.close()
            return redirect(url_for('update'))
        else:
            flash('Invalid date')

    return render_template('update.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            user = User()
            username = request.form['username']
            email = request.form['email']

            password = request.form['pass']
            confirm_password = request.form['confirm_pass']

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
            user.password = user.hash_password(password)
            qry = db_session()
            qry.add(user)
            qry.commit()

            flash("Registration Successful")
            session['logged_in'] = True
            session['username'] = username
            user.set_permission_level()

            return redirect(url_for('index'))

    except Exception as e:
        return str(e)

    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, threaded=True, debug=True)
