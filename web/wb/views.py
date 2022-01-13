from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse

import subprocess
from pathlib import Path

# Create your views here.
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


@accept_websocket
def echo_once(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')  # 接收前端发来的数据
            print(message)
            if message == 'backup_all':  # 这里根据web页面获取的值进行对应的操作
                child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                # while child.poll() is None:
                #     # r = child.stdout.readline().decode('utf-8')
                #     # for line in r:
                #     for line in iter(child.stdout.readline, b''):
                #         # sys.stdout.write(str(line))
                #         request.websocket.send(line)  # 发送消息到客户端
                while True:
                    line = child.stdout.readline().strip()
                    request.websocket.send(line)
                    if not line:
                        break
            else:
                request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))
