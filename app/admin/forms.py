# Forms for admin blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, DecimalField
from wtforms_components import TimeField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Freshman

class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    date = DateField('Date: M/D/YYYY (ie. 9/16/2020)', format='%m/%d/%Y', validators=[DataRequired()])
    start_at = TimeField('Start at',validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    fsp = DecimalField('FSP: Range (0.00 to 9.99)', validators=[DataRequired()])
    numPeople = IntegerField('# People', validators=[DataRequired()])

    submit = SubmitField('Submit')

class AssociatesForm(FlaskForm):
    """
    Form for admin to add or edit a associates job
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    date = DateField('Date: M/D/YYYY (ie. 9/16/2020)', format='%m/%d/%Y', validators=[DataRequired()])
    start_at = TimeField('Start at',validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    fsp = DecimalField('FSP: Please enter in decimal form (ie. 1 is 1.0)', validators=[DataRequired()])
    numPeople = IntegerField('# People', validators=[DataRequired()])

    submit = SubmitField('Submit')

class BikeForm(FlaskForm):
    """
    Form for admin to add or edit a bike job
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    date = DateField('Date: M/D/YYYY (ie. 9/16/2020)', format='%m/%d/%Y', validators=[DataRequired()])
    start_at = TimeField('Start at',validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    fsp = DecimalField('FSP: Please enter in decimal form (ie. 1 is 1.0)', validators=[DataRequired()])
    numPeople = IntegerField('# People', validators=[DataRequired()])

    submit = SubmitField('Submit')

class CulArtForm(FlaskForm):
    """
    Form for admin to add or edit a culart job
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    date = DateField('Date: M/D/YYYY (ie. 09/16/2020)', format='%m/%d/%Y', validators=[DataRequired()])
    start_at = TimeField('Start at',validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    fsp = DecimalField('FSP: Please enter in decimal form (ie. 1 is 1.0)', validators=[DataRequired()])
    numPeople = IntegerField('# People', validators=[DataRequired()])

    submit = SubmitField('Submit')

class MerchForm(FlaskForm):
    """
    Form for admin to add or edit a merch job
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    date = DateField('Date: M/D/YYYY (ie. 09/16/2020)', format='%m/%d/%Y', validators=[DataRequired()])
    start_at = TimeField('Start at',validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    fsp = DecimalField('FSP: Please enter in decimal form (ie. 1 is 1.0)', validators=[DataRequired()])
    numPeople = IntegerField('# People', validators=[DataRequired()])

    submit = SubmitField('Submit')

class SocialsForm(FlaskForm):
    """
    Form for admin to add or edit a socials job
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    date = DateField('Date: M/D/YYYY (ie. 09/16/2020)', format='%m/%d/%Y', validators=[DataRequired()])
    start_at = TimeField('Start at',validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    fsp = DecimalField('FSP: Please enter in decimal form (ie. 1 is 1.0)', validators=[DataRequired()])
    numPeople = IntegerField('# People', validators=[DataRequired()])

    submit = SubmitField('Submit')

class SpiritForm(FlaskForm):
    """
    Form for admin to add or edit a spirit job
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    date = DateField('Date: M/D/YYYY (ie. 09/16/2020)', format='%m/%d/%Y', validators=[DataRequired()])
    start_at = TimeField('Start at',validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    fsp = DecimalField('FSP: Please enter in decimal form (ie. 1 is 1.0)', validators=[DataRequired()])
    numPeople = IntegerField('# People', validators=[DataRequired()])

    submit = SubmitField('Submit')

class SlushForm(FlaskForm):
    """
    Form for admin to add or edit a slush job
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    date = DateField('Date: M/D/YYYY (ie. 09/16/2020)', format='%m/%d/%Y', validators=[DataRequired()])
    start_at = TimeField('Start at',validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    fsp = DecimalField('FSP: Please enter in decimal form (ie. 1 is 1.0)', validators=[DataRequired()])
    numPeople = IntegerField('# People', validators=[DataRequired()])

    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

class FreshmanForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    netID = StringField('NetID', validators=[DataRequired()])
    submit = SubmitField('Submit')