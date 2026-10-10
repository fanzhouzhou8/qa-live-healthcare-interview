# AI Coding 提示词记录

本文档记录完成本次面试技术要求过程中使用的全部提示词。

---

## 需求 1：首页中英文切换

```
1. 给web端的首页添加中英文切换能力，在页面右上角添加语言切换下拉菜单，在用户选择 **中文/English** 选项时动态切换页面显示内容到对应语言。中英文语言资源文件需要保存在 `web/qa-web/src/locales` 目录中。只需要处理首页本身，无需处理其他页面。
```

---

## 需求 2：医生数据改用 MySQL 存储并前后端联调

```
2. 当前应用的数据全部使用json文件的方式在前端项目中存储，请将医生相关的数据使用mysql数据库存储。具体要求如下：
    - 创建 docker-compose.yml 用于创建mysql数据库，并挂接phpmyadmin作为数据库服务器管理界面
    - 在 qa-service-user 服务中创建可以支持前端 [医生页面](web/qa-web/src/views/Doctors.vue) 显示医生列表所需要的api
    - 完成前后端联调
```

---

## 需求 3：问诊用户用户名密码登录

### 3.1 需求原文

```
3. 为问诊用户提供用户名密码登录方式
    - 在 /docs 目录中编写规范的PRD文档模版
    - 指导 AI使用以上模版编写此特性的PRD文档
    - 指导 AI使用此PRD文档完成特性开发，如果需要进行拆分请在PRD文档中提供拆分步骤
```

### 3.2 指导 AI 使用模版编写 PRD

```
请先阅读 docs/PRD_TEMPLATE.md，并严格按该模版结构，为「问诊用户用户名密码登录」编写完整 PRD 文档，保存为 docs/PRD_patient_login.md。
要求：
1. 覆盖背景、目标、非目标、功能需求、交互、数据模型、接口、测试要点
2. 在「开发拆分步骤」中给出可顺序执行的 Step 列表，便于 AI Coding 分步实现
3. 明确替换现有 Consultation.vue 的姓名+生日弱校验为用户名+密码登录
4. 患者数据存 MySQL，登录 API 放在 qa-service-user
```

### 3.3 指导 AI 按 PRD 完成开发

```
请严格按照 docs/PRD_patient_login.md 的「开发拆分步骤」依次实现问诊用户登录特性：
1. 先确认 PRD 与模版已就绪
2. 在 MySQL 增加 patient 表与种子账号，并更新 docker/mysql/init/01-init.sql
3. 在 qa-service-user 实现 POST /api/patients/login
4. 改造前端 Consultation.vue 为用户名密码登录，并联调后端
5. 将本过程使用的提示词追加到 docs/prompts.md
每完成一步先验证再进入下一步，不要跳步。
```

---

## 测试要求：curl 接口测试与报告

### T.1 需求原文

```
测试要求

1. 使用 curl 构建对于以上需求中所涉及的所有接口的测试
2. 提供 /docs/API_TEST.md 用于描述以上接口测试流程，并指导AI使用这份文档完成测试并生成测试报告
```

### T.2 指导 AI 编写 API_TEST.md

```
请在 docs/API_TEST.md 中编写接口测试流程文档，要求：
1. 覆盖本次需求涉及的全部接口（GET /api/doctors、POST /api/patients/login）
2. 给出可直接执行的 curl 命令（兼容 Windows curl.exe）
3. 写明每个用例的期望结果与 PASS/FAIL/BLOCKED 判定规则
4. 在文档中提供「指导 AI 执行测试并生成报告」的提示词
5. 约定测试报告输出为 docs/API_TEST_REPORT.md
```

### T.3 指导 AI 按 API_TEST.md 执行测试并生成报告

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
