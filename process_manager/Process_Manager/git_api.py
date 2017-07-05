# -*- coding: utf-8 -*-
import httplib
import json
import os
import ConfigParser

def getUrl():
    config = ConfigParser.ConfigParser()
    config.read('mfops.conf')
    Gitlab_url = config.get('gitlab','ip')
    Gitlab_api_url = config.get('gitlab','api_url')
    return Gitlab_url,Gitlab_api_url

def getGitProjectIDBySSH(ssh_url):
    Gitlab_url,Gitlab_api_url = getUrl()
    try:
        project_git_namespace = ssh_url.split(':')[1].split('/')[0]
        project_git_name = ssh_url.split('/')[-1].split('.')[0]
        url = Gitlab_api_url + 'projects/%s%%2F%s' % (project_git_namespace,project_git_name)
        conn = httplib.HTTPConnection(Gitlab_url)
        conn.request(method='GET',url=url,headers={"PRIVATE-TOKEN":"kK6619Ut8xfF8AZCiphS"})
        res = conn.getresponse()
        res_json = json.loads(res.read())
        id = res_json['id']
        conn.close()
        return id
    except Exception, e:
        print e
    finally:
        conn.close()

def getGitProjectBranchesByID(id):
    Gitlab_url,Gitlab_api_url = getUrl()
    conn = httplib.HTTPConnection(Gitlab_url)
    try:
        url = Gitlab_api_url + 'projects/%s/repository/branches' % (str(id))
        conn = httplib.HTTPConnection(Gitlab_url)
        conn.request(method='GET',url=url,headers={"PRIVATE-TOKEN":"kK6619Ut8xfF8AZCiphS"})
        res = conn.getresponse()
        res_josn = json.loads(res.read())
        dt_list = list()
        for branch in res_josn:
            dt_list.append(branch['name'])
        conn.close()
        return  dt_list
    except Exception, e:
        print e
    finally:
        conn.close()

