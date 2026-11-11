1. 按步骤执行下面的命令生成WireGuard节点配置：

1）进入WireGuard目录：
```
cd baigujing20.github.io-warp/WireGuard
```
2）注册WireGuard节点：
```
python WireGuard.py
```
会自动生成WireGuard配置文件`config.conf`

2. 优选WireGuard协议IP

1）
```
chmod +x WarpSpeedTest
```
2）
```
./WarpSpeedTest
```
或者
```
./WarpSpeedTest -ipv6
```

3. 转换成WireGuard多节点订阅

①生成手机v2rayNG订阅：
```
python v2rayNG.py
```
直接回车，默认MTU的值为1280

所生成的节点订阅被自动写入v2rayNG.txt文件中，默认输出50个节点，如果想输出100个节点，在v2rayNG.py文件中输入 read_csv_endpoints 搜索，在后面找到50改成100即可

之后执行下面的命令启用浏览器服务：
```
python -m http.server 8080
```
在浏览器中访问:  `http://127.0.0.1:8080/v2rayNG.txt`

全选复制v2rayNG.txt文件中所有的WireGuard节点，导入到手机的v2rayNG中即可，如果发现测延时是-1，请下载最新版本的v2rayNG

v2rayNG下载：[点击下载](https://github.com/2dust/v2rayNG/releases/download/2.3.15/v2rayNG_2.3.15-fdroid_arm64-v8a.apk)

PattNG下载：[点击下载](https://github.com/patterniha/PattNG/releases/download/2.3.15-P71/PattNG_2.3.15-P71_arm64-v8a.apk)

返回Termux，按CTRL+c键退出，如果第一次没有退出，需要按CTRL+c键几次就可退出，或者全部退出Termux再重新进入

②生成手机NekoBox订阅
```
python NekoBox.py
```
所生成的节点订阅被自动写入NekoBox.txt文件中，默认输出50个节点，如果想输出100个节点，在NekoBox.py文件中输入 read_csv_endpoints 搜索，在后面找到50改成100即可

之后执行下面的命令启用浏览器服务：
```
python -m http.server 8080
```
在浏览器中访问:` http://127.0.0.1:8080/NekoBox.txt`

全选复制NekoBox.txt文件中所有的WireGuard节点，导入到手机的NekoBox中即可

NekoBox下载：[点击下载](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases/download/1.4.2/NekoBox-1.4.2-arm64-v8a.apk)

返回Termux，按CTRL+c键退出，如果第一次没有退出，需要按CTRL+c键几次就可退出，或者全部退出Termux再重新进入

③把WireGuard配置转换成Clash订阅

```
python wireguardmihomo.py
```
所生成的节点订阅被自动写入wireguard.yaml文件中，默认输出50个节点，如果想输出100个节点，在wireguardmihomo.py文件中输入 data_list = 搜索，在后面找到50改成100即可

之后执行下面的命令启用浏览器服务：
```
python -m http.server 8080
```
在浏览器中访问：`http://127.0.0.1:8080/wireguard.yaml`

下载wireguard.yaml配置文件到本地，在mihomo内核的Clash系列软件中点击添加配置，选择【文件】进入，找到刚刚从浏览器下载到本地的wireguard.yaml配置文件，从本地直接上传即可

4. IPv6的节点不通什么办？

以FlClash为例，点击底部菜单的【工具】，找到【常规】，找到内核下方的IPv6，将【开启后可以接收IPv6流量】右边的按钮打开，如果你的网络有ipv6，那么wireguard中的ipv6节点就通了

FlClash下载：[点击下载](https://github.com/chen08209/FlClash/releases/download/v0.9.3/FlClash-0.9.3-android-arm64-v8a.apk)

返回Termux，按CTRL+c键退出，如果第一次没有退出，需要按CTRL+c键几次就可退出，或者全部退出Termux再重新进入

5. Cloudflare WireGuard IP 地址范围：

IPv4：
```
8.6.112.0/24
8.34.70.0/24
8.34.146.0/24
8.35.211.0/24
8.39.125.0/24
8.39.204.0/24
8.39.214.0/24
8.47.69.0/24
162.159.192.0/24
162.159.193.0/24
162.159.195.0/24
188.114.96.0/24
188.114.97.0/24
188.114.98.0/24
188.114.99.0/24
```
IPv6：
```
2606:4700:d0::/48
2606:4700:d1::/48
```
WireGuard协议的端口(54个)

{854, 859, 864, 878, 880, 890, 891, 894, 903, 908, 928, 934, 939, 942, 943, 945, 946, 955, 968, 987, 988, 1002, 1010,1014, 1018, 1070, 1074, 1180, 1387, 1843, 2371, 2506, 3138, 3476, 3581, 3854, 4177, 4198, 4233, 5279, 5956, 7103, 7152, 7156,7281, 7559, 8319, 8742, 8854, 8886, 2408, 500, 4500, 1701}, // WireGuard协议的端口(54个)

结尾：

想了解更详细的操作需要进入本项目的WireGuard和MASQUE目录中参阅！别忘了给我点个星Star

WireGuard详情：[进入查阅](https://github.com/baigujing20/baigujing20.github.io-warp/tree/main/WireGuard)

MASQUE详情：[进入查阅](https://github.com/baigujing20/baigujing20.github.io-warp/tree/main/MASQUE)

我的博客网：[进入查阅](https://github.com/baigujing20/baigujing20.github.io)