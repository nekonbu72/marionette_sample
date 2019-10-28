import os
import sys
from pathlib import Path
from time import sleep

from marionette_driver.marionette import Marionette, Actions

from download import setup_download_folder
from mime import mimeTypes

BINARY = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
if not os.path.isfile(BINARY):
    print(f"firefox binary ({BINARY}) does not exist")
    sys.exit(0)

# geckodriver の log ファイル出力を抑止する
NO_LOG = "-"

PROFILE = "C:\\Users\\s150209\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\5332jmf7.default"  # 会社PC
# PROFILE = "C:\\Users\\Tomoyuki Nakamura\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\2wsrx870.Default User"  # 自宅PC
if not os.path.isdir(PROFILE):
    print(f"firefox profile ({PROFILE}) does not exist")
    sys.exit(0)

client = Marionette(bin=BINARY, gecko_log=NO_LOG, profile=PROFILE)

DOWNLOADS = "downloads"
setup_download_folder(DOWNLOADS)

# firefox52 では mimeTypes.rdf, firefox60 では handlers.json に
# ファイル読み込み時の動作設定が格納されている
# 自動ダウンロードするため既存の設定は削除する
DOWNLOAD_ACTION_PREFS = ["mimeTypes.rdf", "handlers.json"]
for name in DOWNLOAD_ACTION_PREFS:
    p = os.path.join(client.profile_path, name)
    if os.path.exists(p):
        os.remove(p)

client.start_session()

# ファイルを自動的にダウンロードディレクトリに保存するかどうかを示す真偽値。この値が false の場合、ユーザは処理方法を尋ねられます。
client.set_pref("browser.download.useDownloadDir", True)
# 自動ダウンロードする MIME タイプを指定
client.set_pref("browser.helperApps.neverAsk.saveToDisk",
                ",".join(mimeTypes))
# ファイルをダウンロードする既定のフォルダを示します。
# 0 の場合はデスクトップ、1 の場合はシステムの既定ダウンロードフォルダ、2 の場合はユーザ定義フォルダ。
client.set_pref("browser.download.folderList", 2)
# ダウンロードされたファイルの保存先としてユーザが選択したローカルフォルダ。
client.set_pref("browser.download.dir", str(Path(DOWNLOADS).resolve()))


class MarionetteCommand:
    def __init__(self, type: str, param: str):
        self.__type = type
        self.__param = param

    @property
    def type(self):
        return self.__type

    @property
    def param(self):
        return self.__param


cmd_list = [MarionetteCommand("py", 'client.navigate("http://xcal1.vodafone.co.uk/")'),
            MarionetteCommand("wait", "5"),  # レンダリング待ち
            MarionetteCommand("js", '''
                                    const elm = document.querySelector(
                                        "body > table > tbody > tr:nth-child(16) > td:nth-child(1) > a"
                                        );
                                    elm.click();
                                    '''),
            MarionetteCommand("wait", "20")]  # ダウンロード待ち

for cmd in cmd_list:
    if cmd.type == "js":
        client.execute_script(cmd.param)

    elif cmd.type == "wait":
        action = Actions(client)
        action.wait(int(cmd.param))
        action.perform()

    elif cmd.type == "py":
        exec(cmd.param)

    else:
        pass

client.quit()
print("complete")
