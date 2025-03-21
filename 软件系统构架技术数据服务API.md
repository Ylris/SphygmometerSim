# 全局公共参数

**全局Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| 暂无参数 |

**全局Query参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| 暂无参数 |

**全局Body参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| 暂无参数 |

**全局认证方式**

> 无需认证

# 状态码说明

| 状态码 | 中文描述 |
| --- | ---- |
| 暂无参数 |

# 取Ticket票

> 创建人: 陈恒鑫

> 更新人: 陈恒鑫

> 创建时间: 2025-02-14 17:05:04

> 更新时间: 2025-03-09 10:50:07

```text
暂无描述
```

**接口状态**

> 已完成

**接口URL**

> /getTicket?deviceId=

**请求方式**

> GET

**Content-Type**

> none

**请求Query参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| deviceId | - | String | 是 | 设备Id号 |

**认证方式**

> 继承父级

**响应示例**

* 成功(200)

```javascript
{
  "code": 200,
  "message": "成功",
  "data": {
    "ticket": "NO47V7vpXbXxE46/Z1NoVSsMczcdcI+Q"
  }
}
```

* 缺少参数(201)

```javascript
{
  "code": 201,
  "message": "缺少参数",
  "data": null
}
```

* 未知设备Id(202)

```javascript
{
  "code": 202,
  "message": "未知设备Id",
  "data": null
}
```

**Query**

# 获取Token

> 创建人: 陈恒鑫

> 更新人: 陈恒鑫

> 创建时间: 2025-02-14 17:26:12

> 更新时间: 2025-03-13 16:19:32

```text
暂无描述
```

**接口状态**

> 已完成

**接口URL**

> /getToken

**请求方式**

> POST

**Content-Type**

> json

**请求Body参数**

```javascript
{
    "deviceId" : "20845",
    "signature" : "9b87c6978fc19e2b6e5deb66cb8ce2b3",
    "ticket" : "NO47V7vpXbXxE46/Z1NoVSsMczcdcI+Q"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| deviceId | - | String | 是 | 设备Id号 |
| signature | - | String | 是 | 签名，=MD5(Ticket+DeviceId+Secret) |
| ticket | - | String | 是 | 票据 |

**认证方式**

> 继承父级

**响应示例**

* 成功(200)

```javascript
{
  "code": 200,
  "message": "成功",
  "data": {
    "token" : "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJ1SWQiOiIyIiwidHlwZSI6MH0.F9WeBJjTElm90fp-iXo3p_wrpaKQJN2pzcQeHX6OtlWldf_kNliEfTCD0XD6K82QgXQL22uNxq2tBuKpLHS6dQ",
    "expiredTime" : 1739526568
  }
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | ---- | ---- |
| token | - | String | 会话Token |

* 缺少参数(201)

```javascript
{
  "code": 201,
  "message": "缺少参数",
  "data": null
}
```

* 未知设备Id(202)

```javascript
{
  "code": 202,
  "message": "未知设备Id",
  "data": null
}
```

* 签名解析失败(203)

```javascript
{
  "code": 203,
  "message": "签名解析失败",
  "data": null
}
```

**Query**

# 上传血压数据

> 创建人: 陈恒鑫

> 更新人: 陈恒鑫

> 创建时间: 2025-02-14 17:32:47

> 更新时间: 2025-03-08 22:30:02

```text
暂无描述
```

**接口状态**

> 已完成

**接口URL**

> /uploadData

**请求方式**

> POST

**Content-Type**

> json

**请求Body参数**

```javascript
{
    "deviceId" : "20845",
    "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZpY2VJZCI6IjIwODQ1IiwiZXhwaXJlZFRpbWUiOjE3NDE0MzIxMDN9.oOgzU99A7IK_oiAem23XIrifDhR3CajyeMbdVNpyyto",
    "data" : {
        "time" : 1739526614,
        "high" : 120,
        "low" : 90
    }
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| deviceId | - | String | 是 | 设备Id |
| token | - | String | 是 | 会话token |
| time | - | Integer | 是 | 血压测量时间 |
| high | - | Integer | 是 | 血压收缩压 |
| low | - | Integer | 是 | 血压舒张压 |

**认证方式**

> 继承父级

**响应示例**

* 成功(200)

```javascript
{
  "code": 200,
  "message": "成功",
  "data": {
    "receivedTime" : 1739526568
  }
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | ---- | ---- |
| receiveTime | - | Integer | 接收到的时间（毫秒时间戳） |

* 缺少参数(201)

```javascript
{
  "code": 201,
  "message": "缺少参数",
  "data": null
}
```

* 未知设备Id(202)

```javascript
{
  "code": 202,
  "message": "未知设备Id",
  "data": null
}
```

* 会话token无效(204)

```javascript
{
  "code": 204,
  "message": "会话token无效",
  "data": null
}
```

* 血压值不正确(205)

```javascript
{
  "code": 205,
  "message": "血压值不正确",
  "data": null
}
```

* token超期(206)

```javascript
{
  "code": 206,
  "message": "token超期",
  "data": null
}
```

**Query**

# 刷新Token

> 创建人: 陈恒鑫

> 更新人: 陈恒鑫

> 创建时间: 2025-03-07 21:44:06

> 更新时间: 2025-03-09 10:50:06

```text
暂无描述
```

**接口状态**

> 已完成

**接口URL**

> /refreshToken

**请求方式**

> POST

**Content-Type**

> json

**请求Body参数**

```javascript
{
    "deviceId" : "20845",
    "signature" : "cd910bb991d913beff67b7c7f8daed1c",
    "token" : "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJ1SWQiOiIyIiwidHlwZSI6MH0.F9WeBJjTElm90fp-iXo3p_wrpaKQJN2pzcQeHX6OtlWldf_kNliEfTCD0XD6K82QgXQL22uNxq2tBuKpLHS6dQ"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| deviceId | - | String | 是 | 设备Id |
| signature | - | String | 是 | 签名，=MD5(token+deviceId+secret) |
| token | - | String | 是 | 现有会话token |

**认证方式**

> 继承父级

**响应示例**

* 成功(200)

```javascript
{
  "code": 200,
  "message": "成功",
  "data": {
    "token": "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJ1SWQiOiIyIiwidHlwZSI6MH0.F9WeBJjTElm90fp-iXo3p_wrpaKQJN2pzcQeHX6OtlWldf_kNliEfTCD0XD6K82QgXQL22uNxq2tBuKpLHS6dQ",
    "expiredTime": 1739526568
  }
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | ---- | ---- |
| token | - | String | 新会话token |

* 缺少参数(201)

```javascript
{
  "code": 201,
  "message": "缺少参数",
  "data": null
}
```

* 未知设备Id(202)

```javascript
{
  "code": 202,
  "message": "未知设备Id",
  "data": null
}
```

* 签名解析失败(203)

```javascript
{
  "code": 203,
  "message": "签名解析失败",
  "data": null
}
```

* 不能用此token再次请求token，请重新取票获取(207)

```javascript
{
  "code": 207,
  "message": "不能用此token再次请求token，请重新取票获取",
  "data": null
}
```

**Query**
