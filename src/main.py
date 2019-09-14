import os
from pathlib import Path
from time import sleep

from marionette_driver.by import By
from marionette_driver.keys import Keys
from marionette_driver.marionette import Marionette

import mime

BINARY = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
client = Marionette(bin=BINARY, gecko_log="-")
client.start_session()
client.navigate("https://downloadtestfiles.com/")


# https://developer.mozilla.org/ja/docs/Download_Manager_preferences

# ファイルを自動的にダウンロードディレクトリに保存するかどうかを示す真偽値。
# この値が false の場合、ユーザは処理方法を尋ねられます。
client.set_pref("browser.download.useDownloadDir", True)


client.set_pref("browser.helperApps.neverAsk.saveToDisk",
                ",".join(mime.mimeTypes))

# ファイルをダウンロードする既定のフォルダを示します。
# 0 の場合はデスクトップ、
# 1 の場合はシステムの既定ダウンロードフォルダ、
# 2 の場合はユーザ定義フォルダ (browser.download.dir を参照)。
client.set_pref("browser.download.folderList", 2)

# ダウンロードされたファイルの保存先としてユーザが選択したローカルフォルダ。
# 他のブラウザから個人設定を移行すると、このパスが設定される場合があります。
# このフォルダは browser.download.folderList の値が 2 になっている場合のみ有効です。
client.set_pref("browser.download.dir", str(Path("downloads").resolve()))

sleep(5)


def clean_dir(dir: str):
    ls = os.listdir(dir)
    for f in ls:
        os.remove(os.path.join(dir, f))
    print("clean dir succeeded")


clean_dir("downloads")
a = client.find_element("css selector", "body > div > a:nth-child(6)")
a.click()

sleep(15)

client.quit()
