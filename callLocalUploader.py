import sys, getopt, os, json, requests, zipfile

def getUploaderInfo(uploaderName, platform):
    dir_path = os.path.dirname(__file__)
    with open(os.path.join(dir_path, 'uploader.json')) as json_file:
        data = json.load(json_file)
        if uploaderName in data:
            return data[uploaderName].get(platform)


def installUploader(uploaderInfo):
    tmpPackFilePath = os.path.join(os.path.dirname(__file__), 'tmp', uploaderInfo['pack_name'])
    uploaderPathDir = os.path.join(os.path.dirname(__file__),
                               os.path.dirname(uploaderInfo['executable_path']).split(os.path.sep)[0])
    try:
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'tmp')):
            os.makedirs(os.path.join(os.path.dirname(__file__), 'tmp'));
            print('Created the tmp directory.')

        # download the uploader
        r = requests.get(uploaderInfo['url'], stream=True)
        with open(tmpPackFilePath, 'wb') as f:
            f.write(r.content)
        print('Downloaded the uploader pack.')
    
        # unzip the uploader
        zip_file = zipfile.ZipFile(tmpPackFilePath, 'r')
        zip_file.extractall(uploaderPathDir)
        print('Unzipped the uploader pack.')
        zip_file.close()

        os.remove(tmpPackFilePath)
        print("Removed the uploader pack.")
    except Exception as e:
        print(e)
        print('Failed to install the uploader.')
        sys.exit(2)

def main(argv):
    uploaderPath = ''
    uploaderName = ''

    # get the parameters
    try:
        opts, args = getopt.getopt(argv, "p:n:", ["path=", "name="])
    except getopt.GetoptError:
        print('callLocalUploader.py -p <uploadPath> -n <uploadName>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--path"):
            uploaderPath = arg
        elif opt in ("-n", "--name"):
            uploaderName = arg
    
    if uploaderPath != '':
        if (sys.platform == 'win32'):
            os.popen('powershell Start-Process -FilePath ' + uploaderPath)
        elif (sys.platform == 'darwin'):
            os.popen(uploaderPath)
        elif (sys.platform == 'linux'):
            os.popen(uploaderPath)
    
    if uploaderName != '':
        if (sys.platform == 'win32'):
            uploaderInfo = getUploaderInfo(uploaderName, 'win')
            if uploaderInfo is None:
                print("Don't find the " + uploaderName + " (win) in uploader.json.")
                sys.exit(2)

            uploaderPath = os.path.join(os.path.expanduser('~'), '.superide/uploaders', uploaderInfo['executable_path'])
            if (os.path.exists(uploaderPath) is False):
                installUploader(uploaderInfo)
                os.popen('powershell Start-Process -FilePath ' + uploaderPath)
            else:
                os.popen('powershell Start-Process -FilePath ' + uploaderPath)

        elif (sys.platform == 'linux'):
            uploaderInfo = getUploaderInfo(uploaderName, 'linux')
            if uploaderInfo is None:
                print("Don't find the " + uploaderName + " (linux) in uploader.json.")
                sys.exit(2)

            uploaderPath = os.path.join(os.path.expanduser('~'), '.superide/uploaders', uploaderInfo['executable_path'])
            if (os.path.exists(uploaderPath) is False):
                installUploader(uploaderInfo)
                os.popen(uploaderPath)
            else:
                os.popen(uploaderPath)

        elif (sys.platform == 'darwin'):
            uploaderInfo = getUploaderInfo(uploaderName, 'darwin')
            if uploaderInfo is None:
                print("Don't find the " + uploaderName + " (darwin) in uploader.json.")
                sys.exit(2)

            uploaderPath = os.path.join(os.path.expanduser('~'), '.superide/uploaders', uploaderInfo['executable_path'])
            if (os.path.exists(uploaderPath) is False):
                installUploader(uploaderInfo)
                os.popen(uploaderPath)
            else:
                os.popen(uploaderPath)


if __name__ == "__main__":
    main(sys.argv[1:])