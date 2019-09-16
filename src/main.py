import os
from pathlib import Path
from time import sleep

from marionette_driver.by import By
from marionette_driver.keys import Keys
from marionette_driver.marionette import Marionette

import mime

BINARY = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
PROFILE = "C:\\Users\\s150209\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\5332jmf7.default"
DOWNLOADS = "downloads"

client = Marionette(bin=BINARY, gecko_log="-")  # , profile=PROFILE)
client.start_session()

# proxy 関係の設定
# client.set_pref("network.proxy.autoconfig_url",
#                 "http://www1.yokohama.sei.co.jp/proxy.pac")
# client.set_pref("network.proxy.type", 2)
# client.set_pref("signon.autologin.proxy", True)

# download 関係の設定
# https://developer.mozilla.org/ja/docs/Download_Manager_preferences
# ファイルを自動的にダウンロードディレクトリに保存するかどうかを示す真偽値。
# この値が false の場合、ユーザは処理方法を尋ねられます。
client.set_pref("browser.download.useDownloadDir", True)
# 自動ダウンロードする MIME タイプを指定
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

client.navigate("http://xcal1.vodafone.co.uk/")
# client.navigate("http://wwwi.sedi.jp/eud_log/")

# レンダリング待ち
sleep(5)

# downloads フォルダを空にする
ls = os.listdir(DOWNLOADS)
for f in ls:
    os.remove(os.path.join(DOWNLOADS, f))
print(f"cleaned {DOWNLOADS} dir")

client.find_element(
    "css selector", "table.dltable > tbody:nth-child(1) > tr:nth-child(16) > td:nth-child(1) > a:nth-child(1)").click()
# "css selector", "div.contentbody:nth-child(6) > a:nth-child(5)").click()

# ダウンロード待ち
sleep(15)
client.quit()
