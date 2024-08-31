import logging

logger = logging.getLogger(__name__)

def getFileMetadata(file_path: str):
    indx = file_path.rindex('/')
    fullfileName = file_path[indx+1:]
    fileName = fullfileName[:fullfileName.rindex('.')]
    extension = fullfileName[fullfileName.rindex('.')+1:]
    
    metadata = {
        'path': file_path[:indx+1],
        'filename': fileName,
        'extension': extension    
    }

    logger.info('file_path:'+file_path+', metadata:'+str(metadata))
    return metadata

def getArchiveFilepath(filemeta: dict, archive_path: str, curr_datetime: str):
    archive_file_path = archive_path + '/' + filemeta['filename'] + curr_datetime + '.' + filemeta['extension']
    return archive_file_path