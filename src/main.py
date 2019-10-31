import os
import sys
from pathlib import Path

from marionette_driver.marionette import Actions, Marionette

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

marionette = Marionette(bin=BINARY, gecko_log=NO_LOG, profile=profile)

DOWNLOADS = "downloads"
setup_download_folder(DOWNLOADS)

# firefox52 では MIME_TYPES.rdf, firefox60 では handlers.json に
# ファイルダウンロード時の動作設定が格納されている（プログラムで開く、など）
# 自動ダウンロードするため既存の設定は削除する
DOWNLOAD_ACTION_PREFS = ["MIME_TYPES.rdf", "handlers.json"]
for name in DOWNLOAD_ACTION_PREFS:
    p = os.path.join(marionette.profile_path, name)
    if os.path.isfile(p):
        os.remove(p)

marionette.start_session()

marionette.set_pref("browser.download.useDownloadDir", True)
marionette.set_pref("browser.helperApps.neverAsk.saveToDisk",
                    ",".join(MIME_TYPES))
# 0 の場合はデスクトップ、1 の場合はシステムの既定ダウンロードフォルダ、2 の場合はユーザ定義フォルダ。
marionette.set_pref("browser.download.folderList", 2)
marionette.set_pref("browser.download.dir", str(Path(DOWNLOADS).resolve()))

DOWNLOAD_TEST = "http://xcal1.vodafone.co.uk/"
# marionette.navigate(DOWNLOAD_TEST)

HREF_SCRIPT = f'''
        window.location.href = "{DOWNLOAD_TEST}";
    '''
marionette.execute_script(HREF_SCRIPT)

Actions(marionette).wait(2).perform()

PRELOAD_SCRIPT = "js\\myQuerySelector.js"
script = load_script(PRELOAD_SCRIPT)
if len(script) > 0:
    marionette.execute_script(script, new_sandbox=True)

TEST_SCRIPT = f'''
    (async() => {{
        const tgt2 = await document.$2(".tgt2")
        console.log(tgt2)
        alert(tgt2.textContent)
    }})()
    '''
marionette.execute_script(TEST_SCRIPT, new_sandbox=False)

marionette.quit()
# exec("marionette.quit()")
print("complete")

# ページ遷移のために window.location.href = "url" すると以降の JS は実行されない
# 続けて実行したい場合は、別で execute_script を呼んで実行する必要あり
# その際、引数 new_sandbox=True にしなければならない。
# 以前に実行した JS の結果はリセットされる
