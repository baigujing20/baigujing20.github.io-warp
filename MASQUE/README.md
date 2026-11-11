1）进入MASQUE目录：
```
cd baigujing20.github.io-warp/MASQUE
```
2）注册MASQUE节点：
```
python masque.py
```
会自动生成Masque配置文件`config.json`

2. 优选Masque协议IP

1）
```
chmod +x udpwarp
```
2）
```
./udpwarp -masque
```
3. 一键生成Clash订阅
```
python masquemihomo.py
```
所生成的节点订阅被自动写入masque.yaml文件中，默认输出50个节点，如果想输出100个节点，在masquemihomo.py文件中输入 for i, item in islice 搜索，在后面找到50改成100即可

4. 启用浏览器服务：
```
python -m http.server 8080
```
在浏览器中访问: `http://127.0.0.1:8080/masque.yaml`

下载masque.yaml订阅文件到本地，在mihomo内核的Clash系列软件中点击添加配置，选择【文件】进入，找到刚刚从浏览器下载到本地的masque.yaml配置文件，从本地直接上传即可

5. IPv6的节点不通什么办？

以FlClash为例，点击底部菜单的【工具】，找到【常规】，找到内核下方的IPv6，将【开启后可以接收IPv6流量】右边的按钮打开，如果你的网络有ipv6，那么masque中的ipv6节点就通了

FlClash下载：[点击下载](https://github.com/chen08209/FlClash/releases/download/v0.9.3/FlClash-0.9.3-android-arm64-v8a.apk)

返回Termux，按CTRL+c键退出，如果第一次没有退出，需要按CTRL+c键几次就可退出，或者全部退出Termux再重新进入

6. Cloudflare Masque IP 地址范围：

IPv4：
```
162.159.197.1
162.159.198.1
162.159.199.1
162.159.197.2
162.159.198.2
162.159.199.2
```
IPv6：
```
2606:4700:102::1
2606:4700:103::1
2606:4700:104::1
2606:4700:105::1
2606:4700:102::2
2606:4700:103::2
2606:4700:104::2
2606:4700:105::2
```
Masque协议的端口(7个)

{443, 500, 1701, 4500, 4443, 8443, 8095}, // Masque协议的端口(7个)

结尾：

想了解更详细的操作需要进入本项目的WireGuard和MASQUE目录中参阅！别忘了给我点个星Star

WireGuard详情：[进入查阅](https://github.com/baigujing20/baigujing20.github.io-warp/tree/main/WireGuard)

MASQUE详情：[进入查阅](https://github.com/baigujing20/baigujing20.github.io-warp/tree/main/MASQUE)

我的博客网：[进入查阅](https://github.com/baigujing20/baigujing20.github.io)