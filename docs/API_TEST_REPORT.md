# 接口测试报告（API_TEST_REPORT）

> 依据 `docs/API_TEST.md`，使用 curl 执行并自动生成。

---

## 1. 测试概要

| 项 | 内容 |
|----|------|
| 测试时间 | 2026-10-10 17:57:35 |
| 环境 BASE_URL | http://localhost:8080 |
| 执行方式 | curl.exe（Windows） |
| 用例总数 | 5 |
| PASS | 5 |
| FAIL | 0 |
| BLOCKED | 0 |
| 通过率 | 100.0% |

## 2. 用例结果

| 编号 | 用例 | 结果 | 说明 |
|------|------|------|------|
| 3.0 | 健康检查 | **PASS** | http=200; up=True |
| TC-01 | 获取医生列表 | **PASS** | http=200; code=0; count=5; hasPassword=False |
| TC-02 | 患者登录成功 | **PASS** | http=200; code=0; username=patient_zhaoming; hasPassword=False |
| TC-03 | 患者登录失败-密码错误 | **PASS** | http=200; code=401; data=None; message=用户名或密码错误 |
| TC-04 | 患者登录失败-参数为空 | **PASS** | http=200; code=400; data=None; message=用户名和密码不能为空 |

## 3. 响应摘要

### 3.0 健康检查

```
{"status":"UP","components":{"db":{"status":"UP","details":{"database":"MySQL","validationQuery":"isValid()"}},"diskSpace":{"status":"UP","details":{"total":512108785664,"free":21808799744,"threshold":10485760,"path":"D:\\claudecode_project\\qa-live-healthcare-interview\\server\\qa-service-user\\.","exists":true}},"ping":{"status":"UP"},"ssl":{"status":"UP","details":{"validChains":[],"invalidChains":[]}}}}
HTTP_CODE:200
```

### TC-01 获取医生列表

```
{"code":0,"data":[{"id":"doc001","username":"dr-zhang-wei","name":"张伟医生","title":"主任医师","department":"心内科","avatar":"https://images.pexels.com/photos/5215024/pexels-photo-5215024.jpeg?auto=compress&cs=tinysrgb&w=400","experience":"15年临床经验","specialties":["高血压","冠心病","心律失常"],"isActive":true},{"id":"doc002","username":"dr-li-na","name":"李娜医生","title":"副主任医师","department":"儿科","avatar":"https://images.pexels.com/photos/5327585/pexels-photo-5327585.jpeg?auto=compress&cs=tinysrgb&w=400","experience":"10年临床经验","specialties":["儿童感冒","儿童发育","疫苗接种"],"isActive":true},{"id":"doc003","username":"dr-wang-qiang","name":"王强医生","title":"主治医师","department":"骨科","avatar":"https://images.pexels.com/photos/5452293/pexels-photo-5452293.jpeg?auto=compress&cs=tinysrgb&w=400","experience":"8年临床经验","specialties":["骨折","关节炎","运动损伤"],"isActive":true},{"id":"doc004","username":"dr-liu-min","name":"刘敏医生","title":"主任医师","department":"妇产科","avatar":"https://images.pexels.com/photos/5452201/pexels-photo-5452201.jpeg?auto=compress&cs=tinysrgb&w=400","experience":"18年临床经验","specialties":["孕期保健","妇科炎症","产后恢复"],"isActive":false},{"id":"doc005","username":"dr-chen-jie","name":"陈杰医生","title":"副主任医师","department":"消化内科","avatar":"https://images.pexels.com/photos/5215024/pexels-photo-5215024.jpeg?auto=compress&cs=tinysrgb&w=400","experience":"12年临床经验","specialties":["胃炎","肠道疾病","肝病"],"isActive":true}],"message":"ok"}
HTTP_CODE:200
```

### TC-02 患者登录成功

```
{"code":0,"data":{"id":"patient001","username":"patient_zhaoming","name":"赵明","birthday":"1985-03-15","phone":"138****1234","gender":"男"},"message":"ok"}
HTTP_CODE:200
```

### TC-03 患者登录失败-密码错误

```
{"code":401,"data":null,"message":"用户名或密码错误"}
HTTP_CODE:200
```

### TC-04 患者登录失败-参数为空

```
{"code":400,"data":null,"message":"用户名和密码不能为空"}
HTTP_CODE:200
```

## 4. 结论

全部用例通过，需求 2（医生列表）与需求 3（患者登录）相关接口符合预期。

## 5. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-10-10 | 按 API_TEST.md 首次执行 |
