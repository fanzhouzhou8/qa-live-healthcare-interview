# 接口测试流程文档（API_TEST）

本文档描述本次面试需求所涉及接口的 **curl** 测试流程，并指导 AI 按本文档执行测试、生成测试报告。

---

## 1. 测试范围

| 关联需求 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 需求 2 | `/api/doctors` | GET | 医生列表（供 Doctors.vue） |
| 需求 3 | `/api/patients/login` | POST | 问诊用户登录 |

前置条件：

1. MySQL 已就绪，库名 `qa_healthcare`，含 `doctor`、`patient` 表及种子数据
2. `qa-service-user` 已启动，默认地址：`http://localhost:8080`
3. 本机可执行 `curl`（Windows 使用 `curl.exe`）

---

## 2. 环境变量（可选）

```bash
export BASE_URL=http://localhost:8080
```

Windows PowerShell：

```powershell
$BASE_URL = "http://localhost:8080"
```

---

## 3. 测试用例与 curl 命令

### 3.0 前置健康检查（可选）

**目的**：确认服务与数据库可用。

```bash
curl -s -w "\nHTTP_CODE:%{http_code}\n" "%BASE_URL%/actuator/health"
```

**期望**：HTTP 200，`status` 为 `UP`。

---

### TC-01 获取医生列表（正常）

**关联需求**：需求 2  
**目的**：验证医生列表 API 返回完整字段且不含密码。

```bash
curl -s -w "\nHTTP_CODE:%{http_code}\n" "%BASE_URL%/api/doctors"
```

**期望**：

- HTTP 200
- JSON：`code == 0`，`message == "ok"`
- `data` 为数组，长度 >= 1
- 每条记录包含：`id, username, name, title, department, avatar, experience, specialties, isActive`
- 响应中 **不包含** `password` 字段

---

### TC-02 患者登录成功

**关联需求**：需求 3  
**目的**：正确用户名密码可登录。

```bash
curl -s -w "\nHTTP_CODE:%{http_code}\n" \
  -X POST "%BASE_URL%/api/patients/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"patient_zhaoming\",\"password\":\"123456\"}"
```

Windows（推荐用文件避免转义问题）：

```powershell
'{"username":"patient_zhaoming","password":"123456"}' | Out-File -Encoding ascii tmp-login-ok.json
curl.exe -s -w "`nHTTP_CODE:%{http_code}`n" -X POST "$BASE_URL/api/patients/login" -H "Content-Type: application/json" --data-binary "@tmp-login-ok.json"
```

**期望**：

- HTTP 200
- `code == 0`
- `data.username == "patient_zhaoming"`
- `data.name` 非空
- 响应中 **不包含** `password`

---

### TC-03 患者登录失败（密码错误）

**关联需求**：需求 3  

```bash
curl -s -w "\nHTTP_CODE:%{http_code}\n" \
  -X POST "%BASE_URL%/api/patients/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"patient_zhaoming\",\"password\":\"wrong\"}"
```

Windows：

```powershell
'{"username":"patient_zhaoming","password":"wrong"}' | Out-File -Encoding ascii tmp-login-fail.json
curl.exe -s -w "`nHTTP_CODE:%{http_code}`n" -X POST "$BASE_URL/api/patients/login" -H "Content-Type: application/json" --data-binary "@tmp-login-fail.json"
```

**期望**：

- HTTP 200（业务错误码在 body）
- `code == 401`
- `data == null`
- `message` 提示用户名或密码错误

---

### TC-04 患者登录失败（参数为空）

**关联需求**：需求 3  

```bash
curl -s -w "\nHTTP_CODE:%{http_code}\n" \
  -X POST "%BASE_URL%/api/patients/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"\",\"password\":\"\"}"
```

Windows：

```powershell
'{"username":"","password":""}' | Out-File -Encoding ascii tmp-login-empty.json
curl.exe -s -w "`nHTTP_CODE:%{http_code}`n" -X POST "$BASE_URL/api/patients/login" -H "Content-Type: application/json" --data-binary "@tmp-login-empty.json"
```

**期望**：

- HTTP 200
- `code == 400`
- `data == null`

---

## 4. 判定规则

| 结果 | 条件 |
|------|------|
| PASS | HTTP 状态与 body 断言全部满足 |
| FAIL | 任一断言不满足或服务不可达 |
| BLOCKED | 环境未就绪（服务未启动 / DB 不可用），无法执行 |

全部用例执行后，汇总通过率，写入测试报告。

---

## 5. 指导 AI 执行测试并生成报告（提示词）

将以下提示词交给 AI：

```
请严格按 docs/API_TEST.md 完成接口测试并生成报告，要求：

1. 确认 BASE_URL（默认 http://localhost:8080）服务可用
2. 使用 curl（Windows 用 curl.exe）依次执行文档中的全部用例：
   - 3.0 健康检查（可选）
   - TC-01 获取医生列表
   - TC-02 患者登录成功
   - TC-03 患者登录失败（密码错误）
   - TC-04 患者登录失败（参数为空）
3. 对照文档「期望」逐条判定 PASS / FAIL / BLOCKED
4. 将原始响应关键摘要写入 docs/API_TEST_REPORT.md
5. 报告需包含：测试时间、环境、用例结果表、结论、失败项说明（如有）
6. 将本提示词追加到 docs/prompts.md

不要跳过用例；若环境问题导致无法测试，标记 BLOCKED 并说明原因。
```

---

## 6. 测试报告产出

| 文件 | 说明 |
|------|------|
| `docs/API_TEST_REPORT.md` | AI 按本文档执行后生成的测试报告 |

---

## 7. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-10-10 | 初版，覆盖需求 2 / 需求 3 接口 |
