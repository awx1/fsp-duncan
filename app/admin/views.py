# Views for admin blueprint

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import DepartmentForm, AssociatesForm, BikeForm, CulArtForm, MerchForm, SpiritForm, SocialsForm, SlushForm, RoleForm, FreshmanForm
from .. import db
from ..models import Department, Associates, Bike, CulArt, Merch, Spirit, Socials, Slush, Employee, Freshman, Done


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
    List all departments jobs
    """
    check_admin()

    departments = Departments.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Department")

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

    for job in associates:
        if (job.employees != None):
            db.session.delete(job)
            db.session.commit()
            freshmans = Freshman.query.all()
    
            employees = str(job.employees)
            assigned_people = employees.split()
            count = False
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        fin_job = Done(name=job.name,
                                        description=job.description,
                                        date=job.date,
                                        start=job.start,
                                        end=job.end,
                                        fsp=job.fsp,
                                        numPeople=job.numPeople,
                                        student=freshman.name,
                                        sid=freshman.id,
                                        department="associates",
                                        points_given=False)
                        try:
                            # add done job to the database
                            db.session.add(fin_job)
                            db.session.commit()
                            if not count:
                                flash('Some Associate Jobs have just been assigned: Please refresh page')
                                count = True
                            # flash('You have successfully added a new assigned Associates Job.')
                        except:
                            # in case done job name already exists
                            flash('Error: this Associates Job already exists in Done.')

    return render_template('admin/associates/associates.html',
                           associates=associates, title="Associates Jobs")

@admin.route('/associates/sentout', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_associate():
    """
    List all associates jobs
    """
    check_admin()

    associates = Associates.query.all()
    sent_but_not_assigned = []
    for job in associates:
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)

    return render_template('admin/associates/associates-sentout.html',
                           done=sent_but_not_assigned, title="Associates Jobs")

@admin.route('/associates/form/1', methods=['GET', 'POST'])
@login_required
def build_form_associate():
    """
    List all associates jobs
    """
    # check_admin()

    # associates = Associates.query.all()
    # not_sent = []
    # for job in associates:
    #     if not job.sent:
    #         sent_but_not_assigned.append(job)

    # form = AssociatesForm()

    # redirect to the associate job page
    return redirect(url_for('admin.list_associates'))

    return render_template(title="Associates Jobs: Form for Jobs Points")

@admin.route('/associates/points', methods=['GET', 'POST'])
@login_required
def points_associate():
    """
    List all associates jobs
    """
    check_admin()

    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        if (str(job.department) == 'associates') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/associates/associates-points.html', done=fin_job,
                            title="Associates Jobs: Assign Points")

@admin.route('/associates/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_associate(id, points):
    """
    Add points for freshman for associates jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp += points
    db.session.commit()
    flash('You have successfully added FSPs for ' + freshman.name + '.')

    # redirect to the associate job page
    return redirect(url_for('admin.points_associate'))

    return render_template(title="Associates Jobs: Added Points")

