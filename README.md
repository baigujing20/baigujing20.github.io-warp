### 安卓手机Termux一键生成免费的Warp节点订阅


支持一键注册WireGuard和MASQUE两种协议，和一键转换成两种协议的多节点订阅。

1. 在Termux中先安装必备核心依赖：

1）
```
pkg update && pkg upgrade -y && pkg install -y git
```
2）
```
git clone https://github.com/baigujing20/baigujing20.github.io-warp.git
```
3）
```
pkg install -y python python-cryptography
```
4）
```
pip install requests pyperclip
```

2. 安装完再注册WireGuard和MASQUE两种协议

1）想注册MASQUE协议并转换成订阅，需要进入MASQUE的目标文件夹，里面详细介绍了操作方法


2）想注册WireGuard协议并转换成订阅，需要进入WireGuard的目标文件夹，里面详细介绍了操作方法

直接对准点击本项目中的WireGuard或MASQUE目录，就可进入其中参阅！别忘了先给我点个星Star

您的支持才是我前进的动力！