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
    due_date = StringField('Finish Date *')
    employee_id = StringField('Employee')
    part_number = StringField('Barcode *')
    comments = TextAreaField('Notes', render_kw={"rows": 1, "cols": 20})
    revision = StringField('Revision')
    original_estimated_time = StringField('Time Estimate')
    quantity_complete = StringField('Quantity Complete')
    priority = StringField('Priority')
    material_status = StringField('Material Status')
    finish = StringField('Finish')
    work_center = SelectField(choices=[('NONE', 'NONE'), ('CNCP', 'CNC Programming'), ('LASR', 'Laser Etching'), ('MNUL', 'Manual Machining'), ('MS', 'Machine Shop Gen.'),
                                       ('MSO', 'Machine Shop Office'), ('NLLG', 'CNC Lathe - Large'), ('NLMD', 'CNC Lathe - Small/Med.'), ('NMLG', 'CNC Mill - Large'),
                                       ('NMSM', 'CNC Mill - Small/Med.'), ('PNT', 'Powder Coating'), ('SAWS', 'All Saws'), ('SMBK', 'Sheet Metal Brake'),
                                       ('SMPC', 'Sheet Metal Punch'), ('WELD', 'Welding')])


class LocationForm(Form):
    location = StringField("Location")


class PasswordForm(Form):
    password = PasswordField('Password')

