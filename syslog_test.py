import syslog

# -*- coding:utf-8 -*-
import syslog
import time
import json

OPERATION_LOG = 'AspOperationLog'
TAG = 'OP0'

syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_INFO))
syslog.openlog(OPERATION_LOG, logoption=syslog.LOG_CONS,
               facility=syslog.LOG_LOCAL1)
# Write log   "Time AA0 user module action result detail"
user = 'test'
src_ip = '10.1.1.1'
module = 'test syslog'
result = '0'
action = 'doit'
detail = {
    'target': 'study syslog',
    'msg': 'syslog is perfect'
}

syslog.syslog(syslog.LOG_INFO, '%s %s %s %s %s %s %s "%s"' % (time.strftime(
    '%Y/%m/%d %H:%M:%S'), TAG, user, src_ip, module, action, result, json.dumps(detail)))
# Close
syslog.closelog()
