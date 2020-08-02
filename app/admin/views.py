# Views for admin blueprint

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import DepartmentForm, AssociatesForm, BikeForm, CulArtForm, MerchForm, SpiritForm, SocialsForm, SlushForm, RoleForm, FreshmanForm
from .. import db
from ..models import Department, Associates, Bike, CulArt, Merch, Spirit, Socials, Slush, Employee, Freshman, Done
from sqlalchemy.exc import SQLAlchemyError
import MySQLdb


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
    new_associates = []
    for job in associates:
        #### Case where employees have been assigned to a Job ###
        if (job.employees != None):
            ### Delete the job from the Associates FSP Jobs
            db.session.delete(job)
            db.session.commit()

            ### Query all Freshman db entries
            freshmans = Freshman.query.all()
            ### Obtain the employees for the current Associates Job
            employees = str(job.employees)
            assigned_people = employees.split()

            count = False
            ### Iterate through the assigned people
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        ### Create "finished assigning" job to the Done db
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
                            # Add that the job to the Done db
                            db.session.add(fin_job)
                            db.session.commit()
                            # Some handling to make sure the message below only
                            # shows once if there are multiple jobs being re-assigned
                            if not count:
                                flash('Some Associate Jobs have just been assigned')
                                count = True
                        except:
                            # In case the job name already exists
                            flash('Error: this Associates Job already exists in Done.')
        ### De-display job from main if the job has been sent out
        elif job.sent == True:
            pass
        ### Only display the job if it has not been sent out and there are no students assigned
        else:
            new_associates.append(job)

    ### Rendering of HTML
    return render_template('admin/associates/associates.html',
                           associates=new_associates, title="Associates Jobs")

