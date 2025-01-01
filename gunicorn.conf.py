# Gunicorn 配置文件
import multiprocessing

# 监听地址和端口
bind = "0.0.0.0:5000"

# 工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = "sync"

# 超时时间
timeout = 30

# 访问日志格式
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 错误日志
errorlog = "-"
loglevel = "info"

# 进程名称
proc_name = "esxi_packet_capture"

# 后台运行
daemon = False

# 重载
reload = False 