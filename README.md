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
```
git clone <repository-url>
cd <repository-name>
```

2. 创建虚拟环境：
```
python -m venv venv
```
3. 激活虚拟环境：
```
source venv/bin/activate
```

4. 安装依赖：
```
pip install -r requirements.txt
```

5. 运行应用：
```
python app.py
```

### 方式二：容器部署

1. 构建镜像：
```
docker build -t packet-capture:latest .
```

2. 运行容器：
```
# 后台运行
docker run -d -p 5000:5000 --name packet-capture packet-capture:latest

# 或者指定时区运行
docker run -d -p 5000:5000 -e TZ=Asia/Shanghai --name packet-capture packet-capture:latest
```


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
```   
docker build -t packet-capture:1.0.0 .
docker tag packet-capture:1.0.0 packet-capture:latest
```
2. 创建Git标签：
```
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```
3. 发布Docker镜像：
```
# 推送指定版本
docker push packet-capture:1.0.0
# 推送最新版本
docker push packet-capture:latest
```

## 使用说明

1. 访问 http://localhost:5000
2. 选择要捕获的网络组件（switchport、vmnic或vmk）
3. 填写相关过滤条件
4. 生成捕获命令
5. 在ESXi主机上执行生成的命令

## 支持的过滤条件

- 网络组件：switchport、vmnic、vmk
- 流量方向：双向、入向、出向
- IP地址过滤：源IP、目标IP
- MAC地址过滤
- VLAN过滤
- 协议过滤：ICMP、DNS、HTTP、HTTPS、SSH、Telnet、NTP
- 自定义端口过滤

## 注意事项

- 确保有适当的权限访问ESXi主机
- 建议在生产环境中使用Docker部署
- 捕获文件默认保存在/tmp/capture.pcap
- 容器时区默认设置为Asia/Shanghai

## License

[MIT License](LICENSE)
