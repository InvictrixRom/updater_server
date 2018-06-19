import inotify.adapters
import time
import hashlib
import json
import re
import os
import zipfile
import datetime

def load_json():
    with open('/root/builds.json') as json_data:
        global builds
        builds = json.load(json_data)

def save_json():
    with open('/root/builds.json', 'w') as json_data:
        json.dump(builds, json_data, sort_keys=True, indent=4)

def add_build(path, name):
    try:
        with zipfile.ZipFile(path, 'r') as update_zip:
            build_prop = update_zip.read('system/build.prop').decode('utf-8')
            timestamp = int(re.findall('ro.build.date.utc=([0-9]+)', build_prop)[0])
            version = re.findall('ro.invictrix.build.version=([a-zA-Z0-9\-\_\.]+)', build_prop)[0]
            buildtype = re.findall('ro.invictrix.buildtype=([a-zA-Z0-9\-\_\.]+)', build_prop)[0]
            device = re.findall('ro.invictrix.device=([a-zA-Z0-9\-\_\.]+)', build_prop)[0]
    except Exception as e:
        print(e)
        timestamp = 1
        version = None
        buildtype = None
        device = "??"

    buildinfo = {}
    buildinfo['sha256'] = sha256_checksum(path)
    buildinfo['sha1'] = sha1_checksum(path)
    buildinfo['size'] = os.path.getsize(path)
    buildinfo['date'] = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    buildinfo['datetime'] = timestamp
    buildinfo['filename'] = name
    buildinfo['filepath'] = 'builds/full/{}/{}'.format(device, name)
    buildinfo['version'] = version
    buildinfo['type'] = buildtype
    buildinfo['incremental'] = False

    builds[device].append(buildinfo)

    save_json()

def sha256_checksum(filename, block_size=257152):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

def sha1_checksum(filename, block_size=257152):
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha1.update(block)
    return sha1.hexdigest()

def _main():
    try:
        for event in i.event_gen():
            (_, type_names, path, filename) = event
            if type_names[0] == "IN_CLOSE_WRITE":
                filePath = "{}/{}".format(path, filename)
                add_build(filePath, filename)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    global i
    i = inotify.adapters.InotifyTree('/var/www/html/builds')

    load_json()
    try:
        while True:
            _main()
            time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting")
