from flask_sqlalchemy import SQLAlchemy
import datetime
from apps import app
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'chart.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
#db.Model.metadata.reflect(db.engine)

class JobTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    PayRunId= db.Column(db.INTEGER)
    PayGroupName = db.Column(db.String(255))
    NumEmpl = db.Column(db.INTEGER,)
    JobMode = db.Column(db.String(80))
    ExecutionTime=db.Column(db.INTEGER)
    JobStatus= db.Column(db.String(80))
    QueueTime=db.Column(db.DateTime)
    StartTime=db.Column(db.DateTime)
    EndTime=db.Column(db.DateTime)
    JobLog=db.Column(db.TEXT)
    JobName = db.Column(db.String(255), default='demo')
    BuildId = db.Column(db.INTEGER, nullable=False)

    def __init__(self, jobname, buildid):
        self.JobName = jobname
        self.BuildId = buildid

    def __repr__(self):
        return '<Job %r>' % self.JobName


class JobName(db.Model):
      jobId= db.Column(db.Integer,primary_key=True)
      jobName= db.Column(db.String(255),unique=True)
      createdTime = db.Column(db.DateTime,default=datetime.datetime.utcnow)
      build = db.relationship('BuildVersion',backref='job_name',lazy='dynamic')

      def __init__(self, jobname):
        self.jobName = jobname

      def __repr__(self):
        return '<Job %r>' % self.jobName

build_test = db.Table('build_test',
                      db.Column('build_id',db.Integer,db.ForeignKey('build_version.buildId')),
                      db.Column('test_id', db.Integer,db.ForeignKey('test_case.testId'))
                      )

class BuildVersion(db.Model):
      buildId=db.Column(db.Integer,primary_key=True)
      buildName = db.Column(db.String(255),unique=True)
      createdTime = db.Column(db.DateTime,default=datetime.datetime.utcnow )
      jobBuild= db.Column(db.Integer,db.ForeignKey('job_name.jobId'))
      test= db.relationship('TestCase',secondary=build_test,
                            backref=db.backref('builds',lazy='dynamic'))

      def __init__(self, buildname):
        self.buildName = buildname

      def __repr__(self):
        return '<buildName %r>' % self.buildName

class TestCase(db.Model):
      testId= db.Column(db.Integer,primary_key=True)
      testName = db.Column(db.String(255),unique=True)
      createdTime=db.Column(db.DateTime,default=datetime.datetime.utcnow )
      jobTrackResults= db.relationship('JobTrackResult',backref='test_case',lazy='dynamic')


      def __init__(self, testname):
        self.testName = testname

      def __repr__(self):
        return '<testName %r>' % self.testName

class JobTrackResult(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      PayRunId= db.Column(db.INTEGER)
      PayGroupName = db.Column(db.String(255))
      NumEmpl = db.Column(db.INTEGER,)
      JobMode = db.Column(db.String(80))
      ExecutionTime=db.Column(db.INTEGER)
      JobStatus= db.Column(db.String(80))
      QueueTime=db.Column(db.DateTime)
      StartTime=db.Column(db.DateTime)
      EndTime=db.Column(db.DateTime)
      JobLog=db.Column(db.TEXT)
      testJob= db.Column(db.Integer,db.ForeignKey('test_case.testId'))

      def __init__(self, testid):
        self.testJob= testid


      def __repr__(self):
        return '<id %r>' % self.id