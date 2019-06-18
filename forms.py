from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField

"""
File for all of the classes of forms that are used on the website front end.
Any page that you make that involves data entry should have its own dedicated
form (if none of them can be reused for your specific task.) Data that is
entered into these forms can be accessed by backend code by creating a form object
and setting a variable to form.[form's variable name].data. Each class includes
all variables you will need to enter into a textbox.
"""


class SchedulerDataEntryForm(Form):
    due_date = StringField('Finish Date')
    part_quantity = StringField('Part Quantity')
    job_number = StringField('Job Number')
    work_number = StringField('Work Order #')
    employee_id = StringField('Employee')
    part_number = StringField('Scan Part Barcode')
    comments = TextAreaField('Notes', render_kw={"rows": 1, "cols": 20})
    revision = StringField('Revision')
    material_status = StringField('Material Status')
    machine_center = SelectField(
        'Machine Center',
        choices=[('QRTZ', 'QRTZ'), ('ALEC', 'ALEC'), ('WELD', 'WELD'), ('MSQC', 'MSQC'), ('MLU', 'MLU')]
    )
    original_estimated_time = StringField('Time Estimate')
    actual_time = StringField('Actual Time')
    quantity_complete = StringField('Quantity Complete')


class LocationForm(Form):
    location = StringField("Location")


class RegistrationForm(Form):
    username = StringField("Username")
    email = StringField("Email")
    password = StringField("Password")


class PasswordForm(Form):
    password = PasswordField('Password')


class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")
