import os
import logging

logger = logging.getLogger(__name__)

BASE_ARCHIVE_PATH = './data/'

def getApplicationArchivePath(name):
    name = removeSpace(name)
    path = BASE_ARCHIVE_PATH + name

    return path

def getServiceArchivePath(service_name, application_name):
    service_name = removeSpace(service_name)
    application_name = removeSpace(application_name)
    path = BASE_ARCHIVE_PATH + application_name + '/' + service_name

    return path

def removeSpace(s):
    arr = s.split(' ')
    final_s = ''
    for ele in arr:
        if ele != ' ':
            final_s = final_s + ele

    return final_s

def makeDir(path):
    resp = True
    try:  
        mode = 0o666
        os.makedirs(path, mode)
        logger.info("Success - created dir -> "+path)  
    except OSError as error:  
        logger.error(error) 
        resp = False

    return resp