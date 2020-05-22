# Views for admin blueprint

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import DepartmentForm, AssociatesForm, BikeForm, CulArtForm, MerchForm, SpiritForm, SocialsForm, SlushForm, RoleForm, FreshmanForm
from .. import db
from ..models import Department, Associates, Bike, CulArt, Merch, Spirit, Socials, Slush, Employee, Freshman


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data,
                                start=form.start_at.data,
                                end=form.end_at.data,
                                fsp=form.fsp.data,
                                numPeople=form.numPeople.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        department.date = form.date.data
        department.start = form.start_at.data
        department.end = form.end_at.data
        department.fsp = form.fsp.data
        department.numPeople = form.numPeople.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.name.data = department.name
    form.description.data = department.description
    department.date = form.date.data
    department.start = form.start_at.data
    department.end = form.end_at.data
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")

# Associates Views

@admin.route('/associates', methods=['GET', 'POST'])
@login_required
def list_associates():
    """
    List all associates jobs
    """
    check_admin()

    associates = Associates.query.all()

    return render_template('admin/associates/associates.html',
                           associates=associates, title="Associates Jobs")

@admin.route('/associates/add', methods=['GET', 'POST'])
@login_required
def add_associate():
    """
    Add a associates job to the database
    """
    check_admin()

    add_associate = True

    form = AssociatesForm()
    if form.validate_on_submit():
        associate = Associates(name=form.name.data,
                                description=form.description.data,
                                date=form.date.data,
                                start=form.start_at.data,
                                end=form.end_at.data,
                                fsp=form.fsp.data,
                                numPeople=form.numPeople.data)
        try:
            # add associates job to the database
            db.session.add(associate)
            db.session.commit()
            flash('You have successfully added a new Associates Job.')
        except:
            # in case associates job name already exists
            flash('Error: this Associates Job already exists.')

        # redirect to associates job page
        return redirect(url_for('admin.list_associates'))

    # load associates template
    return render_template('admin/associates/associate.html', action="Add",
                           add_associate=add_associate, form=form,
                           title="Add Associates Job")

