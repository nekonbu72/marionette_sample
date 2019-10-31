import shlex
import subprocess

from marionette_driver.marionette import Actions, Marionette

cmd = '"C:\\Program Files\\Mozilla Firefox\\firefox.exe" -marionette'
hundler = subprocess.Popen(shlex.split(cmd))

BINARY = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
client = Marionette('localhost', port=2828)  # , bin=BINARY)
client.start_session()
client.navigate("https://www.google.co.jp/")

whs = client.window_handles
cw = client.current_window_handle

hundler.kill()
