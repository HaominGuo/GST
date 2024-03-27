# -*- coding: utf-8 -*-
# @Time       : 2024/3/9 9:53
# @Author     : 郭豪敏
# @FileName   : auto_run.py
# @Software   : PyCharm
# @Description：
import subprocess
import os

# 工程字典，键为工程名，值为一个包含类型、主脚本或命令和路径的元组
projects = {
    "pre-processing": ('.py', "text_to_json.py", "./pre-processing"),
    "DLmodel": ('cmd', "bash predict.sh", "./DLmodel"),
    "post-processing1": ('.py', "json_to_xml.py", "./post-processing"),
    "post-processing2": ('.py', "import_xmi.py", "./post-processing"),
    # 其他工程和命令或主脚本，以及对应的路径
}

# 按顺序运行工程
for project, (project_type, data, path) in projects.items():
    print(f"Running project: {project}")
    current_dir = os.getcwd()  # 保存当前的工作目录
    os.chdir(path)  # 切换到工程所在的路径
    if project_type == '.py':
        # 如果是Python工程，运行对应的Python脚本
        subprocess.run(f"python {data}", shell=True)
    elif project_type == 'cmd':
        # 如果有启动命令的工程，运行对应的命令
        subprocess.run(data, shell=True)
    os.chdir(current_dir)  # 切换回原来的工作目录