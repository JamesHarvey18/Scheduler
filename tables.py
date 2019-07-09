from flask_table import Table, Col, LinkCol
from flask import url_for

"""
File for the shape of the tables that can be returned as results of searching
the database. Make a variable for each column you want to appear, set to the
Col('Column Name'). Function included is for potentially sorting the table
live. Unused currently. Also removes warning for abstract methods.
"""


class Results(Table):
    work_number = Col('WO')
    job_number = Col('Job #')
    part_number = Col('Part Number')
    revision = Col('Rev.')
    part_quantity = Col('Qty.')
    quantity_complete = Col('QCP')
    part_description = Col('Description')
    part_location = Col('Location')
    due_date = Col('Due Date')
    entry_date = Col('Scanned')
    entry_time = Col('Time')
    material_status = Col('Material Status')
    machine_center = Col('Center')
    original_estimated_time = Col('Time Est.')
    actual_time = Col('Actual Time')
    comments = Col('Notes')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))

    def sort_url(self, col_id, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_id, direction=direction)
