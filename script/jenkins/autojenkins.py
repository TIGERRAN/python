#!/usr/bin/env python

import jenkins
import httplib
import xml.etree.cElementTree as et
import os,sys
import json
import time

Jenkins_url = 'http://10.0.2.97:8080'
Gitlab_url = '10.0.18.4'
Gitlab_api_url = 'http://10.0.18.4/api/v3/'

def GetprojectAll():    

	#get project'name by path
	path = sys.path[0]
	project_jenkins_name = path.split('/')[-1]

	#
	server = jenkins.Jenkins(Jenkins_url,username='tangchengwei',password='20a2345ae3e1d879587421a4de3bf26d')
	job_jenkins_config = server.get_job_config(project_jenkins_name)
	job_new_config = et.fromstring(job_jenkins_config.strip())
	job_git_url = job_new_config.find('scm').find('userRemoteConfigs').find('hudson.plugins.git.UserRemoteConfig').findtext('url')
	job_git_branch = job_new_config.find('scm').find('branches').find('hudson.plugins.git.BranchSpec').findtext('name')
	project_git_namespace = job_git_url.split(':')[1].split('/')[0]
	project_git_name = job_git_url.split('/')[-1].split('.')[0]
	project_jenkins_branch = job_git_branch.split('/')[-1]
	
	#get gilab'project id
	conn = httplib.HTTPConnection(Gitlab_url)
	url1 = Gitlab_api_url + 'projects/%s%%2F%s' % (project_git_namespace,project_git_name)
	conn.request(method='GET',url=url1,headers={"PRIVATE-TOKEN":"kK6619Ut8xfF8AZCiphS"})
	res1 = conn.getresponse()
	res = json.loads(res1.read())
	project_git_id = res['id']

	return {
			'project_jenkins_name': project_jenkins_name,
			'project_git_name': project_git_name,
			'project_jenkins_branch': project_jenkins_branch,
			'project_git_id': project_git_id,
			'project_git_namespace': project_git_namespace,
			}  

def CheckGitBranch(git_branch):

	config = GetprojectAll()
	project_git_id = config['project_git_id']

	project_new_branch = git_branch

	conn = httplib.HTTPConnection(Gitlab_url)
	url1 = Gitlab_api_url + "projects/%s/repository/branches/%s" % (str(project_git_id),project_new_branch)
	conn.request(method='GET',url=url1,headers={"PRIVATE-TOKEN":"kK6619Ut8xfF8AZCiphS"})
	res1 = conn.getresponse()
	res = json.loads(res1.read())
	return res.get('name')
	
def ChangeBuild(git_branch=GetprojectAll()['project_jenkins_branch']):

	config = GetprojectAll()
	project_jenkins_name = config['project_jenkins_name']
	old_branch = config['project_jenkins_branch']	
	server = jenkins.Jenkins(Jenkins_url,username='tangchengwei',password='mftour123')
	job_config1 = server.get_job_config(project_jenkins_name)
	job_config2 = et.fromstring(job_config1.strip())
	new_branch = job_config2.find('scm').find('branches').find('hudson.plugins.git.BranchSpec').find('name') 
	new_branch.text = "*/" + git_branch
	server.reconfig_job(project_jenkins_name,et.tostring(job_config2))

	print '''
---------------------------------------------------------------------
    old_branch   |     %s                                              
---------------------------------------------------------------------
    new_branch   |     %s
---------------------------------------------------------------------
	''' % (old_branch,git_branch)

	#build
	nextBuildNumber = server.get_job_info(project_jenkins_name)['nextBuildNumber']
	server.build_job(project_jenkins_name)
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
				output = server.get_build_console_output(project_jenkins_name,nextBuildNumber)
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
					f1 = open('console.out','wb')
					output_final = server.get_build_console_output(project_jenkins_name,nextBuildNumber)
					rev_list_final = output.split('\n')
					for l in rev_list_final:
						f1.write(l.encode('utf-8')+'\n')
					f1.close()

					begin1 = False			
			
			begin = False	



if __name__ == '__main__':

	if len(sys.argv) == 1:
		git_conf_file = r'config.conf'
		if os.path.exists(git_conf_file):
			f = open('config.conf','r')
			git_branch = f.read()
			ChangeBuild(git_branch)
		else:
			ChangeBuild()

	elif len(sys.argv) == 2:
		git_branch = sys.argv[1]
		
		res = CheckGitBranch(git_branch)
		if res == git_branch:
			f = open('config.conf','wb')
			f.write(git_branch)
			f.close()
			ChangeBuild(git_branch)
		elif res == None:
			print "The branch %s is not exist in Gitlab" % git_branch
	else:
		pass







