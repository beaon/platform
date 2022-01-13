# !usr/bin/env python
# -*- coding:utf-8 _*-
import sys
import shlex
import subprocess
from pathlib import Path

tank_smoke = "tankmaoyan.air"
script_path = r"E:\mywork\2022.01.07\AirtestIDE-win-1.2.13\AirtestIDE\my_scripts"
script_name = Path(script_path) / tank_smoke
print('脚本路径是：', script_name)

script_log = Path(script_path) / 'log'
print('脚本执行log的路径：', script_log)

log_path = Path(script_path) / 'logfile'
logfile = open(log_path, 'w')

report_path = Path(script_path) / 'report'

cmd = ["airtest", "run", str(script_name), "--device", "Android:///", "--log", str(script_log), "--recording"]
# cmd = shlex.split(cmd) linux下
print('处理执行air脚本', cmd)

child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while child.poll() is None:
    # r = child.stdout.readline().decode('utf-8')
    # for line in r:
    for line in iter(child.stdout.readline, b''):
        # sys.stdout.write(str(line))
        print(line)
        logfile.write(str(line))
child.wait()
print('脚本执行完成')

report_cmd = ["airtest", "report", str(script_name), "--log_root", str(script_log), "--lang", "zh", "--export",
              str(report_path)]
child1 = subprocess.Popen(report_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
child1.wait()
print('报告执行完成')

