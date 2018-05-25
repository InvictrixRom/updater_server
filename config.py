import os

class Config(object):
    GERRIT_URL = os.environ.get('GERRIT_URL', 'https://review.invictrixrom.com')
    CACHE_DEFAULT_TIMEOUT = os.environ.get('CACHE_DEFAULT_TIMEOUT', '3600')
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST', 'redis')
    CACHE_REDIS_DB = os.environ.get('CACHE_REDIS_DB', 4)
    WIKI_INSTALL_URL = os.environ.get('WIKI_INSTALL_URL', 'https://wiki.lineageos.org/devices/{device}/install')
    WIKI_INFO_URL = os.environ.get('WIKI_INFO_URL', 'https://wiki.lineageos.org/devices/{device}')
    DOWNLOAD_BASE_URL = os.environ.get('DOWNLOAD_BASE_URL', 'https://ota.invictrixrom.com/')
