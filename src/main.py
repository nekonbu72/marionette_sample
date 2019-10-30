import os
import sys
from pathlib import Path

from marionette_driver.marionette import Marionette

from download import setup_download_folder
from javascript import load_script
from mime import MIME_TYPES
from userprofile import profile_dir

BINARY = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
if not os.path.isfile(BINARY):
    print(f"firefox binary ({BINARY}) does not exist")
    sys.exit(0)

# geckodriver の log ファイル出力を抑止する
NO_LOG = "-"

profile = profile_dir()
if not os.path.isdir(profile):
    print(f"firefox profile ({profile}) does not exist")
    sys.exit(0)

client = Marionette(bin=BINARY, gecko_log=NO_LOG, profile=profile)

DOWNLOADS = "downloads"
setup_download_folder(DOWNLOADS)

# firefox52 では MIME_TYPES.rdf, firefox60 では handlers.json に
# ファイル読み込み時の動作設定が格納されている
# 自動ダウンロードするため既存の設定は削除する
DOWNLOAD_ACTION_PREFS = ["MIME_TYPES.rdf", "handlers.json"]
for name in DOWNLOAD_ACTION_PREFS:
    p = os.path.join(client.profile_path, name)
    if os.path.exists(p):
        os.remove(p)

client.start_session()

# ファイルを自動的にダウンロードディレクトリに保存するかどうかを示す真偽値。この値が false の場合、ユーザは処理方法を尋ねられます。
client.set_pref("browser.download.useDownloadDir", True)
# 自動ダウンロードする MIME タイプを指定
client.set_pref("browser.helperApps.neverAsk.saveToDisk",
                ",".join(MIME_TYPES))
# ファイルをダウンロードする既定のフォルダを示します。
# 0 の場合はデスクトップ、1 の場合はシステムの既定ダウンロードフォルダ、2 の場合はユーザ定義フォルダ。
client.set_pref("browser.download.folderList", 2)
# ダウンロードされたファイルの保存先としてユーザが選択したローカルフォルダ。
client.set_pref("browser.download.dir", str(Path(DOWNLOADS).resolve()))

DOWNLOAD_TEST = "http://xcal1.vodafone.co.uk/"
client.navigate(DOWNLOAD_TEST)

PRELOAD_SCRIPT = "js\\myQuerySelector.js"
script = load_script(PRELOAD_SCRIPT)
if len(script) > 0:
    client.execute_script(script, new_sandbox=False)

TEST_SCRIPT = '''
    document.$2(".tgt2").then(console.log)
    '''
client.execute_script(TEST_SCRIPT, new_sandbox=False)

client.quit()
print("complete")
