from flask import Flask, request, jsonify, Response
import time
import os
import uuid
import jwt
import hashlib
import csv
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建应用
app = Flask(__name__)

# 在生产环境中禁用调试模式
app.config['DEBUG'] = False

# 加载设备信息
def load_devices():
    """加载设备ID和对应的密钥"""
    devices = {}
    try:
        # 使用相对路径和绝对路径都尝试
        file_paths = [
            '血压计序列号和secret.txt',
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '血压计序列号和secret.txt')
        ]
        
        file_loaded = False
        for file_path in file_paths:
            if os.path.exists(file_path):
                logger.info(f"尝试从 {file_path} 加载设备信息")
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header
                    for row in reader:
                        if len(row) >= 2:
                            devices[row[0]] = row[1]
                            logger.info(f"加载设备: {row[0]}")
                file_loaded = True
                logger.info(f"成功从 {file_path} 加载了 {len(devices)} 个设备")
                break
        
        if not file_loaded:
            logger.error("未找到设备信息文件")
        
        if not devices:
            logger.warning("没有加载到任何设备信息!")
    except Exception as e:
        logger.error(f"加载设备信息失败: {e}")
    
    # 添加测试文件中使用的设备ID（如果需要测试）
    if "20845" not in devices:
        devices["20845"] = "abcde"
        logger.info("添加测试设备: 20845")
    
    # 打印所有可用的设备ID，用于调试
    logger.info(f"可用设备列表: {list(devices.keys())}")
    return devices

# 全局变量
devices = load_devices()
token_refresh_counts = {}  # 存储token的刷新次数
token_chains = {}  # 记录token的来源关系，用于检查刷新链

# 健康检查端点，对于监控很有用
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "devices_count": len(devices)})

# 添加响应压缩
@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/getTicket', methods=['GET'])
def get_ticket():
    device_id = request.args.get('deviceId')
    
    # Check if deviceId is provided
    if not device_id:
        return jsonify({"code": 201, "message": "缺少参数", "data": None})
    
    # Check if deviceId is valid
    if device_id not in devices:
        return jsonify({"code": 202, "message": "未知设备Id", "data": None})
    
    # Generate a ticket
    ticket = str(uuid.uuid4()).replace('-', '')
    
    return jsonify({
        "code": 200,
        "message": "成功",
        "data": {
            "ticket": ticket
        }
    })

@app.route('/getToken', methods=['POST'])
def get_token():
    data = request.get_json()
    
    # Check if required parameters are provided
    if not data or 'deviceId' not in data or 'signature' not in data or 'ticket' not in data:
        return jsonify({"code": 201, "message": "缺少参数", "data": None})
    
    device_id = data.get('deviceId')
    signature = data.get('signature')
    ticket = data.get('ticket')
    
    # Check if deviceId is valid
    if device_id not in devices:
        return jsonify({"code": 202, "message": "未知设备Id", "data": None})
    
    # Check signature
    secret = devices[device_id]
    expected_signature = hashlib.md5((ticket + device_id + secret).encode('utf-8')).hexdigest()
    
    if signature != expected_signature:
        return jsonify({"code": 203, "message": "签名解析失败", "data": None})
    
    # Generate JWT token
    expiration_time = int(time.time()) + 3600  # Token valid for 1 hour
    payload = {
        "deviceId": device_id,
        "expiredTime": expiration_time
    }
    
    token = jwt.encode(payload, secret, algorithm="HS256")
    # Initialize refresh count
    token_refresh_counts[token] = 0
    # 初始token没有父token
    token_chains[token] = None
    
    return jsonify({
        "code": 200,
        "message": "成功",
        "data": {
            "token": token,
            "expiredTime": expiration_time
        }
    })