@admin.route('/associates/points/remove/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def remove_points_associate(id, points):
    """
    Remove points for freshman for associates jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp -= points
    db.session.commit()
    flash('You have successfully removed FSPs for ' + freshman.name + '.')

    # redirect to the associate job page
    return redirect(url_for('admin.points_associate'))

    return render_template(title="Associates Jobs: Removed Points")

@admin.route('/associates/points/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_fin_job_associate(id):
    """
    Remove finished job for associates jobs to store in Done db
    """
    check_admin()

    job = Done.query.get_or_404(id)
    job.points_given = True
    db.session.commit()
    flash('Successfully finished Job: ' + job.name + ' for Student: ' + job.student)

    # redirect to the associate job page
    return redirect(url_for('admin.points_associate'))

    return render_template(title="Associates Jobs")

@admin.route('/associates/add', methods=['GET', 'POST'])
@login_required
def add_associate():
    """
    Add a associates job to the database
    """
    check_admin()

    add_associate = 1

    form = AssociatesForm()
    if form.validate_on_submit():
        associate = Associates(name=form.name.data,
                                description=form.description.data,
                                date=form.date.data,
                                start=form.start_at.data,
                                end=form.end_at.data,
                                fsp=form.fsp.data,
                                numPeople=form.numPeople.data,
                                sent=False)

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

@admin.route('/associates/dup/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicate_associate(id):
    """
    Duplicate an associate job from the database
    """
    check_admin()

    add_associate = 3

    associate = Associates.query.get_or_404(id)

    iter_num = associate.name[-1]
    try:
        iter_num = int(iter_num) + 1
    except:
        iter_num = 1

    if (iter_num > 1):
        name = associate.name[:-1] + str(iter_num)
    else:
        name = associate.name + " " + str(iter_num)
    
    dup_associate = Associates(name=name,
                            description=associate.description,
                            date=associate.date,
                            start=associate.start,
                            end=associate.end,
                            fsp=associate.fsp,
                            numPeople=associate.numPeople,
                            sent=associate.sent)
    
    try:
        # add associates job to the database
        db.session.add(dup_associate)
        db.session.commit()
        flash('You have successfully duplicated the Associates job.')
    except:
        # in case associates job name already exists
        flash('Error: this Associates Job already exists.')

    # redirect to the associate job page
    return redirect(url_for('admin.list_associates'))

    return render_template('admin/associates/associate.html', action="Duplicate",
                           add_associate=add_associate,
                           title="Add Associates Job")

@admin.route('/associates/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_associate(id):
    """
    Edit a associates job
    """
    check_admin()

    add_associate = 2

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

    for job in bikes:
        if (job.employees != None):
            db.session.delete(job)
            db.session.commit()
            freshmans = Freshman.query.all()
    
            employees = str(job.employees)
            assigned_people = employees.split()
            count = False
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        fin_job = Done(name=job.name,
                                        description=job.description,
                                        date=job.date,
                                        start=job.start,
                                        end=job.end,
                                        fsp=job.fsp,
                                        numPeople=job.numPeople,
                                        student=freshman.name,
                                        sid=freshman.id,
                                        department="bike",
                                        points_given=False)
                        try:
                            # add done job to the database
                            db.session.add(fin_job)
                            db.session.commit()
                            if not count:
                                flash('Some Bike Jobs have just been assigned: Please refresh page')
                                count = True
                            # flash('You have successfully added a new assigned Bike Job.')
                        except:
                            # in case done job name already exists
                            flash('Error: this Bike Job already exists in Done.')

    return render_template('admin/bikes/bikes.html',
                           bikes=bikes, title="Beer Bike Jobs")

@admin.route('/bike/form', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_bike():
    """
    List all bike jobs
    """
    check_admin()

    associates = Bike.query.all()
    sent_but_not_assigned = []
    for job in associates:
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)

    return render_template('admin/bikes/bikes-sentout.html',
                           done=sent_but_not_assigned, title="Bike Jobs")

@admin.route('/bike/points', methods=['GET', 'POST'])
@login_required
def points_bike():
    """
    List all bike jobs
    """
    check_admin()

    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        if (str(job.department) == 'bike') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/bikes/bikes-points.html', done=fin_job,
                            title="Bike Jobs: Assign Points")

@admin.route('/bike/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_bike(id, points):
    """
    Add points for freshman for bike jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp += points
    db.session.commit()
    flash('You have successfully added FSPs for ' + freshman.name + '.')

    # redirect to the bike job page
    return redirect(url_for('admin.points_bike'))

    return render_template(title="Bike Jobs: Added Points")

@admin.route('/bike/points/remove/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def remove_points_bike(id, points):
    """
    Remove points for freshman for bike jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp -= points
    db.session.commit()
    flash('You have successfully removed FSPs for ' + freshman.name + '.')

    # redirect to the bike job page
    return redirect(url_for('admin.points_bike'))

    return render_template(title="Bike Jobs: Removed Points")

@admin.route('/bike/points/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_fin_job_bike(id):
    """
    Remove finished job for bike jobs to store in Done db
    """
    check_admin()

    job = Done.query.get_or_404(id)
    job.points_given = True
    db.session.commit()
    flash('Successfully finished Job: ' + job.name + ' for Student: ' + job.student)

    # redirect to the bike job page
    return redirect(url_for('admin.points_bike'))

    return render_template(title="Bike Jobs")

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
                                numPeople=form.numPeople.data,
                                sent=False)
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

@admin.route('/bike/dup/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicate_bike(id):
    """
    Duplicate a bike job from the database
    """
    check_admin()

    add_bike = 3

    bike = Bike.query.get_or_404(id)

    iter_num = bike.name[-1]
    try:
        iter_num = int(iter_num) + 1
    except:
        iter_num = 1

    if (iter_num > 1):
        name = bike.name[:-1] + str(iter_num)
    else:
        name = bike.name + " " + str(iter_num)
    
    dup_bike = Bike(name=name,
                            description=bike.description,
                            date=bike.date,
                            start=bike.start,
                            end=bike.end,
                            fsp=bike.fsp,
                            numPeople=bike.numPeople,
                            sent=bike.sent)
    
    try:
        # add bike job to the database
        db.session.add(dup_bike)
        db.session.commit()
        flash('You have successfully duplicated the Bike job.')
    except:
        # in case bike job name already exists
        flash('Error: this Bike Job already exists.')

    # redirect to the bike job page
    return redirect(url_for('admin.list_bikes'))

    return render_template('admin/bikes/bike.html', action="Duplicate",
                           add_bike=add_bike,
                           title="Add Bike Job")

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

    for job in cularts:
        if (job.employees != None):
            db.session.delete(job)
            db.session.commit()
            freshmans = Freshman.query.all()
    
            employees = str(job.employees)
            assigned_people = employees.split()
            count = False
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        fin_job = Done(name=job.name,
                                        description=job.description,
                                        date=job.date,
                                        start=job.start,
                                        end=job.end,
                                        fsp=job.fsp,
                                        numPeople=job.numPeople,
                                        student=freshman.name,
                                        sid=freshman.id,
                                        department="culart",
                                        points_given=False)
                        try:
                            # add done job to the database
                            db.session.add(fin_job)
                            db.session.commit()
                            if not count:
                                flash('Some C & A Jobs have just been assigned: Please refresh page')
                                count = True
                            # flash('You have successfully added a new assigned C & A Job.')
                        except:
                            # in case done job name already exists
                            flash('Error: this C & A Job already exists in Done.')

    return render_template('admin/cularts/cularts.html',
                           cularts=cularts, title="C & A Jobs")

@admin.route('/culart/form', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_culart():
    """
    List all C & A jobs
    """
    check_admin()

    associates = CulArt.query.all()
    sent_but_not_assigned = []
    for job in associates:
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)

    return render_template('admin/cularts/cularts-sentout.html',
                           done=sent_but_not_assigned, title="C & A Jobs")

@admin.route('/culart/points', methods=['GET', 'POST'])
@login_required
def points_culart():
    """
    List all C & A jobs
    """
    check_admin()

    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        if (str(job.department) == 'culart') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/cularts/cularts-points.html', done=fin_job,
                            title="C & A Jobs: Assign Points")

@admin.route('/culart/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_culart(id, points):
    """
    Add points for freshman for C & A jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp += points
    db.session.commit()
    flash('You have successfully added FSPs for ' + freshman.name + '.')

    # redirect to the C & A job page
    return redirect(url_for('admin.points_culart'))

    return render_template(title="C & A Jobs: Added Points")

@admin.route('/culart/points/remove/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def remove_points_culart(id, points):
    """
    Remove points for freshman for C & A jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp -= points
    db.session.commit()
    flash('You have successfully removed FSPs for ' + freshman.name + '.')

    # redirect to the C & A job page
    return redirect(url_for('admin.points_culart'))

    return render_template(title="C & A Jobs: Removed Points")

@admin.route('/culart/points/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_fin_job_culart(id):
    """
    Remove finished job for C & A jobs to store in Done db
    """
    check_admin()

    job = Done.query.get_or_404(id)
    job.points_given = True
    db.session.commit()
    flash('Successfully finished Job: ' + job.name + ' for Student: ' + job.student)

    # redirect to the C & A job page
    return redirect(url_for('admin.points_bike'))

    return render_template(title="C & A Jobs")

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
                                numPeople=form.numPeople.data,
                                sent=False)
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

@admin.route('/culart/dup/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicate_culart(id):
    """
    Duplicate a culart job from the database
    """
    check_admin()

    add_culart = 3

    culart = CulArt.query.get_or_404(id)

    iter_num = culart.name[-1]
    try:
        iter_num = int(iter_num) + 1
    except:
        iter_num = 1

    if (iter_num > 1):
        name = culart.name[:-1] + str(iter_num)
    else:
        name = culart.name + " " + str(iter_num)
    
    dup_culart = CulArt(name=name,
                            description=culart.description,
                            date=culart.date,
                            start=culart.start,
                            end=culart.end,
                            fsp=culart.fsp,
                            numPeople=culart.numPeople,
                            sent=culart.sent)
    
    try:
        # add culart job to the database
        db.session.add(dup_culart)
        db.session.commit()
        flash('You have successfully duplicated the CulArt job.')
    except:
        # in case culart job name already exists
        flash('Error: this CulArt Job already exists.')

    # redirect to the culart job page
    return redirect(url_for('admin.list_cularts'))

    return render_template('admin/cularts/culart.html', action="Duplicate",
                           add_culart=add_culart,
                           title="Add CulArt Job")

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

    for job in merchs:
        if (job.employees != None):
            db.session.delete(job)
            db.session.commit()
            freshmans = Freshman.query.all()
    
            employees = str(job.employees)
            assigned_people = employees.split()
            count = False
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        fin_job = Done(name=job.name,
                                        description=job.description,
                                        date=job.date,
                                        start=job.start,
                                        end=job.end,
                                        fsp=job.fsp,
                                        numPeople=job.numPeople,
                                        student=freshman.name,
                                        sid=freshman.id,
                                        department="merch",
                                        points_given=False)
                        try:
                            # add done job to the database
                            db.session.add(fin_job)
                            db.session.commit()
                            if not count:
                                flash('Some Merch Jobs have just been assigned: Please refresh page')
                                count = True
                            # flash('You have successfully added a new assigned Merch Job.')
                        except:
                            # in case done job name already exists
                            flash('Error: this Merch Job already exists in Done.')

    return render_template('admin/merchs/merchs.html',
                           merchs=merchs, title="Merch Jobs")

@admin.route('/merch/form', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_merch():
    """
    List all merch jobs
    """
    check_admin()

    associates = Merch.query.all()
    sent_but_not_assigned = []
    for job in associates:
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)

    return render_template('admin/merchs/merchs-sentout.html',
                           done=sent_but_not_assigned, title="Merch Jobs")

@admin.route('/merch/points', methods=['GET', 'POST'])
@login_required
def points_merch():
    """
    List all merch jobs
    """
    check_admin()

    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        if (str(job.department) == 'merch') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/merchs/merchs-points.html', done=fin_job,
                            title="Merch Jobs: Assign Points")

@admin.route('/merch/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_merch(id, points):
    """
    Add points for freshman for merch jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp += points
    db.session.commit()
    flash('You have successfully added FSPs for ' + freshman.name + '.')

    # redirect to the bike job page
    return redirect(url_for('admin.points_merch'))

    return render_template(title="Merch Jobs: Added Points")

@admin.route('/merch/points/remove/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def remove_points_merch(id, points):
    """
    Remove points for freshman for merch jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp -= points
    db.session.commit()
    flash('You have successfully removed FSPs for ' + freshman.name + '.')

    # redirect to the merch job page
    return redirect(url_for('admin.points_merch'))

    return render_template(title="Merch Jobs: Removed Points")

@admin.route('/merch/points/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_fin_job_merch(id):
    """
    Remove finished job for merch jobs to store in Done db
    """
    check_admin()

    job = Done.query.get_or_404(id)
    job.points_given = True
    db.session.commit()
    flash('Successfully finished Job: ' + job.name + ' for Student: ' + job.student)

    # redirect to the merch job page
    return redirect(url_for('admin.points_merch'))

    return render_template(title="Merch Jobs")

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
                                numPeople=form.numPeople.data,
                                sent=False)
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

@admin.route('/merch/dup/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicate_merch(id):
    """
    Duplicate a merch job from the database
    """
    check_admin()

    add_merch = 3

    merch = Merch.query.get_or_404(id)

    iter_num = merch.name[-1]
    try:
        iter_num = int(iter_num) + 1
    except:
        iter_num = 1

    if (iter_num > 1):
        name = merch.name[:-1] + str(iter_num)
    else:
        name = merch.name + " " + str(iter_num)
    
    dup_merch = Merch(name=name,
                            description=merch.description,
                            date=merch.date,
                            start=merch.start,
                            end=merch.end,
                            fsp=merch.fsp,
                            numPeople=merch.numPeople,
                            sent=merch.sent)
    
    try:
        # add merch job to the database
        db.session.add(dup_merch)
        db.session.commit()
        flash('You have successfully duplicated the Merch job.')
    except:
        # in case merch job name already exists
        flash('Error: this Merch Job already exists.')

    # redirect to the merch job page
    return redirect(url_for('admin.list_merch'))

    return render_template('admin/merchs/merch.html', action="Duplicate",
                           add_merch=add_merch,
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

    for job in spirits:
        if (job.employees != None):
            db.session.delete(job)
            db.session.commit()
            freshmans = Freshman.query.all()
    
            employees = str(job.employees)
            assigned_people = employees.split()
            count = False
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        fin_job = Done(name=job.name,
                                        description=job.description,
                                        date=job.date,
                                        start=job.start,
                                        end=job.end,
                                        fsp=job.fsp,
                                        numPeople=job.numPeople,
                                        student=freshman.name,
                                        sid=freshman.id,
                                        department="spirit",
                                        points_given=False)
                        try:
                            # add done job to the database
                            db.session.add(fin_job)
                            db.session.commit()
                            if not count:
                                flash('Some Spirit Jobs have just been assigned: Please refresh page')
                                count = True
                            # flash('You have successfully added a new assigned Spirit Job.')
                        except:
                            # in case done job name already exists
                            flash('Error: this Spirit Job already exists in Done.')

    return render_template('admin/spirits/spirits.html',
                           spirits=spirits, title="Spirit Jobs")

@admin.route('/spirit/form', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_spirit():
    """
    List all spirit jobs
    """
    check_admin()

    associates = Spirit.query.all()
    sent_but_not_assigned = []
    for job in associates:
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)

    return render_template('admin/spirits/spirits-sentout.html',
                           done=sent_but_not_assigned, title="Spirit Jobs")

@admin.route('/spirit/points', methods=['GET', 'POST'])
@login_required
def points_spirit():
    """
    List all spirit jobs
    """
    check_admin()

    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        if (str(job.department) == 'spirit') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/spirits/spirits-points.html', done=fin_job,
                            title="Spirit Jobs: Assign Points")

@admin.route('/spirit/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_spirit(id, points):
    """
    Add points for freshman for spirit jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp += points
    db.session.commit()
    flash('You have successfully added FSPs for ' + freshman.name + '.')

    # redirect to the spirit job page
    return redirect(url_for('admin.points_spirit'))

    return render_template(title="Spirit Jobs: Added Points")

@admin.route('/spirit/points/remove/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def remove_points_spirit(id, points):
    """
    Remove points for freshman for spirit jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp -= points
    db.session.commit()
    flash('You have successfully removed FSPs for ' + freshman.name + '.')

    # redirect to the spirit job page
    return redirect(url_for('admin.points_spirit'))

    return render_template(title="Spirit Jobs: Removed Points")

@admin.route('/spirit/points/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_fin_job_spirit(id):
    """
    Remove finished job for spirit jobs to store in Done db
    """
    check_admin()

    job = Done.query.get_or_404(id)
    job.points_given = True
    db.session.commit()
    flash('Successfully finished Job: ' + job.name + ' for Student: ' + job.student)

    # redirect to the spirit job page
    return redirect(url_for('admin.points_spirit'))

    return render_template(title="Spirit Jobs")

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
                                numPeople=form.numPeople.data,
                                sent=False)
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

@admin.route('/spirit/dup/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicate_spirit(id):
    """
    Duplicate a spirit job from the database
    """
    check_admin()

    add_spirit = 3

    spirit = Spirit.query.get_or_404(id)

    iter_num = spirit.name[-1]
    try:
        iter_num = int(iter_num) + 1
    except:
        iter_num = 1

    if (iter_num > 1):
        name = spirit.name[:-1] + str(iter_num)
    else:
        name = spirit.name + " " + str(iter_num)
    
    dup_spirit = Spirit(name=name,
                            description=spirit.description,
                            date=spirit.date,
                            start=spirit.start,
                            end=spirit.end,
                            fsp=spirit.fsp,
                            numPeople=spirit.numPeople,
                            sent=spirit.sent)
    
    try:
        # add spirit job to the database
        db.session.add(dup_spirit)
        db.session.commit()
        flash('You have successfully duplicated the Spirit job.')
    except:
        # in case spirit job name already exists
        flash('Error: this Spirit Job already exists.')

    # redirect to the spirit job page
    return redirect(url_for('admin.list_spirit'))

    return render_template('admin/spirits/spirit.html', action="Duplicate",
                           add_spirit=add_spirit,
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

    for job in socials:
        if (job.employees != None):
            db.session.delete(job)
            db.session.commit()
            freshmans = Freshman.query.all()
    
            employees = str(job.employees)
            assigned_people = employees.split()
            count = False
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        fin_job = Done(name=job.name,
                                        description=job.description,
                                        date=job.date,
                                        start=job.start,
                                        end=job.end,
                                        fsp=job.fsp,
                                        numPeople=job.numPeople,
                                        student=freshman.name,
                                        sid=freshman.id,
                                        department="socials",
                                        points_given=False)
                        try:
                            # add done job to the database
                            db.session.add(fin_job)
                            db.session.commit()
                            if not count:
                                flash('Some Socials Jobs have just been assigned: Please refresh page')
                                count = True
                            # flash('You have successfully added a new assigned Socials Job.')
                        except:
                            # in case done job name already exists
                            flash('Error: this Socials Job already exists in Done.')

    return render_template('admin/socials/socials.html',
                           socials=socials, title="Socials Jobs")

@admin.route('/socials/form', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_social():
    """
    List all associates jobs
    """
    check_admin()

    associates = Socials.query.all()
    sent_but_not_assigned = []
    for job in associates:
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)

    return render_template('admin/socials/socials-sentout.html',
                           done=sent_but_not_assigned, title="Socials Jobs")

@admin.route('/socials/points', methods=['GET', 'POST'])
@login_required
def points_social():
    """
    List all socials jobs
    """
    check_admin()

    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        if (str(job.department) == 'socials') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/socials/socials-points.html', done=fin_job,
                            title="Socials Jobs: Assign Points")

@admin.route('/socials/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_social(id, points):
    """
    Add points for freshman for socials jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp += points
    db.session.commit()
    flash('You have successfully added FSPs for ' + freshman.name + '.')

    # redirect to the socials job page
    return redirect(url_for('admin.points_social'))

    return render_template(title="Socials Jobs: Added Points")

@admin.route('/socials/points/remove/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def remove_points_social(id, points):
    """
    Remove points for freshman for socials jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp -= points
    db.session.commit()
    flash('You have successfully removed FSPs for ' + freshman.name + '.')

    # redirect to the socials job page
    return redirect(url_for('admin.points_social'))

    return render_template(title="Socials Jobs: Removed Points")

@admin.route('/socials/points/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_fin_job_social(id):
    """
    Remove finished job for socials jobs to store in Done db
    """
    check_admin()

    job = Done.query.get_or_404(id)
    job.points_given = True
    db.session.commit()
    flash('Successfully finished Job: ' + job.name + ' for Student: ' + job.student)

    # redirect to the social job page
    return redirect(url_for('admin.points_social'))

    return render_template(title="Socials Jobs")

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
                                numPeople=form.numPeople.data,
                                sent=False)
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

@admin.route('/social/dup/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicate_social(id):
    """
    Duplicate a social job from the database
    """
    check_admin()

    add_social = 3

    social = Socials.query.get_or_404(id)

    iter_num = social.name[-1]
    try:
        iter_num = int(iter_num) + 1
    except:
        iter_num = 1

    if (iter_num > 1):
        name = social.name[:-1] + str(iter_num)
    else:
        name = social.name + " " + str(iter_num)
    
    dup_social = Socials(name=name,
                            description=social.description,
                            date=social.date,
                            start=social.start,
                            end=social.end,
                            fsp=social.fsp,
                            numPeople=social.numPeople,
                            sent=social.sent)
    
    try:
        # add socials job to the database
        db.session.add(dup_social)
        db.session.commit()
        flash('You have successfully duplicated the Socials job.')
    except:
        # in case socials job name already exists
        flash('Error: this Socials Job already exists.')

    # redirect to the socials job page
    return redirect(url_for('admin.list_socials'))

    return render_template('admin/socials/social.html', action="Duplicate",
                           add_social=add_social,
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

    for job in slushs:
        if (job.employees != None):
            db.session.delete(job)
            db.session.commit()
            freshmans = Freshman.query.all()
    
            employees = str(job.employees)
            assigned_people = employees.split()
            count = False
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        fin_job = Done(name=job.name,
                                        description=job.description,
                                        date=job.date,
                                        start=job.start,
                                        end=job.end,
                                        fsp=job.fsp,
                                        numPeople=job.numPeople,
                                        student=freshman.name,
                                        sid=freshman.id,
                                        department="slush",
                                        points_given=False)
                        try:
                            # add done job to the database
                            db.session.add(fin_job)
                            db.session.commit()
                            if not count:
                                flash('Some Slush Jobs have just been assigned: Please refresh page')
                                count = True
                            # flash('You have successfully added a new assigned Slush Job.')
                        except:
                            # in case done job name already exists
                            flash('Error: this Slush Job already exists in Done.')

    return render_template('admin/slushs/slushs.html',
                           slushs=slushs, title="Slush Jobs")

@admin.route('/slush/form/', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_slush():
    """
    List all slush jobs
    """
    check_admin()

    associates = Slush.query.all()
    sent_but_not_assigned = []
    for job in associates:
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)

    return render_template('admin/slushs/slushs-sentout.html',
                           done=sent_but_not_assigned, title="Slush Jobs")

@admin.route('/slush/points', methods=['GET', 'POST'])
@login_required
def points_slush():
    """
    List all slush jobs
    """
    check_admin()

    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        if (str(job.department) == 'slush') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/slushs/slushs-points.html', done=fin_job,
                            title="Slush Jobs: Assign Points")

@admin.route('/slush/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_slush(id, points):
    """
    Add points for freshman for slush jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp += points
    db.session.commit()
    flash('You have successfully added FSPs for ' + freshman.name + '.')

    # redirect to the slush job page
    return redirect(url_for('admin.points_slush'))

    return render_template(title="Slush Jobs: Added Points")

@admin.route('/slush/points/remove/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def remove_points_slush(id, points):
    """
    Remove points for freshman for slush jobs
    """
    check_admin()

    freshman = Freshman.query.get_or_404(id)
    freshman.fsp -= points
    db.session.commit()
    flash('You have successfully removed FSPs for ' + freshman.name + '.')

    # redirect to the slush job page
    return redirect(url_for('admin.points_slush'))

    return render_template(title="Slush Jobs: Removed Points")

@admin.route('/slush/points/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_fin_job_slush(id):
    """
    Remove finished job for slush jobs to store in Done db
    """
    check_admin()

    job = Done.query.get_or_404(id)
    job.points_given = True
    db.session.commit()
    flash('Successfully finished Job: ' + job.name + ' for Student: ' + job.student)

    # redirect to the slush job page
    return redirect(url_for('admin.points_slush'))

    return render_template(title="Slush Jobs")

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
                                numPeople=form.numPeople.data,
                                sent=False)
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

@admin.route('/slush/dup/<int:id>', methods=['GET', 'POST'])
@login_required
def duplicate_slush(id):
    """
    Duplicate a slush job from the database
    """
    check_admin()

    add_slush = 3

    slush = Slush.query.get_or_404(id)

    iter_num = slush.name[-1]
    try:
        iter_num = int(iter_num) + 1
    except:
        iter_num = 1

    if (iter_num > 1):
        name = slush.name[:-1] + str(iter_num)
    else:
        name = slush.name + " " + str(iter_num)
    
    dup_slush = Slush(name=name,
                            description=slush.description,
                            date=slush.date,
                            start=slush.start,
                            end=slush.end,
                            fsp=slush.fsp,
                            numPeople=slush.numPeople,
                            sent=slush.sent)
    
    try:
        # add slush job to the database
        db.session.add(dup_slush)
        db.session.commit()
        flash('You have successfully duplicated the Slush job.')
    except:
        # in case slush job name already exists
        flash('Error: this Slush Job already exists.')

    # redirect to the slush job page
    return redirect(url_for('admin.list_slush'))

    return render_template('admin/slushs/slush.html', action="Duplicate",
                           add_slush=add_slush,
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

# Freshman Views

@admin.route('/freshman', methods=['GET', 'POST'])
def list_freshmans_nologin():
    """
    List all departments
    """

    freshmans = Freshman.query.all()

    return render_template('admin/freshmans/freshmans-nologin.html',
                           freshman=freshmans, title="Freshmans")

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
                                netID=form.netID.data,
                                fsp=0)
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
