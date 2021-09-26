Simulators
=======

A system for Simulators.

- 2014 - p2dv
- 2015 - sjtu.cool
- 2021 - Great Ideas



## Core Server Setup Example

~~~sh
sudo locale-gen zh_CN.UTF-8
sudo dpkg-reconfigure tzdata
sudo apt-get install build-essential git python3-pip python-dev nodejs screen mongodb-server vim nginx npm
sudo pip3 install tornado pymongo subprocess32
sudo pip3 install tabulate requests
sudo apt install npm
sudo useradd -m -s /bin/bash p2dv
sudo passwd p2dv
su p2dv
# 设置 p2dv 的密码
cd ~
git clone https://github.com/andy-yang-1/great.simulators.git
mkdir data
mkdir data/ai
mkdir data/log
mkdir data/upload
mkdir log
# 注意，接下来要设置一些路径
vim great.simulators/core_server/const.py
vim great.simulators/daemon/const.py
# daemon 需要修改其中 CORE_SERVER 将其改为自己服务器端口
vim great.simulators/web/settings.js
# 此处可以修改 cdn

# 开启 web 服务
screen -S web
cd great.simulators/web
npm install express connect-mongo method-override ejs mongoose body-parser
# install nodejs packeages, maybe not complete
node app.js

# ctrl + A + D 切屏
screen -S core_server
cd great.simulators/core_server
python3 core_server.py

# Judge Server Setup
# ctrl + A + D 切屏
screen -S daemon
cd great.simulators/daemon
python3 p2dv.in.py
# finished
~~~



