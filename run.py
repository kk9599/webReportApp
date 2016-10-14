from flask_script import Manager,Server
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import threading,time
import pandas as pd
import glob,os
from apps import app
from apps.model import db,JobName,BuildVersion,TestCase,build_test

manager = Manager(app)
bootstrap= Bootstrap(app)
moment = Moment(app)

server = Server(host="0.0.0.0", port=9000)
manager.add_command("runserver", server)

@manager.command
def Print(jobName=None, buildId=None):
    print("hello command {0},{1}".format(jobName,buildId))
    importFile(jobName,buildId)

def importFile(jobName=None, buildId=None,filePath = 'apps/import/report/*.csv'):
    #threading.Timer(10, importFile).start()
    filelist = glob.glob(filePath)
    #names = [os.path.basename(x) for x in filelist]
    if len(filelist) > 0:
        for file in filelist:
            insertRecord(jobName, buildId,file,'job_track_result')

            # print(names)
            filename = os.path.basename(file)
            print(filename)
			
            try:
                moveFile(file,target='apps/import/report/artifacts/{0}'.format(filename))
            except ValueError as err:
                print(err.args)
			
    else :
         print(time.ctime())

def moveFile(inputFile='import/report/', target='import/report/artifacts/'):
    os.rename(inputFile, target)

def insertRecord( jobName, buildId,inputFile, tableName):
    print("insert Record")
    if inputFile :
        df = pd.read_csv(inputFile)
        print(df.values)
        df = df.drop(df.index[0])
        #df['JobLog'] = 'Joblog'
        df['JobName'] = jobName
        df['BuildId'] = buildId
        df.to_sql(tableName, db.engine, index=False, if_exists='append')

    else :
        print("error files")
    # engine = sqlalchemy.create_engine('sqlite:///apps/chart.db')
    # df.to_sql('pr_payrun_job_track', engine, if_exists='append')

def check_record(fuc):
      def isNewRecord(*args, **kwargs):
            JobName_exists = db.session.query(JobName.jobName).filter_by(jobName='{0}'.name).scalar() is not None

      return isNewRecord


app.config['DEBUG'] = True # Ensure debugger will load.
if __name__ == '__main__':
    manager.run()