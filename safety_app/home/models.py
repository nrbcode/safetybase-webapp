from datetime import datetime

from ..authentication.models import db, User


class CheckList(db.Document):
    '''
    A single safety checklist form
    '''
    author = db.ReferenceField(User)
    job_site = db.StringField(required=True, max_length=50)
    job_date = db.DateTimeField(required=True, default=datetime.now())
    checklist = db.DictField()
    job_activity = db.StringField(required=True, max_length=50)
    comments = db.StringField()
    number_of_workers = db.IntField()
    weather_conditions = db.StringField()

    def __repr__(self):
        return f"CheckList({self.job_site}, {self.job_date}, {self.job_activity})"

    def __str__(self):
        return f"{self.job_site}, {self.display_date()}"

    def to_json(self):
        return {
            "author": self.author,
            "site": self.job_site
        }

    def display_date(self):
        return self.job_date.strftime('%A %d %B %Y')

class IncidentReport(db.Document):
    '''
    An incident report
    '''
    #_id = db.StringField()
    author = db.ReferenceField(User)
    employee = db.StringField(max_length=50)
    job_site = db.StringField(max_length=50)
    form_date = db.DateTimeField(required=True, default=datetime.now())
    incident_date = db.DateTimeField(required=True)
    description = db.StringField(max_length=100)
    
    def __repr__(self):
        return f"CheckList({self.employee}, {self.job_site})"

    def __str__(self):
        return f"{self.employee}, {self.job_site}, {self.display_date()}."

    def to_json(self):
        return {
            "employee": self.employee,
            "site": self.job_site
        }

    def display_date(self):
        return self.incident_date.strftime('%A %d %B %Y')

class CourseLearner(db.Document):

    #_id = db.StringField()
    author = db.ReferenceField(User)
    first_name = db.StringField(max_length=30)
    last_name = db.StringField(max_length=30)
    mobile = db.IntField()
    date = db.DateTimeField(required=True, default=datetime.now())

    tickets = db.ListField(db.StringField(max_length=50))
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class TaskRecord(db.Document):

    author = db.ReferenceField(User)
    added_date = db.DateTimeField(required=True, default=datetime.now())
    due_date = db.DateTimeField(required=True)
    task = db.StringField(max_length=100)
    complete = db.BooleanField(required=True, default=False)

    def __str__(self):
        return f"{self.task}, {self.display_date()}"

    def display_date(self):
        return self.due_date.strftime('%A %d %B %Y')