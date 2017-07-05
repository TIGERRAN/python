# -*- coding: utf-8 -*-
import jenkins
import httplib
import xml.etree.cElementTree as et
import os,sys
import json
import time

jenkins_url='http://10.0.2.97:8080'

#user_id='zhaoyan'
#api_token='acea47a18f5b7140d1fb8327a9e2f5a5'
username='tangchengwei'
password='mftour123'

def BuildJob(project_jenkins_name,project_git_branch):
    server = jenkins.Jenkins(jenkins_url, username=username, password=password)

    try:
        job_config1 = server.get_job_config(project_jenkins_name)
        job_config2 = et.fromstring(job_config1.strip())
        new_branch = job_config2.find('scm').find('branches').find('hudson.plugins.git.BranchSpec').find('name')
        new_branch.text = "*/" + project_git_branch
        server.reconfig_job(project_jenkins_name, et.tostring(job_config2))

        # build
        nextBuildNumber = server.get_job_info(project_jenkins_name)['nextBuildNumber']
        o = server.build_job(project_jenkins_name)

        time.sleep(10)
        scan = True
        while scan:
            build_info = server.get_build_info(project_jenkins_name, nextBuildNumber)
            if(build_info['building'] == False):
                result = build_info['result']
                scan = False
                return result
            time.sleep(1)
    except Exception, e:
        print e
        return e

    '''
    begin = True
    while begin:
        running_build_project = server.get_running_builds()
        if len(running_build_project) == 0:
            begin = True

        else:
            begin1 = True
            n = 0
            while begin1:
                time.sleep(0.75)
                rev_list_tmp = []
                output = server.get_build_console_output(project_jenkins_name, nextBuildNumber)
                rev_list = output.split('\n')

                if n == 0:
                    rev_list_last = rev_list
                    rev_list_tmp = rev_list
                    n += 1

                if len(rev_list_last) != len(rev_list):
                    for i in rev_list:
                        if i not in rev_list_last:
                            rev_list_tmp.append(i)
                    rev_list_last = rev_list_last + rev_list_tmp

                if len(rev_list_tmp) != 0:
                    for g in rev_list_tmp:
                        print g

                running_build_project = server.get_running_builds()
                if len(running_build_project) == 0:
                    f1 = open('console.out', 'wb')
                    output_final = server.get_build_console_output(project_jenkins_name, nextBuildNumber)
                    rev_list_final = output.split('\n')
                    for l in rev_list_final:
                        f1.write(l.encode('utf-8') + '\n')
                    f1.close()

                    begin1 = False

            begin = False
    '''
