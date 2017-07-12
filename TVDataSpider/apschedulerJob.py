# 会在数据库中生成apscheduler_jobs表，如果每次启动都执行add_job函数，则会在数据库中存放多个相同的作业，比如my_job1会存在多条记录，就会被反复调用，相当于并行执行了。

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from TVDataSpider.constant import Logger
from TVDataSpider.grabber import grabData

class Scheduler():
    # 使用mysql存储作业
    url = 'mysql://root:sq1357902@118.89.182.156/stock'

    jobstores = {
        'default': SQLAlchemyJobStore(url = url)
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }

    sched = BackgroundScheduler(jobstores = jobstores, executors = executors, job_defaults = job_defaults)
    if sched.get_job('GrabData') == None:
        try:
            sched.add_job(grabData, 'cron', day='*', hour=3, id='GrabData')
            sched.start()
            Logger.sechdLogger.info('*************定时任务已启动*************')
        except (KeyboardInterrupt, SystemExit):
            Logger.sechdLogger.exception('定时任务出错:')
            sched.remove_all_jobs()
            sched.shutdown()