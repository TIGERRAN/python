# -*- coding: utf-8 -*-
from datetime import *
import os,re
from apscheduler.schedulers.blocking import BlockingScheduler
import threading
from .db_backup_info import setStatusById,getStatusById,setRunningById,getDBBackupInfoById
import commands
from time import sleep

scheduler = BlockingScheduler()

def A_backup(id):
    if checkShFile(id) == False:
        return False
    startAutoBackup(id)

def M_backup(id):
    if checkShFile(id) == False:
        return False
    info = getDBBackupInfoById(id)

    t = threading.Thread(target=job_dbbackup, args=[id,info['name']])
    t.setDaemon(True)
    t.start()

def checkShFile(id):
    info = getDBBackupInfoById(id)

    baseDir = os.path.dirname(os.path.abspath(__name__))
    sh_dir = os.path.join(baseDir, 'static', 'DBbackup_shell')
    filename = os.path.join(sh_dir, info['name'] + '.sh')

    exists = os.path.exists(filename)
    return exists

def todo():
    scheduler.daemonic = False
    if(scheduler.running == False):
        scheduler.start()

st = threading.Thread(target=todo,name='db_backup_thread')
scheduler = BlockingScheduler()

def job_dbbackup(id,name):
    setRunningById(id, 1)

    baseDir = os.path.dirname(os.path.abspath(__name__))
    sh_dir = os.path.join(baseDir, 'static', 'DBbackup_shell')
    filename = os.path.join(sh_dir, name + '.sh')
    status, output = commands.getstatusoutput(filename)

    setRunningById(id, 0)

def startAutoBackup(id):
    setStatusById(id, 1)
    #scheduler.add_job(job_dbbackup, 'cron', args=[name], day_of_week='*', hour='*', minute='*', second='*/3', id=name)

    dt = getDBBackupInfoById(id)
    timeTuple = datetime.strptime(dt['time'], '%H:%M')
    scheduler.add_job(job_dbbackup, 'cron', args=[id,dt['name']], day_of_week=dt['rate'], hour=timeTuple.hour, minute=timeTuple.minute, id=id)

    if st.isAlive() == False:
        st.start()

def stopAutoBackup(id):
    k = scheduler.get_job(id)
    if k:
        scheduler.remove_job(id)
    setStatusById(id, 0)
    #scheduler.remove_all_jobs()
    #scheduler.shutdown(wait=False)

# ----------- 源码  -------------------------------
#   def add_job(self, func, year=None, month=None, day=None, week=None,
#                    day_of_week=None, hour=None, minute=None, second=None,
#                    start_date=None, args=None, kwargs=None, **options):
#       """
#       Schedules a job to be completed on times that match the given
#       expressions.
#
#       :param func: callable to run
#       :param year: year to run on
#       :param month: month to run on
#       :param day: day of month to run on
#       :param week: week of the year to run on
#       :param day_of_week: weekday to run on (0 = Monday)
#       :param hour: hour to run on
#       :param second: second to run on
#       :param args: list of positional arguments to call func with
#       :param kwargs: dict of keyword arguments to call func with
#       :param name: name of the job
#       :param jobstore: alias of the job store to add the job to
#       :param misfire_grace_time: seconds after the designated run time that
#           the job is still allowed to be run
#       :return: the scheduled job
#       :rtype: :class:`~apscheduler.job.Job`
#       """