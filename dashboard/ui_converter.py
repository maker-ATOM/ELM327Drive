import subprocess

subprocess.check_output(['pyuic5', '-o', 'dashboard_ui.py', 'dashboard.ui'])
