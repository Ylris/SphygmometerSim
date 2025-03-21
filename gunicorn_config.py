import multiprocessing

# 绑定的IP和端口
bind = "127.0.0.1:8000"

# 工作模式
worker_class = "sync"

# 并行工作进程数 (通常设置为 CPU 数量的 2-4 倍)
workers = multiprocessing.cpu_count() * 2 + 1

# 指定每个工作进程的线程数
threads = 2

# 最大客户端并发数量
worker_connections = 1000

# 守护进程运行
daemon = False

# 请求超时时间
timeout = 30

# 访问日志文件
accesslog = "gunicorn_access.log"

# 错误日志文件
errorlog = "gunicorn_error.log"

# 日志级别
loglevel = "info" 