# ESXi Network Capture Tool
这是一个基于Flask的Web应用程序，用于生成ESXi主机上的数据包捕获命令。

## 功能特点

- 支持多种网络组件的数据包捕获（switchport、vmnic、vmk）
- 支持常见协议过滤（ICMP、DNS、HTTP、HTTPS、SSH、Telnet、NTP）
- 支持IP地址、MAC地址、VLAN等过滤条件
- 支持双向、入向、出向流量捕获
- 提供文件保存和在线查看两种捕获模式

## 项目预览

### 主界面
![主界面](https://yxyj1919-imagebed.oss-cn-beijing.aliyuncs.com/rocket-image/202501111656756.png)

### 命令生成
![命令生成](https://yxyj1919-imagebed.oss-cn-beijing.aliyuncs.com/rocket-image/202501111713907.png)

## 环境要求

- Python 3.x
- Flask 2.3.3
- Werkzeug 2.3.7
- Gunicorn 21.2.0

## 安装步骤

### 方式一：本地安装

1. 克隆仓库：


### 方式一：容器部署

## 版本管理

### 版本号规则
我们使用语义化版本号(Semantic Versioning)进行版本管理：
- 主版本号：不兼容的API修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 版本历史
- v1.0.0 (2024-01-11)
  - 初始版本发布
  - 支持基本的数据包捕获功能
  - 支持Docker部署

### 版本发布流程
1. 更新版本号：
