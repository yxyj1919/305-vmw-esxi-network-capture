# ESXi Network Packet Capture Web Interface
![](https://yxyj1919-imagebed.oss-cn-beijing.aliyuncs.com/rocket-image/202501111656756.png)
这是一个基于Flask的Web应用程序，用于生成ESXi主机上的数据包捕获命令。

## 功能特点

- 支持多种网络组件的数据包捕获（switchport、vmnic、vmk）
- 支持常见协议过滤（ICMP、DNS、HTTP、HTTPS、SSH、Telnet、NTP）
- 支持IP地址、MAC地址、VLAN等过滤条件
- 支持双向、入向、出向流量捕获
- 提供文件保存和在线查看两种捕获模式

## 环境要求

- Python 3.x
- Flask 2.3.3
- Werkzeug 2.3.7
- Gunicorn 21.2.0

## 安装步骤

1. 克隆仓库：