@admin.route('/associates/sentout', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_associate():
    """
    List all associates jobs that have been sentout but not assigned
    Should de-display the jobs that have "sentout" col == True from "associates"
        and display the job at "associates/sentout" 
    """
    check_admin()

    ### Queries all Associates Jobs
    associates = Associates.query.all()
    sent_but_not_assigned = []
    for job in associates:
        ### If the job has been sent out or there are no employees assigned
        if job.sent and (job.employees == None):
            sent_but_not_assigned.append(job)
    ### Displays the Jobs for sentout but not assigned
    return render_template('admin/associates/associates-sentout.html',
                           done=sent_but_not_assigned, title="Associates Jobs")

#### Ignore this function for now
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
    Only displays jobs that are associates jobs and if point have not been assigned
    """
    check_admin()

    ### Queries all the jobs in the Done db
    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        ### Only displays jobs that are associates jobs
        ###     and if point have not been assigned
        if (str(job.department) == 'associates') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/associates/associates-points.html', done=fin_job,
                            title="Associates Jobs: Assign Points")

@admin.route('/associates/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_associate(id, points):
    """
    Add points functionality for freshman for Associates jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Assigns points
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
    Remove points functionality for freshman for associates jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Removes points
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

    ### Queries the job from Done db
    job = Done.query.get_or_404(id)
    # Sets that points have been assigned
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
    ### Specifies adding job in associate.html
    add_associate = 1

    ### Calls an Associates Form
    form = AssociatesForm()
    if form.validate_on_submit():
        ### Assigns data from form
        associate = Associates(name=form.name.data,
                                description=form.description.data,
                                date=form.date.data,
                                start=form.start_at.data,
                                end=form.end_at.data,
                                fsp=form.fsp.data,
                                numPeople=form.numPeople.data,
                                sent=False)

        try:
            # Add the associates job to the database
            db.session.add(associate)
            db.session.commit()
            flash('You have successfully added a new Associates Job.')
        except:
            # in case associates job name already exists
            flash('Error: this Associates Job already exists.')
        
        # redirect to associates job page once done
        return redirect(url_for('admin.list_associates'))
    
    # load associates main page
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

    ### Specifies duplicating job in associate.html
    add_associate = 3
    ### Queries the associates job to duplicate
    associate = Associates.query.get_or_404(id)

    ### Check to see if duplication has occurred before
    iter_num = associate.name[-1]
    try:
        # Successfully adds 1 to count
        iter_num = int(iter_num) + 1
    except:
        # Count should start at 1
        iter_num = 1
    ### Updates the Job name
    if (iter_num > 1):
        # Only changes the number
        name = associate.name[:-1] + str(iter_num)
    else:
        # Adds a number to the end
        name = associate.name + " " + str(iter_num)
    ### Builds the duplicate associates job
    dup_associate = Associates(name=name,
                            description=associate.description,
                            date=associate.date,
                            start=associate.start,
                            end=associate.end,
                            fsp=associate.fsp,
                            numPeople=associate.numPeople,
                            sent=associate.sent)
    
    try:
        # Adds duplciate associates job to the database
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
    Edit an associates job
    """
    check_admin()

    ### Specifies editting job in associate.html
    add_associate = 2
    ### Queries the associates job to edit
    associate = Associates.query.get_or_404(id)
    ### Calls an Associates Form
    form = AssociatesForm(obj=associate)
    if form.validate_on_submit():
        associate.name = form.name.data
        associate.description = form.description.data
        associate.date = form.date.data
        associate.start = form.start_at.data
        associate.end = form.end_at.data
        associate.fsp = form.fsp.data
        associate.numPeople = form.numPeople.data
        try:
            db.session.commit()
            # redirect to the associates job page
            return redirect(url_for('admin.list_associates'))

            flash('You have successfully edited the Associates Job.')
        except MySQLdb.IntegrityError:
            # redirect to the associates job page
            return redirect(url_for('admin.list_associates'))

            # in case associates job name already exists
            flash('Error: this Associates Job already exists.')

    return render_template('admin/associates/associate.html', action="Edit",
                           add_associate=add_associate, form=form,
                           associate=associate, title="Edit Associates Job")

@admin.route('/associates/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_associate(id):
    """
    Delete an associate job from the database
    """
    check_admin()
    ### Queries the associates job to delete
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
    new_bikes = []
    for job in bikes:
        #### Case where employees have been assigned to a Job ###
        if (job.employees != None):
            ### Delete the job from the Bikes FSP Jobs
            db.session.delete(job)
            db.session.commit()

            ### Query all Freshman db entries
            freshmans = Freshman.query.all()
            ### Obtain the employees for the current Bikes Job
            employees = str(job.employees)
            assigned_people = employees.split()

            count = False
            ### Iterate through the assigned people
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        ### Create "finished assigning" job to the Done db
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
                            # Add that the job to the Done db
                            db.session.add(fin_job)
                            db.session.commit()
                            # Some handling to make sure the message below only
                            # shows once if there are multiple jobs being re-assigned
                            if not count:
                                flash('Some Bike Jobs have just been assigned: Please refresh page')
                                count = True
                            # flash('You have successfully added a new assigned Bike Job.')
                        except:
                            # in case done job name already exists
                            flash('Error: this Bike Job already exists in Done.')
        ### De-display job from main if the job has been sent out
        elif job.sent == True:
            pass
        ### Only display the job if it has not been sent out and there are no students assigned
        else:
            new_bikes.append(job)

    return render_template('admin/bikes/bikes.html',
                           bikes=new_bikes, title="Beer Bike Jobs")

@admin.route('/bike/form', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_bike():
    """
    List all bike jobs that have been sentout but not assigned
    Should de-display the jobs that have "sentout" col == True from "bikes"
        and display the job at "bikes/sentout" 
    """
    check_admin()

    ### Queries all Bikes Jobs
    bikes = Bike.query.all()
    sent_but_not_assigned = []
    for job in bikes:
        ### If the job has been sent out or there are no employees assigned
        if not job.sent and (job.employees == None):
            sent_but_not_assigned.append(job)
    ### Displays the Jobs for sentout but not assigned
    return render_template('admin/bikes/bikes-sentout.html',
                           done=sent_but_not_assigned, title="Bike Jobs")

@admin.route('/bike/points', methods=['GET', 'POST'])
@login_required
def points_bike():
    """
    Only displays jobs that are bikes jobs and if point have not been assigned
    """
    check_admin()

    ### Queries all the jobs in the Done db
    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        ### Only displays jobs that are bike jobs
        ###     and if point have not been assigned
        if (str(job.department) == 'bike') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/bikes/bikes-points.html', done=fin_job,
                            title="Bike Jobs: Assign Points")

@admin.route('/bike/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_bike(id, points):
    """
    Add points functionality for freshman for Bikes jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Assigns points
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
    Remove points functionality for freshman for bikes jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Removes points
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

    ### Queries the job from Done db
    job = Done.query.get_or_404(id)
    # Sets that points have been assigned
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
    ### Specifies adding job in bike.html
    add_bike = 1

    ### Calls an Bike Form
    form = BikeForm()
    if form.validate_on_submit():
        ### Assigns data from form
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

    # load bikes main page
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

    ### Specifies duplicating job in bike.html
    add_bike = 3
    ### Queries the bike job to duplicate
    bike = Bike.query.get_or_404(id)

    ### Check to see if duplication has occurred before
    iter_num = bike.name[-1]
    try:
        # Successfully adds 1 to count
        iter_num = int(iter_num) + 1
    except:
        iter_num = 1
    ### Updates the Job name
    if (iter_num > 1):
        # Only changes the number
        name = bike.name[:-1] + str(iter_num)
    else:
        # Adds a number to the end
        name = bike.name + " " + str(iter_num)
    ### Builds the duplicate bikes job
    dup_bike = Bike(name=name,
                            description=bike.description,
                            date=bike.date,
                            start=bike.start,
                            end=bike.end,
                            fsp=bike.fsp,
                            numPeople=bike.numPeople,
                            sent=bike.sent)
    
    try:
        # Adds duplciate bike job to the database
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
    Edit a bikes job
    """
    check_admin()

    ### Specifies editting job in bikes.html
    add_bike = 2
    ### Queries the bikes job to edit
    bike = Bike.query.get_or_404(id)
    ### Calls an Bike Form
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
        try:
            db.session.commit()
            # redirect to the bikes job page
            return redirect(url_for('admin.list_bikes'))

            flash('You have successfully edited the Bikes Job.')
        except MySQLdb.IntegrityError:
            # redirect to the bikes job page
            return redirect(url_for('admin.list_bikes'))

            # in case associates job name already exists
            flash('Error: this Bikes Job already exists.')

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
    ### Queries the bikes job to delete
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
    new_cularts = []
    for job in cularts:
        #### Case where cularts have been assigned to a Job ###
        if (job.employees != None):
            ### Delete the job from the CulArt FSP Jobs
            db.session.delete(job)
            db.session.commit()

            ### Query all Freshman db entries
            freshmans = Freshman.query.all()
            ### Obtain the employees for the current culart Job
            employees = str(job.employees)
            assigned_people = employees.split()

            count = False
            ### Iterate through the assigned people
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        ### Create "finished assigning" job to the Done db
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
                            # Add that the job to the Done db
                            db.session.add(fin_job)
                            db.session.commit()
                            # Some handling to make sure the message below only
                            # shows once if there are multiple jobs being re-assigned
                            if not count:
                                flash('Some C & A Jobs have just been assigned: Please refresh page')
                                count = True
                            # flash('You have successfully added a new assigned C & A Job.')
                        except:
                            # in case done job name already exists
                            flash('Error: this C & A Job already exists in Done.')
        ### De-display job from main if the job has been sent out
        elif job.sent == True:
            pass
        ### Only display the job if it has not been sent out and there are no students assigned
        else:
            new_associates.append(job)
    return render_template('admin/cularts/cularts.html',
                           cularts=new_cularts, title="C & A Jobs")

@admin.route('/culart/form', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_culart():
    """
    List all culart jobs that have been sentout but not assigned
    Should de-display the jobs that have "sentout" col == True from "culart"
        and display the job at "cularts/sentout" 
    """
    check_admin()

    ### Queries all Associates Jobs
    culart = CulArt.query.all()
    sent_but_not_assigned = []
    for job in culart:
        ### If the job has been sent out or there are no employees assigned
        if not job.sent and (job.employees == None):
            sent_but_not_assigned.append(job)
    ### Displays the Jobs for sentout but not assigned
    return render_template('admin/cularts/cularts-sentout.html',
                           done=sent_but_not_assigned, title="C & A Jobs")

@admin.route('/culart/points', methods=['GET', 'POST'])
@login_required
def points_culart():
    """
    Only displays jobs that are C & A jobs and if points have not been assigned
    """
    check_admin()

    ### Queries all the jobs in the Done db
    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        ### Only displays jobs that are associates jobs
        ###     and if point have not been assigned
        if (str(job.department) == 'culart') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/cularts/cularts-points.html', done=fin_job,
                            title="C & A Jobs: Assign Points")

@admin.route('/culart/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_culart(id, points):
    """
    Add points functionality for freshman for C & A jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Assigns points
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
    Remove points functionality for freshman for C & A jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Removes points
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

    ### Queries the job from Done db
    job = Done.query.get_or_404(id)
    # Sets that points have been assigned
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
    ### Specifies adding job in culart.html
    add_culart = 1

    ### Calls an CulArt Form
    form = CulArtForm()
    if form.validate_on_submit():
        ### Assigns data from form
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

    ### Specifies duplicating job in culart.html
    add_culart = 3
    ### Queries the culart job to duplicate
    culart = CulArt.query.get_or_404(id)

    ### Check to see if duplication has occurred before
    iter_num = culart.name[-1]
    try:
        # Successfully adds 1 to count
        iter_num = int(iter_num) + 1
    except:
        # Count should start at 1
        iter_num = 1
    ### Updates the Job name
    if (iter_num > 1):
        # Only changes the number
        name = culart.name[:-1] + str(iter_num)
    else:
        # Adds a number to the end
        name = culart.name + " " + str(iter_num)
    ### Builds the duplicate C & A job
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

    ### Specifies editting job in culart.html
    add_culart = 2
    ### Queries the C & A job to edit
    culart = CulArt.query.get_or_404(id)
    ### Calls an C & A Form
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
        try:
            db.session.commit()
            # redirect to the associates job page
            return redirect(url_for('admin.list_cularts'))

            flash('You have successfully edited the C & A Job.')
        except MySQLdb.IntegrityError:
            # redirect to the associates job page
            return redirect(url_for('admin.list_cularts'))

            # in case associates job name already exists
            flash('Error: this Associates Job already exists.')

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
    ### Queries the C & A job to delete
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
    new_merch = []
    for job in merchs:
        #### Case where employees have been assigned to a Job ###
        if (job.employees != None):
            ### Delete the job from the Merch FSP Jobs
            db.session.delete(job)
            db.session.commit()

            ### Query all Freshman db entries
            freshmans = Freshman.query.all()
            ### Obtain the employees for the current Merch Job
            employees = str(job.employees)
            assigned_people = employees.split()

            count = False
            ### Iterate through the assigned people
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        ### Create "finished assigning" job to the Done db
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
                            # Add done job to the database
                            db.session.add(fin_job)
                            db.session.commit()
                            # Some handling to make sure the message below only
                            # shows once if there are multiple jobs being re-assigned
                            if not count:
                                flash('Some Merch Jobs have just been assigned: Please refresh page')
                                count = True
                            # flash('You have successfully added a new assigned Merch Job.')
                        except:
                            # in case done job name already exists
                            flash('Error: this Merch Job already exists in Done.')
        ### De-display job from main if the job has been sent out
        elif job.sent == True:
            pass
        ### Only display the job if it has not been sent out and there are no students assigned
        else:
            new_merch.append(job)

    return render_template('admin/merchs/merchs.html',
                           merchs=new_merch, title="Merch Jobs")

@admin.route('/merch/form', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_merch():
    """
    List all merch jobs that have been sentout but not assigned
    Should de-display the jobs that have "sentout" col == True from "merch"
        and display the job at "merchs/sentout" 
    """
    check_admin()

    ### Queries all Merch Jobs
    associates = Merch.query.all()
    sent_but_not_assigned = []
    for job in associates:
        ### If the job has been sent out or there are no employees assigned
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)
    ### Displays the Jobs for sentout but not assigned
    return render_template('admin/merchs/merchs-sentout.html',
                           done=sent_but_not_assigned, title="Merch Jobs")

@admin.route('/merch/points', methods=['GET', 'POST'])
@login_required
def points_merch():
    """
    Only displays jobs that are merch jobs and if point have not been assigned
    """
    check_admin()

    ### Queries all the jobs in the Done db
    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        ### Only displays jobs that are merch jobs
        ###     and if point have not been assigned
        if (str(job.department) == 'merch') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/merchs/merchs-points.html', done=fin_job,
                            title="Merch Jobs: Assign Points")