@admin.route('/associates/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_associate(id):
    """
    Edit a associates job
    """
    check_admin()

    add_associate = False

    associate = Associates.query.get_or_404(id)
    form = AssociatesForm(obj=associate)
    if form.validate_on_submit():
        associate.name = form.name.data
        associate.description = form.description.data
        associate.date = form.date.data
        associate.start = form.start_at.data
        associate.end = form.end_at.data
        associate.fsp = form.fsp.data
        associate.numPeople = form.numPeople.data
        db.session.commit()
        flash('You have successfully edited the Associates Job.')

        # redirect to the associates job page
        return redirect(url_for('admin.list_associates'))

    form.name.data = associate.name
    form.description.data = associate.description

    associate.date = form.date.data
    associate.start = form.start_at.data
    associate.end = form.end_at.data
    return render_template('admin/associates/associate.html', action="Edit",
                           add_associate=add_associate, form=form,
                           associate=associate, title="Edit Associates Job")

@admin.route('/associates/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_associate(id):
    """
    Delete a associate job from the database
    """
    check_admin()

    associate = Associates.query.get_or_404(id)
    db.session.delete(associate)
    db.session.commit()
    flash('You have successfully deleted the Associates job.')

    # redirect to the associate job page
    return redirect(url_for('admin.list_associates'))

    return render_template(title="Delete Associates Job")

# Bike Views

@admin.route('/bike', methods=['GET', 'POST'])
@login_required
def list_bikes():
    """
    List all bike jobs
    """
    check_admin()

    bikes = Bike.query.all()

    return render_template('admin/bikes/bikes.html',
                           bikes=bikes, title="Beer Bike Jobs")

@admin.route('/bike/add', methods=['GET', 'POST'])
@login_required
def add_bike():
    """
    Add a bikes job to the database
    """
    check_admin()

    add_bike = True

    form = BikeForm()
    if form.validate_on_submit():
        bike = Bike(name=form.name.data,
                                description=form.description.data,
                                date=form.date.data,
                                start=form.start_at.data,
                                end=form.end_at.data,
                                fsp=form.fsp.data,
                                numPeople=form.numPeople.data)
        try:
            # add bikes job to the database
            db.session.add(bike)
            db.session.commit()
            flash('You have successfully added a new Beer Bike Job.')
        except:
            # in case bikes job name already exists
            flash('Error: this Beer Bike Job already exists.')

        # redirect to bikes job page
        return redirect(url_for('admin.list_bikes'))

    # load bikes template
    return render_template('admin/bikes/bike.html', action="Add",
                           add_bike=add_bike, form=form,
                           title="Add Beer Bike Job")

@admin.route('/bike/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_bike(id):
    """
    Edit a bikes
    """
    check_admin()

    add_bike = False

    bike = Bike.query.get_or_404(id)
    form = BikeForm(obj=bike)
    if form.validate_on_submit():
        bike.name = form.name.data
        bike.description = form.description.data
        bike.date = form.date.data
        bike.start = form.start_at.data
        bike.end = form.end_at.data
        bike.fsp = form.fsp.data
        bike.numPeople = form.numPeople.data
        db.session.commit()
        flash('You have successfully edited the Beer Bike Job.')

        # redirect to the bikes job page
        return redirect(url_for('admin.list_bikes'))

    form.name.data = bike.name
    form.description.data = bike.description

    bike.date = form.date.data
    bike.start = form.start_at.data
    bike.end = form.end_at.data
    return render_template('admin/bikes/bike.html', action="Edit",
                           add_bike=add_bike, form=form,
                           bike=bike, title="Edit Beer Bike Job")

@admin.route('/bike/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_bike(id):
    """
    Delete a bikes job from the database
    """
    check_admin()

    bike = Bike.query.get_or_404(id)
    db.session.delete(bike)
    db.session.commit()
    flash('You have successfully deleted the Beer Bike job.')

    # redirect to the bikes job page
    return redirect(url_for('admin.list_bikes'))

    return render_template(title="Delete Beer Bike Job")

# CulArt Views

@admin.route('/culart', methods=['GET', 'POST'])
@login_required
def list_cularts():
    """
    List all culart jobs
    """
    check_admin()

    cularts = CulArt.query.all()

    return render_template('admin/cularts/cularts.html',
                           cularts=cularts, title="C & A Jobs")

@admin.route('/culart/add', methods=['GET', 'POST'])
@login_required
def add_culart():
    """
    Add a cularts job to the database
    """
    check_admin()

    add_culart = True

    form = CulArtForm()
    if form.validate_on_submit():
        culart = CulArt(name=form.name.data,
                                description=form.description.data,
                                date=form.date.data,
                                start=form.start_at.data,
                                end=form.end_at.data,
                                fsp=form.fsp.data,
                                numPeople=form.numPeople.data)
        try:
            # add culart job to the database
            db.session.add(culart)
            db.session.commit()
            flash('You have successfully added a new C & A Job.')
        except:
            # in case culart job name already exists
            flash('Error: this C & A Job already exists.')

        # redirect to culart job page
        return redirect(url_for('admin.list_cularts'))

    # load culart template
    return render_template('admin/cularts/culart.html', action="Add",
                           add_culart=add_culart, form=form,
                           title="Add C & A Job")

@admin.route('/culart/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_culart(id):
    """
    Edit a cularts
    """
    check_admin()

    add_culart = False

    culart = CulArt.query.get_or_404(id)
    form = CulArtForm(obj=culart)
    if form.validate_on_submit():
        culart.name = form.name.data
        culart.description = form.description.data
        culart.date = form.date.data
        culart.start = form.start_at.data
        culart.end = form.end_at.data
        culart.fsp = form.fsp.data
        culart.numPeople = form.numPeople.data
        db.session.commit()
        flash('You have successfully edited the C & A Job.')

        # redirect to the culart job page
        return redirect(url_for('admin.list_cularts'))

    form.name.data = culart.name
    form.description.data = culart.description

    culart.date = form.date.data
    culart.start = form.start_at.data
    culart.end = form.end_at.data
    return render_template('admin/cularts/culart.html', action="Edit",
                           add_culart=add_culart, form=form,
                           culart=culart, title="Edit C & A Job")

@admin.route('/culart/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_culart(id):
    """
    Delete a cularts job from the database
    """
    check_admin()

    culart = CulArt.query.get_or_404(id)
    db.session.delete(culart)
    db.session.commit()
    flash('You have successfully deleted the C & A job.')

    # redirect to the culart job page
    return redirect(url_for('admin.list_cularts'))

    return render_template(title="Delete C & A Job")

# Merch Views

@admin.route('/merch', methods=['GET', 'POST'])
@login_required
def list_merch():
    """
    List all merch jobs
    """
    check_admin()

    merchs = Merch.query.all()

    return render_template('admin/merchs/merchs.html',
                           merchs=merchs, title="Merch Jobs")

@admin.route('/merch/add', methods=['GET', 'POST'])
@login_required
def add_merch():
    """
    Add a merch job to the database
    """
    check_admin()

    add_merch = True

    form = MerchForm()
    if form.validate_on_submit():
        merch = Merch(name=form.name.data,
                                description=form.description.data,
                                date=form.date.data,
                                start=form.start_at.data,
                                end=form.end_at.data,
                                fsp=form.fsp.data,
                                numPeople=form.numPeople.data)
        try:
            # add merch job to the database
            db.session.add(merch)
            db.session.commit()
            flash('You have successfully added a new Merch Job.')
        except:
            # in case merch job name already exists
            flash('Error: this Merch Job already exists.')

        # redirect to merch job page
        return redirect(url_for('admin.list_merch'))

    # load merch template
    return render_template('admin/merchs/merch.html', action="Add",
                           add_merch=add_merch, form=form,
                           title="Add Merch Job")

@admin.route('/merch/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_merch(id):
    """
    Edit a merch
    """
    check_admin()

    add_merch = False

    merch = Merch.query.get_or_404(id)
    form = MerchForm(obj=merch)
    if form.validate_on_submit():
        merch.name = form.name.data
        merch.description = form.description.data
        merch.date = form.date.data
        merch.start = form.start_at.data
        merch.end = form.end_at.data
        merch.fsp = form.fsp.data
        merch.numPeople = form.numPeople.data
        db.session.commit()
        flash('You have successfully edited the Merch Job.')

        # redirect to the merch job page
        return redirect(url_for('admin.list_merch'))

    form.name.data = merch.name
    form.description.data = merch.description

    merch.date = form.date.data
    merch.start = form.start_at.data
    merch.end = form.end_at.data
    return render_template('admin/merchs/merch.html', action="Edit",
                           add_merch=add_merch, form=form,
                           merch=merch, title="Edit Merch Job")

@admin.route('/merch/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_merch(id):
    """
    Delete a merch job from the database
    """
    check_admin()

    merch = Merch.query.get_or_404(id)
    db.session.delete(merch)
    db.session.commit()
    flash('You have successfully deleted the Merch job.')

    # redirect to the merch job page
    return redirect(url_for('admin.list_merch'))

    return render_template(title="Delete Merch Job")

# Spirit Views

@admin.route('/spirit', methods=['GET', 'POST'])
@login_required
def list_spirit():
    """
    List all spirit jobs
    """
    check_admin()

    spirits = Spirit.query.all()

    return render_template('admin/spirits/spirits.html',
                           spirits=spirits, title="Spirit Jobs")

@admin.route('/spirit/add', methods=['GET', 'POST'])
@login_required
def add_spirit():
    """
    Add a spirit job to the database
    """
    check_admin()

    add_spirit = True

    form = SpiritForm()
    if form.validate_on_submit():
        spirit = Spirit(name=form.name.data,
                                description=form.description.data,
                                date=form.date.data,
                                start=form.start_at.data,
                                end=form.end_at.data,
                                fsp=form.fsp.data,
                                numPeople=form.numPeople.data)
        try:
            # add spirit job to the database
            db.session.add(spirit)
            db.session.commit()
            flash('You have successfully added a new Spirit Job.')
        except:
            # in case spirit job name already exists
            flash('Error: this Spirit Job already exists.')

        # redirect to spirit job page
        return redirect(url_for('admin.list_spirit'))

    # load spirit template
    return render_template('admin/spirits/spirit.html', action="Add",
                           add_spirit=add_spirit, form=form,
                           title="Add Spirit Job")

@admin.route('/spirit/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_spirit(id):
    """
    Edit a spirit job
    """
    check_admin()

    add_spirit = False

    spirit = Spirit.query.get_or_404(id)
    form = SpiritForm(obj=spirit)
    if form.validate_on_submit():
        spirit.name = form.name.data
        spirit.description = form.description.data
        spirit.date = form.date.data
        spirit.start = form.start_at.data
        spirit.end = form.end_at.data
        spirit.fsp = form.fsp.data
        spirit.numPeople = form.numPeople.data
        db.session.commit()
        flash('You have successfully edited the Spirit Job.')

        # redirect to the spirit job page
        return redirect(url_for('admin.list_spirit'))

    form.name.data = spirit.name
    form.description.data = spirit.description

    spirit.date = form.date.data
    spirit.start = form.start_at.data
    spirit.end = form.end_at.data
    return render_template('admin/spirits/spirit.html', action="Edit",
                           add_spirit=add_spirit, form=form,
                           spirit=spirit, title="Edit Spirit Job")

@admin.route('/spirit/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_spirit(id):
    """
    Delete a spirit job from the database
    """
    check_admin()

    spirit = Spirit.query.get_or_404(id)
    db.session.delete(spirit)
    db.session.commit()
    flash('You have successfully deleted the Spirit job.')

    # redirect to the spirit job page
    return redirect(url_for('admin.list_spirit'))

    return render_template(title="Delete Spirit Job")

# Socials Views

@admin.route('/socials', methods=['GET', 'POST'])
@login_required
def list_socials():
    """
    List all socials jobs
    """
    check_admin()

    socials = Socials.query.all()

    return render_template('admin/socials/socials.html',
                           socials=socials, title="Socials Jobs")

@admin.route('/socials/add', methods=['GET', 'POST'])
@login_required
def add_social():
    """
    Add a socials job to the database
    """
    check_admin()

    add_social = True

    form = SocialsForm()
    if form.validate_on_submit():
        social = Socials(name=form.name.data,
                                description=form.description.data,
                                date=form.date.data,
                                start=form.start_at.data,
                                end=form.end_at.data,
                                fsp=form.fsp.data,
                                numPeople=form.numPeople.data)
        try:
            # add socials job to the database
            db.session.add(social)
            db.session.commit()
            flash('You have successfully added a new Socials Job.')
        except:
            # in case socials job name already exists
            flash('Error: this Socials Job already exists.')

        # redirect to socials job page
        return redirect(url_for('admin.list_socials'))

    # load socials template
    return render_template('admin/socials/social.html', action="Add",
                           add_social=add_social, form=form,
                           title="Add Socials Job")

@admin.route('/socials/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_social(id):
    """
    Edit a socials
    """
    check_admin()

    add_social = False

    social = Socials.query.get_or_404(id)
    form = SocialsForm(obj=social)
    if form.validate_on_submit():
        social.name = form.name.data
        social.description = form.description.data
        social.date = form.date.data
        social.start = form.start_at.data
        social.end = form.end_at.data
        social.fsp = form.fsp.data
        social.numPeople = form.numPeople.data
        db.session.commit()
        flash('You have successfully edited the Socials Job.')

        # redirect to the socials job page
        return redirect(url_for('admin.list_socials'))

    form.name.data = social.name
    form.description.data = social.description

    social.date = form.date.data
    social.start = form.start_at.data
    social.end = form.end_at.data
    return render_template('admin/socials/social.html', action="Edit",
                           add_social=add_social, form=form,
                           social=social, title="Edit Socials Job")

@admin.route('/socials/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_social(id):
    """
    Delete a socials job from the database
    """
    check_admin()

    social = Socials.query.get_or_404(id)
    db.session.delete(social)
    db.session.commit()
    flash('You have successfully deleted the Socials job.')

    # redirect to the socials job page
    return redirect(url_for('admin.list_socials'))

    return render_template(title="Delete Socials Job")

# Slush Views

@admin.route('/slush', methods=['GET', 'POST'])
@login_required
def list_slush():
    """
    List all slush jobs
    """
    check_admin()

    slushs = Slush.query.all()

    return render_template('admin/slushs/slushs.html',
                           slushs=slushs, title="Slush Jobs")

@admin.route('/slush/add', methods=['GET', 'POST'])
@login_required
def add_slush():
    """
    Add a slush job to the database
    """
    check_admin()

    add_slush = True

    form = SlushForm()
    if form.validate_on_submit():
        slush = Slush(name=form.name.data,
                                description=form.description.data,
                                date=form.date.data,
                                start=form.start_at.data,
                                end=form.end_at.data,
                                fsp=form.fsp.data,
                                numPeople=form.numPeople.data)
        try:
            # add slush job to the database
            db.session.add(slush)
            db.session.commit()
            flash('You have successfully added a new Slush Job.')
        except:
            # in case slush job name already exists
            flash('Error: this Slush Job already exists.')

        # redirect to slush job page
        return redirect(url_for('admin.list_slush'))

    # load slush template
    return render_template('admin/slushs/slush.html', action="Add",
                           add_slush=add_slush, form=form,
                           title="Add Slush Job")

@admin.route('/slush/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_slush(id):
    """
    Edit a slush
    """
    check_admin()

    add_slush = False

    slush = Slush.query.get_or_404(id)
    form = SlushForm(obj=slush)
    if form.validate_on_submit():
        slush.name = form.name.data
        slush.description = form.description.data
        slush.date = form.date.data
        slush.start = form.start_at.data
        slush.end = form.end_at.data
        slush.fsp = form.fsp.data
        slush.numPeople = form.numPeople.data
        db.session.commit()
        flash('You have successfully edited the Slush Job.')

        # redirect to the slush job page
        return redirect(url_for('admin.list_slush'))

    form.name.data = slush.name
    form.description.data = slush.description

    slush.date = form.date.data
    slush.start = form.start_at.data
    slush.end = form.end_at.data
    return render_template('admin/slushs/slush.html', action="Edit",
                           add_slush=add_slush, form=form,
                           slush=slush, title="Edit Slush Job")

@admin.route('/slush/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_slush(id):
    """
    Delete a slush job from the database
    """
    check_admin()

    slush = Slush.query.get_or_404(id)
    db.session.delete(slush)
    db.session.commit()
    flash('You have successfully deleted the Slush job.')

    # redirect to the slush job page
    return redirect(url_for('admin.list_slush'))

    return render_template(title="Delete Slush Job")

# Role Views

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

# Freshman Views

@admin.route('/freshmans', methods=['GET', 'POST'])
@login_required
def list_freshmans():
    """
    List all departments
    """
    check_admin()

    freshmans = Freshman.query.all()

    return render_template('admin/freshmans/freshmans.html',
                           freshman=freshmans, title="Freshmans")

@admin.route('/freshmans/add', methods=['GET', 'POST'])
@login_required
def add_freshman():
    """
    Add a department to the database
    """
    check_admin()

    add_freshman = True

    form = FreshmanForm()
    if form.validate_on_submit():
        freshman = Freshman(name=form.name.data,
                                netID=form.netID.data)
        try:
            # add department to the database
            db.session.add(freshman)
            db.session.commit()
            flash('You have successfully added a new freshman.')
        except:
            # in case department name already exists
            flash('Error: freshman name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_freshmans'))

    # load department template
    return render_template('admin/freshmans/freshman.html', action="Add",
                           add_freshman=add_freshman, form=form,
                           title="Add Freshman")

@admin.route('/freshmans/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_freshman(id):
    """
    Edit a department
    """
    check_admin()

    add_freshman = False

    freshman = Freshman.query.get_or_404(id)
    form = FreshmanForm(obj=freshman)
    if form.validate_on_submit():
        freshman.name = form.name.data
        freshman.netID = form.netID.data
        db.session.commit()
        flash('You have successfully edited the freshman.')

        # redirect to the departments page
        return redirect(url_for('admin.list_freshmans'))

    form.netID.data = freshman.netID
    form.name.data = freshman.name
    return render_template('admin/freshmans/freshman.html', action="Edit",
                           add_freshman=add_freshman, form=form,
                           freshman=freshman, title="Edit Freshman")

@admin.route('/freshmans/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_freshman(id):
    """
    Delete a department from the database
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    db.session.delete(freshman)
    db.session.commit()
    flash('You have successfully deleted the freshman.')

    # redirect to the departments page
    return redirect(url_for('admin.list_freshmans'))

    return render_template(title="Delete freshman")

# Employees Views

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


# @admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
# @login_required
# def assign_employee(id):
#     """
#     Assign a department and a role to an employee
#     """
#     check_admin()

#     employee = Employee.query.get_or_404(id)

#     # prevent admin from being assigned a department or role
#     if employee.is_admin:
#         abort(403)

#     form = EmployeeAssignForm(obj=employee)
#     if form.validate_on_submit():
#         employee.department = form.department.data
#         employee.role = form.role.data
#         db.session.add(employee)
#         db.session.commit()
#         flash('You have successfully assigned a department and role.')

#         # redirect to the roles page
#         return redirect(url_for('admin.list_employees'))

#     return render_template('admin/employees/employee.html',
#                            employee=employee, form=form,
#                            title='Assign Employee')


