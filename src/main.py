from download import setup_download_folder
from script import load_script
from userprofile import profile_dir
from puppeteer import Puppet

BINARY = "C:\\Program Files\\Mozilla Firefox\\firefox.exe@"
profile = profile_dir()

puppet = Puppet(BINARY, profile)
if puppet is None:
    print("yeah")

DOWNLOAD = "download"
setup_download_folder(DOWNLOAD)
SCRIPT = "scripts\\sample.py"
script = load_script(SCRIPT)

puppet.start()
puppet.exec(script, DOWNLOAD)
puppet.quit()