@admin.route('/merch/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_merch(id, points):
    """
    Add points for freshman for Merch jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Assigns points
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
    Remove points functionality for freshman for merch jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Removes points
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

    ### Queries the job from Done db
    job = Done.query.get_or_404(id)
    # Sets that points have been assigned
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
    ### Specifies adding job in merch.html
    add_merch = 1

    ### Calls a Merch Form
    form = MerchForm()
    if form.validate_on_submit():
        ### Assigns data from form
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

        # redirect to merch job page once done
        return redirect(url_for('admin.list_merch'))

    # load merch main page
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

    ### Specifies duplicating job in merch.html
    add_merch = 3
    ### Queries the merch job to duplicate
    merch = Merch.query.get_or_404(id)

    ### Check to see if duplication has occurred before
    iter_num = merch.name[-1]
    try:
        # Successfully adds 1 to count
        iter_num = int(iter_num) + 1
    except:
        iter_num = 1
    ### Updates the Job name
    if (iter_num > 1):
        # Only changes the number
        name = merch.name[:-1] + str(iter_num)
    else:
        # Adds a number to the end
        name = merch.name + " " + str(iter_num)
    ### Builds the duplicate merch job
    dup_merch = Merch(name=name,
                            description=merch.description,
                            date=merch.date,
                            start=merch.start,
                            end=merch.end,
                            fsp=merch.fsp,
                            numPeople=merch.numPeople,
                            sent=merch.sent)
    
    try:
        # add duplciate merch job to the database
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
    Edit a merch job
    """
    check_admin()

    ### Specifies editting job in merch.html
    add_merch = 2
    ### Queries the merch job to edit
    merch = Merch.query.get_or_404(id)
    ### Calls a Merch Form
    form = MerchForm(obj=merch)
    if form.validate_on_submit():
        merch.name = form.name.data
        merch.description = form.description.data
        merch.date = form.date.data
        merch.start = form.start_at.data
        merch.end = form.end_at.data
        merch.fsp = form.fsp.data
        merch.numPeople = form.numPeople.data
        try:
            db.session.commit()
            # redirect to the merch job page
            return redirect(url_for('admin.list_associates'))

            flash('You have successfully edited the Merch Job.')
        except MySQLdb.IntegrityError:
            # redirect to the merch job page
            return redirect(url_for('admin.list_merch'))

            # in case merch job name already exists
            flash('Error: this Merch Job already exists.')

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
    ### Queries the merch job to delete
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
    new_spirit = []
    for job in spirits:
        #### Case where employees have been assigned to a Job ###
        if (job.employees != None):
            ### Delete the job from the Spirit FSP Jobs
            db.session.delete(job)
            db.session.commit()

            ### Query all Freshman db entries
            freshmans = Freshman.query.all()
            ### Obtain the employees for the current Spirit Job
            employees = str(job.employees)
            assigned_people = employees.split()

            count = False
            ### Iterate through the assigned people
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        ### Create "finished assigning" job to the Done db
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
                            # Add that the job to the Done db
                            db.session.add(fin_job)
                            db.session.commit()
                            # Some handling to make sure the message below only
                            # shows once if there are multiple jobs being re-assigned
                            if not count:
                                flash('Some Spirit Jobs have just been assigned: Please refresh page')
                                count = True
                        except:
                            # in case done job name already exists
                            flash('Error: this Spirit Job already exists in Done.')
        ### De-display job from main if the job has been sent out
        elif job.sent == True:
            pass
        ### Only display the job if it has not been sent out and there are no students assigned
        else:
            new_spirit.append(job)

    ### Rendering of HTML 
    return render_template('admin/spirits/spirits.html',
                           spirits=new_spirit, title="Spirit Jobs")

@admin.route('/spirit/form', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_spirit():
    """
    List all spirit jobs that have been sentout but not assigned
    Should de-display the jobs that have "sentout" col == True from "spirit"
        and display the job at "spirits/sentout" 
    """
    check_admin()

    ### Queries all Spirit Jobs
    associates = Spirit.query.all()
    sent_but_not_assigned = []
    for job in associates:
        ### If the job has been sent out or there are no employees assigned
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)
    ### Displays the Jobs for sentout but not assigned
    return render_template('admin/spirits/spirits-sentout.html',
                           done=sent_but_not_assigned, title="Spirit Jobs")

@admin.route('/spirit/points', methods=['GET', 'POST'])
@login_required
def points_spirit():
    """
    Only displays jobs that are spirit jobs and if point have not been assigned
    """
    check_admin()

    ### Queries all the jobs in the Done db
    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        ### Only displays jobs that are spirit jobs
        ###     and if point have not been assigned
        if (str(job.department) == 'spirit') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/spirits/spirits-points.html', done=fin_job,
                            title="Spirit Jobs: Assign Points")

