from apps import app,api
from flask import render_template,request,abort,send_file
from apps.model import JobTrackResult,BuildVersion,JobName,TestCase,build_test
import glob,os
from apps.api.v1.chart import *
from apps.task import add


@app.route("/")
def apiRedirect():
    return send_file('partial_templates/index.html')

@app.route("/<path:template>")
def apiTemplate(template):
    filelist = glob.glob('partial_templates/*.html')
    template = "{0}.html".format(template)
    filelist_child = glob.glob('partial_templates/*/*.html')
    filelist.extend(filelist_child)
    filename = [os.path.basename(x) for x in filelist]
    if(template in filename):
        return  send_file('partial_templates/{0}.html'.format(template))
    else:
        return abort(404)



@app.route("/<int:id>")
def getChart(id):
    # return jsonify([dict(type="column", dataPoints=[
    #     dict(label="performanceTest 20160727214650 (4) 01-00", y=int(id)),
    #     dict(label="performanceTest 20160727214650 (3) 01-00", y=4181),
    #     dict(label="performanceTest 20160727214650 (1) 01-00", y=4237)
    #
    # ])])
    result= add.delay(id,id)
    #result = importFileCelery('celery', 9999)
    return render_template('main.html',result =result.wait(timeout=2))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'),404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'),500

@app.route('/chart',methods=['POST','GET'])
def renderChart():
    jobName = request.args.get('jobName')
    buildName = request.args.get('buildName')
    testName =request.args.get('testName')
    joblist = JobTrackResult.query.filter(JobName.JobName==jobName, BuildVersion.buildName==buildName,
                                          TestCase.testName==testName
                                          ).all()

    if len(joblist)> 0 :
       return render_template('chart.html',joblist=joblist )
    else:
        return abort(500)

@app.route('/testCases', methods=['POST','GET'])
def testCaseMenu():
    jobName=request.args.get('jobName')
    buildName= request.args.get('buildName')
    build= BuildVersion.query.join(JobName).filter(JobName.jobName==jobName, BuildVersion.buildName==buildName).first_or_404()
    test_list = TestCase.query.filter(TestCase.builds.any(buildId=build.buildId)).all()
    return render_template('testCaseMenu.html',testList=test_list)


@app.route('/plot',methods=['POST','GET'])
def renderPlotyChart():
    # jobName = request.args.get('jobName')
    # buildName = request.args.get('buildName')
    testjob =request.args.get('testjob')
    joblist = JobTrackResult.query.filter(JobTrackResult.testJob==testjob).all()

    if len(joblist)> 0 :
       return render_template('plotlyChart.html',joblist=joblist )
    else:
        return abort(500)

api.add_resource(jobResult, '/api/job')



def isTemplate_path(template_name):
        filelist = glob.glob('partial_templates/*.html')
        template_name = "{0}.html".format(template_name)
        filelist_child = glob.glob('partial_templates/*/*.html')
        filelist.extend(filelist_child)
        filename = [os.path.basename(x) for x in filelist]
        return template_name in filename
