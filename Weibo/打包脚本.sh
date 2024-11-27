#!/bin/bash

# 检查 release目录是否存在，如果不存在则创建它
if [! -d "release" ]; then
    mkdir release
fi

# 使用PyInstaller进行单个文件打包，指定输出路径为release目录
pyinstaller --onefile process.py -o release

echo "打包完成，输出文件在release目录下。"