@admin.route('/spirit/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_spirit(id, points):
    """
    Add points functionality for freshman for Spirit jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Assigns points
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
    Remove points functionality for freshman for spirit jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Removes points
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

    ### Queries the job from Done db
    job = Done.query.get_or_404(id)
    # Sets that points have been assigned
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
    ### Specifies adding job in spirit.html
    add_spirit = 1

    ### Calls an Spirit Form
    form = SpiritForm()
    if form.validate_on_submit():
        ### Assigns data from form
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

        # redirect to spirit job page once done
        return redirect(url_for('admin.list_spirit'))

    # load spirit main page
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

    ### Specifies duplicating job in spirit.html
    add_spirit = 3
    ### Queries the spirit job to duplicate
    spirit = Spirit.query.get_or_404(id)

    ### Check to see if duplication has occurred before
    iter_num = spirit.name[-1]
    try:
        # Successfully adds 1 to count
        iter_num = int(iter_num) + 1
    except:
        # Count should start at 1
        iter_num = 1
    ### Updates the Job name
    if (iter_num > 1):
        # Only changes the number
        name = spirit.name[:-1] + str(iter_num)
    else:
        # Adds a number to the end
        name = spirit.name + " " + str(iter_num)
    ### Builds the duplicate spirit job
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

    ### Specifies editting job in spirit.html
    add_spirit = 2
    ### Queries the spirit job to edit
    spirit = Spirit.query.get_or_404(id)
    ### Calls a Spirit Form
    form = SpiritForm(obj=spirit)
    if form.validate_on_submit():
        spirit.name = form.name.data
        spirit.description = form.description.data
        spirit.date = form.date.data
        spirit.start = form.start_at.data
        spirit.end = form.end_at.data
        spirit.fsp = form.fsp.data
        spirit.numPeople = form.numPeople.data
        try:
            db.session.commit()
            # redirect to the spirit job page
            return redirect(url_for('admin.list_spirit'))

            flash('You have successfully edited the Spirit Job.')
        except MySQLdb.IntegrityError:
            # redirect to the spirit job page
            return redirect(url_for('admin.list_spirit'))

            # in case spirit job name already exists
            flash('Error: this Spirit Job already exists.')
        
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
    ### Queries the spirit job to delete
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
    new_socials = []
    for job in socials:
        #### Case where employees have been assigned to a Job ###
        if (job.employees != None):
            db.session.delete(job)
            db.session.commit()

            ### Query all Freshman db entries
            freshmans = Freshman.query.all()
            ### Obtain the employees for the current Spirit Job
            employees = str(job.employees)
            assigned_people = employees.split()

            count = False
            ### Iterate through the assigned people
            for person in assigned_people:
                for freshman in freshmans:
                    if freshman.netID == person:
                        ### Create "finished assigning" job to the Done db
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
                            # add done job to the Done db
                            db.session.add(fin_job)
                            db.session.commit()
                            # Some handling to make sure the message below only
                            # shows once if there are multiple jobs being re-assigned
                            if not count:
                                flash('Some Socials Jobs have just been assigned: Please refresh page')
                                count = True
                        except:
                            # in case done job name already exists
                            flash('Error: this Socials Job already exists in Done.')
        ### De-display job from main if the job has been sent out
        elif job.sent == True:
            pass
        ### Only display the job if it has not been sent out and there are no students assigned
        else:
            new_socials.append(job)

    ### Rendering of HTML        
    return render_template('admin/socials/socials.html',
                           socials=new_socials, title="Socials Jobs")

@admin.route('/socials/form', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_social():
    """
    List all social jobs that have been sentout but not assigned
    Should de-display the jobs that have "sentout" col == True from "social"
        and display the job at "socials/sentout" 
    """
    check_admin()

    ### Queries all Social Jobs
    associates = Socials.query.all()
    sent_but_not_assigned = []
    for job in associates:
        ### If the job has been sent out or there are no employees assigned
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)
    ### Displays the Jobs for sentout but not assigned
    return render_template('admin/socials/socials-sentout.html',
                           done=sent_but_not_assigned, title="Socials Jobs")

@admin.route('/socials/points', methods=['GET', 'POST'])
@login_required
def points_social():
    """
    Only displays jobs that are social jobs and if point have not been assigned
    """
    check_admin()

    ### Queries all the jobs in the Done db
    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        ### Only displays jobs that are social jobs
        ###     and if point have not been assigned
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

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Assigns points
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
    Remove points functionality for freshman for socials jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Removes points
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

    ### Queries the job from Done db
    job = Done.query.get_or_404(id)
    # Sets that points have been assigned
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
    ### Specifies adding job in social.html
    add_social = 1

    ### Calls an Associates Form
    form = SocialsForm()
    if form.validate_on_submit():
        ### Assigns data from form
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

        # redirect to socials job page once done
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

    ### Specifies duplicating job in social.html
    add_social = 3
    ### Queries the socials job to duplicate
    social = Socials.query.get_or_404(id)

    ### Check to see if duplication has occurred before
    iter_num = social.name[-1]
    try:
        # Successfully adds 1 to count
        iter_num = int(iter_num) + 1
    except:
        # Count should start at 1
        iter_num = 1
    ### Updates the Job name
    if (iter_num > 1):
        # Only changes the number
        name = social.name[:-1] + str(iter_num)
    else:
        # Adds a number to the end
        name = social.name + " " + str(iter_num)
    ### Builds the duplicate socials job
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
    Edit a socials job
    """
    check_admin()

    ### Specifies editting job in social.html
    add_social = 2
    ### Queries the socials job to edit
    social = Socials.query.get_or_404(id)
    ### Calls a Socials Form
    form = SocialsForm(obj=social)
    if form.validate_on_submit():
        social.name = form.name.data
        social.description = form.description.data
        social.date = form.date.data
        social.start = form.start_at.data
        social.end = form.end_at.data
        social.fsp = form.fsp.data
        social.numPeople = form.numPeople.data
        try:
            db.session.commit()
            # redirect to the socials job page
            return redirect(url_for('admin.list_socials'))

            flash('You have successfully edited the Socials Job.')
        except MySQLdb.IntegrityError:
            # redirect to the socials job page
            return redirect(url_for('admin.list_socials'))

            # in case socials job name already exists
            flash('Error: this Socials Job already exists.')

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
    ### Queries the socials job to delete
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
    new_slush = []
    for job in slushs:
        #### Case where employees have been assigned to a Job ###
        if (job.employees != None):
            ### Delete the job from the Slush FSP Jobs
            db.session.delete(job)
            db.session.commit()

            ### Query all Freshman db entries
            freshmans = Freshman.query.all()
            ### Obtain the employees for the current Slush Job
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
                            # Some handling to make sure the message below only
                            # shows once if there are multiple jobs being re-assigned
                            if not count:
                                flash('Some Slush Jobs have just been assigned: Please refresh page')
                                count = True
                        except:
                            # in case done job name already exists
                            flash('Error: this Slush Job already exists in Done.')
        ### De-display job from main if the job has been sent out
        elif job.sent == True:
            pass
        ### Only display the job if it has not been sent out and there are no students assigned
        else:
            new_slush.append(job)
    return render_template('admin/slushs/slushs.html',
                           slushs=new_slush, title="Slush Jobs")

@admin.route('/slush/form/', methods=['GET', 'POST'])
@login_required
def list_sentout_but_not_assigned_slush():
    """
    List all slush jobs that have been sentout but not assigned
    Should de-display the jobs that have "sentout" col == True from "slush"
        and display the job at "slushs/sentout" 
    """
    check_admin()

    ### Queries all Slush Jobs
    associates = Slush.query.all()
    sent_but_not_assigned = []
    for job in associates:
        ### If the job has been sent out or there are no employees assigned
        if not (job.sent or str(job.employees)):
            sent_but_not_assigned.append(job)
    ### Displays the Jobs for sentout but not assigned
    return render_template('admin/slushs/slushs-sentout.html',
                           done=sent_but_not_assigned, title="Slush Jobs")

@admin.route('/slush/points', methods=['GET', 'POST'])
@login_required
def points_slush():
    """
    Only displays jobs that are slush jobs and if point have not been assigned
    """
    check_admin()

    ### Queries all the jobs in the Done db
    jobs = Done.query.all()
    fin_job = []
    for job in jobs:
        ### Only displays jobs that are slush jobs
        ###     and if point have not been assigned
        if (str(job.department) == 'slush') and not job.points_given:
            fin_job.append(job)

    return render_template('admin/slushs/slushs-points.html', done=fin_job,
                            title="Slush Jobs: Assign Points")

@admin.route('/slush/points/add/<int:id>/<int:points>', methods=['GET', 'POST'])
@login_required
def add_points_slush(id, points):
    """
    Add points functionality for freshman for slush jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Assigns points
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
    Remove points functionality for freshman for slush jobs
    """
    check_admin()

    ### Queries a specific freshman from id
    freshman = Freshman.query.get_or_404(id)
    # Removes points
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

    ### Queries the job from Done db
    job = Done.query.get_or_404(id)
    # Sets that points have been assigned
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
    ### Specifies adding job in slush.html
    add_slush = 1

    ### Calls an Slush Form
    form = SlushForm()
    if form.validate_on_submit():
        ### Assigns data from form
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

    # load slush main page
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

    ### Specifies duplicating job in slush.html
    add_slush = 3
    ### Queries the slush job to duplicate
    slush = Slush.query.get_or_404(id)

    ### Check to see if duplication has occurred before
    iter_num = slush.name[-1]
    try:
        # Successfully adds 1 to count
        iter_num = int(iter_num) + 1
    except:
        # Count should start at 1
        iter_num = 1
    ### Updates the Job name
    if (iter_num > 1):
        # Only changes the number
        name = slush.name[:-1] + str(iter_num)
    else:
        # Adds a number to the end
        name = slush.name + " " + str(iter_num)
    ### Builds the duplicate slush job
    dup_slush = Slush(name=name,
                            description=slush.description,
                            date=slush.date,
                            start=slush.start,
                            end=slush.end,
                            fsp=slush.fsp,
                            numPeople=slush.numPeople,
                            sent=slush.sent)
    
    try:
        # add duplciate slush job to the database
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
    Edit a slush job
    """
    check_admin()

    ### Specifies editting job in slush.html
    add_slush = 2
    ### Queries the slush job to edit
    slush = Slush.query.get_or_404(id)
    ### Calls a Slush Form
    form = SlushForm(obj=slush)
    if form.validate_on_submit():
        slush.name = form.name.data
        slush.description = form.description.data
        slush.date = form.date.data
        slush.start = form.start_at.data
        slush.end = form.end_at.data
        slush.fsp = form.fsp.data
        slush.numPeople = form.numPeople.data
        try:
            db.session.commit()
            # redirect to the slush job page
            return redirect(url_for('admin.list_slush'))

            flash('You have successfully edited the Slush Job.')
        except MySQLdb.IntegrityError:
            # redirect to the slush job page
            return redirect(url_for('admin.list_slush'))

            # in case slush job name already exists
            flash('Error: this Slush Job already exists.')

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
    ### Queries the slush job to delete
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


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')

#Role Views

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
