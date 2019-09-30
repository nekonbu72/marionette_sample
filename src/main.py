import os
from pathlib import Path
from time import sleep

from marionette_driver.marionette import Marionette

import mime

BINARY = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
PROFILE = "C:\\Users\\s150209\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\5332jmf7.default"
# PROFILE = "C:\\Users\\Tomoyuki Nakamura\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\2wsrx870.Default User"
DOWNLOADS = "downloads"

# ff52 では mimeTypes.rdf, ff60 では handlers.json に
# ファイル読み込み時の動作設定を格納している
DOWNLOAD_ACTION_PREFS = ["mimeTypes.rdf", "handlers.json"]

client = Marionette(bin=BINARY, gecko_log="-", profile=PROFILE)

for name in DOWNLOAD_ACTION_PREFS:
    p = os.path.join(client.profile_path, name)
    if os.path.exists(p):
        os.remove(p)

client.start_session()

# proxy 関係の設定
# client.set_pref("network.proxy.autoconfig_url",
#                 "http://www1.yokohama.sei.co.jp/proxy.pac")
# client.set_pref("network.proxy.type", 2)
# client.set_pref("signon.autologin.proxy", True)

# download 関係の設定

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
sleep(3)

# downloads フォルダを空にする
ls = os.listdir(DOWNLOADS)
for f in ls:
    os.remove(os.path.join(DOWNLOADS, f))
print(f"cleaned {DOWNLOADS} dir")

with open('js\\click.js') as file:
    dt = file.read()

client.execute_script(dt)

# ダウンロード待ち
sleep(30)
client.quit()