@app.route('/uploadData', methods=['POST'])
def upload_data():
    data = request.get_json()
    
    # Check if required parameters are provided
    if not data or 'deviceId' not in data or 'token' not in data or 'data' not in data:
        return jsonify({"code": 201, "message": "缺少参数", "data": None})
    
    device_id = data.get('deviceId')
    token = data.get('token')
    bp_data = data.get('data')
    
    # Check if deviceId is valid
    if device_id not in devices:
        return jsonify({"code": 202, "message": "未知设备Id", "data": None})
    
    # Validate token
    secret = devices[device_id]
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        
        # Check if token is for the right device
        if payload.get('deviceId') != device_id:
            return jsonify({"code": 204, "message": "会话token无效", "data": None})
        
        # Check if token is expired
        if payload.get('expiredTime', 0) < time.time():
            return jsonify({"code": 206, "message": "token超期", "data": None})
        
    except:
        return jsonify({"code": 204, "message": "会话token无效", "data": None})
    
    # Validate blood pressure data
    try:
        # Check if time is a valid timestamp
        if isinstance(bp_data.get('time'), str):
            # Convert to int if possible
            try:
                time_value = int(time.mktime(time.strptime(bp_data.get('time'), "%Y-%m-%d")))
            except:
                return jsonify({"code": 205, "message": "血压值不正确", "data": None})
        else:
            time_value = bp_data.get('time')
        
        # Check if high and low are valid blood pressure values
        high = int(bp_data.get('high'))
        low = int(bp_data.get('low'))
        
        # Basic validation: high should be higher than low
        if high <= low:
            return jsonify({"code": 205, "message": "血压值不正确", "data": None})
        
        # More specific validation could be added here
        if high < 60 or high > 250 or low < 40 or low > 180:
            return jsonify({"code": 205, "message": "血压值不正确", "data": None})
            
    except:
        return jsonify({"code": 205, "message": "血压值不正确", "data": None})
    
    # Process successful upload
    current_time = int(time.time())
    
    return jsonify({
        "code": 200,
        "message": "成功",
        "data": {
            "receivedTime": current_time
        }
    })

@app.route('/refreshToken', methods=['POST'])
def refresh_token():
    data = request.get_json()
    
    # Check if required parameters are provided
    if not data or 'deviceId' not in data or 'signature' not in data or 'token' not in data:
        return jsonify({"code": 201, "message": "缺少参数", "data": None})
    
    device_id = data.get('deviceId')
    signature = data.get('signature')
    token = data.get('token')
    
    # Check if deviceId is valid
    if device_id not in devices:
        return jsonify({"code": 202, "message": "未知设备Id", "data": None})
    
    # Check signature
    secret = devices[device_id]
    expected_signature = hashlib.md5((token + device_id + secret).encode('utf-8')).hexdigest()
    
    if signature != expected_signature:
        return jsonify({"code": 203, "message": "签名解析失败", "data": None})
    
    # 检查token是否已经是刷新过的token
    if token in token_chains and token_chains[token] is not None:
        # 这个token已经是通过刷新获得的，不能再次刷新
        return jsonify({"code": 207, "message": "不能用此token再次请求token，请重新取票获取", "data": None})
    
    # Generate new JWT token
    expiration_time = int(time.time()) + 3600  # Token valid for 1 hour
    payload = {
        "deviceId": device_id,
        "expiredTime": expiration_time
    }
    
    new_token = jwt.encode(payload, secret, algorithm="HS256")
    
    # 记录新token的来源
    token_chains[new_token] = token
    
    # Update refresh count for traceability
    token_refresh_counts[token] = token_refresh_counts.get(token, 0) + 1
    token_refresh_counts[new_token] = 0
    
    return jsonify({
        "code": 200,
        "message": "成功",
        "data": {
            "token": new_token,
            "expiredTime": expiration_time
        }
    })

# 仅在直接运行此文件时启动Flask开发服务器
if __name__ == '__main__':
    # 开发环境使用Flask自带服务器，生产环境应使用Gunicorn
    app.run(host='127.0.0.1', port=80, debug=True) 