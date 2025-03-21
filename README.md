# 血压计监控系统后端服务

这是一个基于Flask的血压计监控系统后端服务，实现了设备认证和血压数据上传功能。

## 功能特点

- 设备认证和授权机制
  - Ticket获取
  - Token获取和刷新
- 血压数据上传和验证
- 支持多台设备并发访问
- 完整的错误处理机制

## API接口

### 1. 取Ticket票 (/getTicket)
- **请求方式**: GET
- **参数**: deviceId (设备ID号)
- **响应代码**: 200(成功), 201(缺少参数), 202(未知设备ID)

### 2. 获取Token (/getToken)
- **请求方式**: POST
- **参数**: deviceId, signature, ticket
- **响应代码**: 200(成功), 201(缺少参数), 202(未知设备ID), 203(签名解析失败)

### 3. 上传血压数据 (/uploadData)
- **请求方式**: POST
- **参数**: deviceId, token, data(包含time, high, low)
- **响应代码**: 200(成功), 201(缺少参数), 202(未知设备ID), 204(会话token无效), 205(血压值不正确), 206(token超期)

### 4. 刷新Token (/refreshToken)
- **请求方式**: POST
- **参数**: deviceId, signature, token
- **响应代码**: 200(成功), 201(缺少参数), 202(未知设备ID), 203(签名解析失败), 207(不能用此token再次请求token)

## 安装与部署

### 安装依赖
```bash
pip install -r requirements.txt
```

### 开发环境运行
```bash
python app.py
```

### 生产环境部署
1. 使用Gunicorn作为WSGI服务器:
```bash
gunicorn -c gunicorn_config.py app:app
```

2. 配置Nginx作为反向代理:
```bash
# 将nginx_config.conf复制到Nginx配置目录
```

## 安全说明

- 使用JWT进行设备认证
- 采用MD5签名机制
- Token有效期限制和刷新限制
- 血压数据格式验证 