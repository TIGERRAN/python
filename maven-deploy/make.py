#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
import os,sys
import re

def checkConfig(project,*args):
    config = ConfigParser.SafeConfigParser()
    conf_file = os.path.dirname(os.path.realpath(__file__))[0:-3] + 'project/' + project + '/conf/info.conf'
    config.read(conf_file)
    if len(args) == 1:
        change_branch = args[0]
        config.set('git','git_branch',change_branch)
        config.write(open(conf_file,'w'))

    mission_list = {}
    mission_list['getSrc'] = [config.get('git','git_repo'),config.get('git','git_branch')]
    if config.get('global','make_triger') == "True":
        if len(config.options('make_before_shell')) > 0:
            mission_list['before_shell'] = []
            for item in config.options('make_before_shell'):
                mission_list['before_shell'].append(config.get('make_before_shell',item))
        else:
            mission_list['before_shell'] = []

        mission_list['make'] = []
        mission_list['make'].append(config.get('maven','mvn_args'))

        if len(config.options('make_after_shell')) > 0:
            mission_list['after_shell'] = []
            for item in config.options('make_after_shell'):
                mission_list['after_shell'].append(config.get('make_after_shell',item))
        else:
            mission_list['after_shell'] = []

    else:
        pass


    return mission_list

def getSrc(project,git_repo,git_branch):
    src_dir = os.path.dirname(os.path.realpath(__file__))[0:-3] + 'project/' + project + '/src'
    print '''
 ---------------------------------------------------------------------
    make_branch   |     %s
 ---------------------------------------------------------------------
    ''' % (git_branch)

    os.system('(cd %s && rm -rf `ls -a | grep -E -v ^[.]\{1,2\}$` &> /dev/null)' % src_dir )
    os.system('git clone -b %s %s %s || mkdir -p %s' % (git_branch,git_repo,src_dir,src_dir))
    if not os.listdir(src_dir):
        print "the %s is exist in gitlab!!!!" % git_branch
        return False
    else:
        return True

def make(project,mvn_args):
    src_dir = os.path.dirname(os.path.realpath(__file__))[0:-3] + 'project/' + project + '/src'
    os.system('mvn %s -f %s | tee %s_console.out' %(mvn_args,src_dir,project))
    f = open('%s_console.out' % project,'rb')
    for file in f.readlines():
        build_res1 = re.search(r'BUILD (.*)',file)
        if build_res1:
            build_res = build_res1.group(1)

    if build_res == "SUCCESS":
        return True
    elif build_res == "FAILURE":
        return False


def before_shell(*args):
    for item in args:
        os.system(item)



def after_shell(*args):
    for item in args:
        os.system(item)




def get_args():

    try:
        if len(sys.argv) == 3:
            new_branch = sys.argv[2]
            project = sys.argv[1]
            checkConfig(project,new_branch)
            return project

        elif len(sys.argv) == 2:
            project = sys.argv[1]
            checkConfig(project)
            return project
    except ConfigParser.NoSectionError:
        print "the %s is exist!!!!!" % project
    else:
        pass



# mission_list = checkConfig('trade_service')
# print mission_list

if __name__ == '__main__':

    if get_args() != None:
        project = get_args()

        #get info_dict
        mission_list = checkConfig(project)

        getSrc_res = getSrc(project,mission_list['getSrc'][0],mission_list['getSrc'][1])
        if getSrc_res == True:
            if len(mission_list['before_shell']) != 0:
                before_shell(*mission_list['before_shell'])

            make(project,mission_list['make'][0])

            if len(mission_list['after_shell']) != 0:
                after_shell(*mission_list['after_shell'])


    else:
        pass






# os.system('rm -rf /home/tangchengwei/.m2/repository/com/pzj')
# getsrc_res = getSrc('travel_pc','git@10.0.18.4:mftour/travel-pc.git','feature/feature1.4.2')
# if getsrc_res == True:
    # build_res = make('travel_pc','clean package -Dmaven.test.skip=True')
    # print build_res


