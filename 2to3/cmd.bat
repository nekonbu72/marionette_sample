@echo off

python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\marionette_driver"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\mozrunner"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\mozdevice"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\mozlog"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\blessings"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\six"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\mozterm"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\mozfile"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\mozinfo"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\mozprocess"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\mozprofile"
python "C:\\Program Files\\anaconda3\\Tools\\scripts\\2to3.py" -W -n -f all -f raise -f import ".venv\\Lib\\site-packages\\mozversion"

copy .\\2to3\\modified\\marionette_driver\\geckoinstance.py .venv\\Lib\\site-packages\\marionette_driver\\geckoinstance.py
copy .\\2to3\\modified\\marionette_driver\\marionette.py    .venv\\Lib\\site-packages\\marionette_driver\\marionette.py
copy .\\2to3\\modified\\marionette_driver\\transport.py     .venv\\Lib\\site-packages\\marionette_driver\\transport.py
copy .\\2to3\\modified\\mozprocess\\processhandler.py       .venv\\Lib\\site-packages\\mozprocess\\processhandler.py
copy .\\2to3\\modified\\mozprocess\\winprocess.py           .venv\\Lib\\site-packages\\mozprocess\\winprocess.py
copy .\\2to3\\modified\\six.py                              .venv\\Lib\\site-packages\\six.py