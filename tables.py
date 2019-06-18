from flask_table import Table, Col, LinkCol
from flask import url_for

"""
File for the shape of the tables that can be returned as results of searching
the database. Make a variable for each column you want to appear, set to the
Col('Column Name'). Function included is for potentially sorting the table
live. Unused currently. Also removes warning for abstract methods.
"""


class Results(Table):
    id = Col('ID')
    due_date = Col('Finish Date')
    work_number = Col('Work Order')
    job_number = Col('Job Number')
    part_number = Col('Part Number')
    revision = Col('Revision')
    part_quantity = Col('Quantity')
    part_description = Col('Description')
    part_location = Col('Location')
    entry_date = Col('Date Scanned')
    entry_time = Col('Time Scanned')
    employee_id = Col('Employee')
    comments = Col('Notes')
    material_status = Col('Material Status')
    machine_center = Col('Machine Center')
    original_estimated_time = Col('Time Est.')
    actual_time = Col('Actual Time')
    quantity_complete = Col('Quantity Complete')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))

    def sort_url(self, col_id, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_id, direction=direction)
