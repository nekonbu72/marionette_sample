from pathlib import Path

from marionette_driver.marionette import Actions, Marionette

from mime import MIME_TYPES


class Puppet:
    def __init__(self, binary: str, profile: str):
        if not Path(binary).is_file():
            return None

        if not Path(profile).is_dir():
            return None

        # geckodriver の log ファイル出力を抑止する
        NO_LOG = "-"

        self.marionette = Marionette(
            bin=binary, gecko_log=NO_LOG, profile=profile)

    def start(self):
        self.marionette.start_session()

    def exec(self, script: str, download: str = None):
        if not download is None:
            # firefox52 では MIME_TYPES.rdf, firefox60 では handlers.json に
            # ファイルダウンロード時の動作設定が格納されている（プログラムで開く、など）
            # 自動ダウンロードするため既存の設定は削除する
            DOWNLOAD_ACTION_PREFS = ["MIME_TYPES.rdf", "handlers.json"]
            for name in DOWNLOAD_ACTION_PREFS:
                p = Path(self.marionette.profile_path).joinpath(name)
                if p.is_file():
                    p.unlink()

            self.marionette.set_pref("browser.download.useDownloadDir", True)
            self.marionette.set_pref("browser.helperApps.neverAsk.saveToDisk",
                                     ",".join(MIME_TYPES))
            # 0 の場合はデスクトップ、1 の場合はシステムの既定ダウンロードフォルダ、2 の場合はユーザ定義フォルダ
            self.marionette.set_pref("browser.download.folderList", 2)
            self.marionette.set_pref("browser.download.dir",
                                     str(Path(download).resolve()))

        exec(script)

    def wait(self, seconds):
        actions = Actions(self.marionette)
        actions.wait(seconds).perform()

    def quit(self):
        self.marionette.quit()
