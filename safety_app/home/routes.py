# -*- encoding: utf-8 -*-
"""
Home routes and views
"""
from datetime import datetime
#import json
#from flask import jsonify

from jinja2 import TemplateNotFound
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from ..home import blueprint
from ..home.models import CheckList, IncidentReport, CourseLearner, TaskRecord
from ..home.constants import FIRST_LIST, COURSE_LIST

COURSE_DICT = dict(enumerate(COURSE_LIST, start=1))

@blueprint.get('/prestarts')
@login_required
def view_prestarts():

    """    Table of pre-start records.    """
    page_num = int(request.args.get("page") or 1)
    entries = CheckList.objects().order_by('-job_date').paginate(page=page_num, per_page=2)
    
    # Detect the current page
    segment = get_segment(request)

    return render_template(
        'home/prestarts.html',
        segment=segment,
        entries=entries.items,
        pages=entries.pages,
        page=page_num,
        per_page=2
    )

@blueprint.route('prestarts/new', methods=["GET", "POST"])
@login_required
def new_prestart():

    """    Record new safety checklist.   """
    if request.method == 'POST':

        checklist = CheckList(
            author=current_user,
            checklist={safety_item: request.form[str(list_num)] for list_num, safety_item in enumerate(FIRST_LIST, start=1)},
            job_site=request.form["job_site"],
            job_activity=request.form["job_activity"],
            comments=request.form["comments"],
            weather_conditions=request.form["weather_conditions"],
            number_of_workers=request.form["number_of_workers"]
        )
        checklist.save()
        
        #return jsonify(checklist)
        return redirect(url_for('home_blueprint.index'))
    
    #dt_now = datetime.now().strftime('%d/%m/%Y')
    return render_template('home/prestart.html', checklist=enumerate(FIRST_LIST, start=1))

@blueprint.get('prestart/<string:id>')
@login_required
def review_prestart(id: str):
    entry = CheckList.objects(id=id).first()

    return render_template('home/prestart-review.html', prestart=entry)


#******************************************************************************
@blueprint.get('/reports')
@login_required
def view_reports():

    """     Show recorded incident reports      """
    entries = IncidentReport.objects(author=current_user)
    # Detect the current page
    segment = get_segment(request)

    return render_template('home/reports.html', segment=segment, entries=entries)

@blueprint.route('reports/incident', methods=["GET", "POST"])
@login_required
def incident_report():
    """    Record new safety checklist    """
    
    if request.method == 'POST':

        incident = IncidentReport(
            author = current_user,
            employee = request.form["employee"],
            job_site = request.form["site"],
            incident_date = request.form["date"],
            description = request.form["description"]
        )
        incident.save()
        
        return redirect(url_for('.view_reports'))
    
    #dt_now = datetime.now().strftime('%m/%d/%Y')

    return render_template('home/incident.html')

@login_required
@blueprint.get("/reports/<string:id>")
def view_report(id: str):
    #entry = IncidentReport.objects().first()
    entry = IncidentReport.objects(id=id).first()

    #return jsonify(entry)
    return render_template('home/incident-review.html', incident_report=entry)
    

#******************************************************************************
@blueprint.route('/training', methods=['GET', 'POST'])
@login_required
def view_training():

    """     Show list of courses completed     """
    courses = COURSE_DICT
    entries = CourseLearner.objects(author=current_user)

    segment = get_segment(request)

    if request.method == 'POST':
        learner = CourseLearner(**request.form)
        learner['author'] = current_user
        learner.save()
        #return jsonify(learner), 201
    
    return render_template('home/training.html', entries=entries, courses=courses, segment=segment)

@blueprint.route('training/<string:id>', methods=['POST'])
@login_required
def edit_training(id: str):

    course_indices = request.form.getlist("cl")
    new_courses = [COURSE_DICT[int(num)] for num in course_indices]
    
    edit = {'tickets': new_courses}
    learner = CourseLearner.objects(id=id)
    learner.update(**edit)

    #return jsonify(learner)
    #return redirect(url_for('home_blueprint.index'))
    return redirect(url_for('.view_training'))

@blueprint.route('training/<int:course>', methods=["GET", "POST"])
@login_required
def filter_training(course: int):
    """     Show list of courses completed     """
    courses = COURSE_DICT
    entries = CourseLearner.objects(author=current_user, tickets__contains=courses[course])
    segment = get_segment(request)
    
    return render_template('home/training.html', entries=entries, courses=courses, segment=segment, course=courses[course])


#******************************************************************************
@blueprint.route('/dash', methods=['GET', 'POST'])
@login_required
def view_tasks():
    tasks = TaskRecord.objects(author=current_user).order_by('due_date')
    num_tasks = tasks.count()
    num_active = tasks(complete=False).count()
    dt_now = datetime.now()

    if request.method == 'POST':
        new_task = TaskRecord(**request.form)
        new_task['author'] = current_user
        new_task.save()

        tasks = TaskRecord.objects(author=current_user)
        num_tasks = tasks.count()
        num_active = tasks(complete=False).count()
        #return jsonify(new_task), 201

    return render_template(
        'home/dash.html', 
        tasks=tasks, 
        date=dt_now, 
        num_tasks=num_tasks, 
        num_active=num_active
    )

@blueprint.route('dash/edit', methods=['POST'])
@login_required
def edit_tasks():

    completed_tasks = request.form.getlist("ct")
    active_tasks = TaskRecord.objects(id__in=completed_tasks)
    active_tasks.update(complete=True)

    #return jsonify({"completed": completed_tasks, "active": active_tasks})
    return redirect(url_for('.view_tasks'))

@blueprint.route('dash/delete', methods=['POST'])
@login_required
def delete_tasks():

    deletion = request.form.getlist("dt")
    tasks_to_delete = TaskRecord.objects(id__in=deletion)
    tasks_to_delete.delete()

    return redirect(url_for('.view_tasks'))

#******************************************************************************
@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    #return render_template('home/dash.html', tasks=tasks, segment=segment)
    return redirect(url_for('.view_tasks'))

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, timedate=datetime.now())

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

