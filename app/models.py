from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    # department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Freshman(db.Model):
    """
    Create an Freshman table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'freshman'

    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(60), index=True, unique=True)
    # username = db.Column(db.String(60), index=True, unique=True)
    # first_name = db.Column(db.String(60), index=True)
    # last_name = db.Column(db.String(60), index=True)
    name = db.Column(db.String(60), unique=True)
    netID = db.Column(db.String(10))
    fsp = db.Column(db.Float)

    def __repr__(self):
        return '<Freshman: {}>'.format(self.email)

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    fsp = db.Column(db.Float)
    numPeople = db.Column(db.Integer)
    # employees = db.relationship('Employee', backref='department',
    #                             lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class Associates(db.Model):
    """
    Create a Associates table
    """

    __tablename__ = 'associates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    fsp = db.Column(db.Numeric(3,2))
    numPeople = db.Column(db.Integer)
    sent = db.Column(db.Boolean)
    employees = db.Column(db.String(200))

    def __repr__(self):
        return '<Associates: {}>'.format(self.name)

class Bike(db.Model):
    """
    Create a Bike table
    """

    __tablename__ = 'bike'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    fsp = db.Column(db.Numeric(3,2))
    numPeople = db.Column(db.Integer)
    sent = db.Column(db.Boolean)
    employees = db.Column(db.String(200))

    def __repr__(self):
        return '<Bike: {}>'.format(self.name)

class CulArt(db.Model):
    """
    Create a CulArt table
    """

    __tablename__ = 'culart'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    fsp = db.Column(db.Numeric(3,2))
    numPeople = db.Column(db.Integer)
    sent = db.Column(db.Boolean)
    employees = db.Column(db.String(200))

    def __repr__(self):
        return '<CulArt: {}>'.format(self.name)

class Merch(db.Model):
    """
    Create a Merch table
    """

    __tablename__ = 'merch'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    fsp = db.Column(db.Numeric(3,2))
    numPeople = db.Column(db.Integer)
    sent = db.Column(db.Boolean)
    employees = db.Column(db.String(200))

    def __repr__(self):
        return '<Merch: {}>'.format(self.name)

class Spirit(db.Model):
    """
    Create a Spirit table
    """

    __tablename__ = 'spirit'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    fsp = db.Column(db.Numeric(3,2))
    numPeople = db.Column(db.Integer)
    sent = db.Column(db.Boolean)
    employees = db.Column(db.String(200))

    def __repr__(self):
        return '<Spirit: {}>'.format(self.name)

class Socials(db.Model):
    """
    Create a Socials table
    """

    __tablename__ = 'socials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    fsp = db.Column(db.Numeric(3,2))
    numPeople = db.Column(db.Integer)
    sent = db.Column(db.Boolean)
    employees = db.Column(db.String(200))

    def __repr__(self):
        return '<Socials: {}>'.format(self.name)

class Slush(db.Model):
    """
    Create a Slush table
    """

    __tablename__ = 'slush'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    fsp = db.Column(db.Numeric(3,2))
    numPeople = db.Column(db.Integer)
    sent = db.Column(db.Boolean)
    employees = db.Column(db.String(200))

    def __repr__(self):
        return '<Slush: {}>'.format(self.name)

class Done(db.Model):
    """
    Create a Done table for completed jobs
    """

    __tablename__ = 'done'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    fsp = db.Column(db.Numeric(3,2))
    numPeople = db.Column(db.Integer)
    student = db.Column(db.String(60))
    sid = db.Column(db.String(60))
    department = db.Column(db.String(60))
    points_given = db.Column(db.Boolean)

    def __repr__(self):
        return '<Done: {}>'.format(self.name)


