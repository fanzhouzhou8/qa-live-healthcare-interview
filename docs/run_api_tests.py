# -*- coding: utf-8 -*-
"""按 docs/API_TEST.md 使用 curl 执行接口测试并生成报告。"""
from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080")
DOCS_DIR = Path(__file__).resolve().parent
REPORT_PATH = DOCS_DIR / "API_TEST_REPORT.md"
results: list[dict] = []


def run_curl(method: str, path: str, body: str | None = None) -> tuple[str, str]:
    url = f"{BASE_URL}{path}"
    cmd = ["curl.exe", "-s", "-w", "\nHTTP_CODE:%{http_code}", "-X", method, url]
    tmp_path = None
    if body is not None:
        fd, tmp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        Path(tmp_path).write_text(body, encoding="utf-8")
        cmd.extend(["-H", "Content-Type: application/json", "--data-binary", f"@{tmp_path}"])

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        raw = proc.stdout
    finally:
        if tmp_path:
            Path(tmp_path).unlink(missing_ok=True)

    match = re.search(r"HTTP_CODE:(\d+)\s*$", raw)
    http_code = match.group(1) if match else ""
    body_text = re.sub(r"\n?HTTP_CODE:\d+\s*$", "", raw).strip()
    return http_code, body_text


def add_result(case_id: str, name: str, status: str, detail: str, evidence: str) -> None:
    results.append(
        {
            "id": case_id,
            "name": name,
            "status": status,
            "detail": detail,
            "evidence": evidence,
        }
    )


def main() -> int:
    # 3.0 health
    try:
        code, body = run_curl("GET", "/actuator/health")
        ok = code == "200" and '"status":"UP"' in body.replace(" ", "")
        add_result(
            "3.0",
            "健康检查",
            "PASS" if ok else "FAIL",
            f"http={code}; up={ok}",
            f"{body}\nHTTP_CODE:{code}",
        )
    except Exception as exc:  # noqa: BLE001
        add_result("3.0", "健康检查", "BLOCKED", str(exc), "")

    # TC-01
    code, body = run_curl("GET", "/api/doctors")
    try:
        obj = json.loads(body)
        count = len(obj.get("data") or [])
        has_password = '"password"' in body
        ok = code == "200" and obj.get("code") == 0 and count >= 1 and not has_password
        add_result(
            "TC-01",
            "获取医生列表",
            "PASS" if ok else "FAIL",
            f"http={code}; code={obj.get('code')}; count={count}; hasPassword={has_password}",
            f"{body}\nHTTP_CODE:{code}",
        )
    except Exception as exc:  # noqa: BLE001
        add_result("TC-01", "获取医生列表", "FAIL", f"parse error: {exc}", f"{body}\nHTTP_CODE:{code}")

    # TC-02
    code, body = run_curl(
        "POST",
        "/api/patients/login",
        '{"username":"patient_zhaoming","password":"123456"}',
    )
    try:
        obj = json.loads(body)
        data = obj.get("data") or {}
        has_password = '"password"' in body
        ok = (
            code == "200"
            and obj.get("code") == 0
            and data.get("username") == "patient_zhaoming"
            and not has_password
        )
        add_result(
            "TC-02",
            "患者登录成功",
            "PASS" if ok else "FAIL",
            f"http={code}; code={obj.get('code')}; username={data.get('username')}; hasPassword={has_password}",
            f"{body}\nHTTP_CODE:{code}",
        )
    except Exception as exc:  # noqa: BLE001
        add_result("TC-02", "患者登录成功", "FAIL", f"parse error: {exc}", f"{body}\nHTTP_CODE:{code}")

    # TC-03
    code, body = run_curl(
        "POST",
        "/api/patients/login",
        '{"username":"patient_zhaoming","password":"wrong"}',
    )
    try:
        obj = json.loads(body)
        ok = code == "200" and obj.get("code") == 401 and obj.get("data") is None
        add_result(
            "TC-03",
            "患者登录失败-密码错误",
            "PASS" if ok else "FAIL",
            f"http={code}; code={obj.get('code')}; data={obj.get('data')}; message={obj.get('message')}",
            f"{body}\nHTTP_CODE:{code}",
        )
    except Exception as exc:  # noqa: BLE001
        add_result("TC-03", "患者登录失败-密码错误", "FAIL", f"parse error: {exc}", f"{body}\nHTTP_CODE:{code}")

    # TC-04
    code, body = run_curl("POST", "/api/patients/login", '{"username":"","password":""}')
    try:
        obj = json.loads(body)
        ok = code == "200" and obj.get("code") == 400 and obj.get("data") is None
        add_result(
            "TC-04",
            "患者登录失败-参数为空",
            "PASS" if ok else "FAIL",
            f"http={code}; code={obj.get('code')}; data={obj.get('data')}; message={obj.get('message')}",
            f"{body}\nHTTP_CODE:{code}",
        )
    except Exception as exc:  # noqa: BLE001
        add_result("TC-04", "患者登录失败-参数为空", "FAIL", f"parse error: {exc}", f"{body}\nHTTP_CODE:{code}")

    pass_n = sum(1 for r in results if r["status"] == "PASS")
    fail_n = sum(1 for r in results if r["status"] == "FAIL")
    blocked_n = sum(1 for r in results if r["status"] == "BLOCKED")
    total = len(results)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rate = round(pass_n / max(total, 1) * 100, 1)

    lines = [
        "# 接口测试报告（API_TEST_REPORT）",
        "",
        "> 依据 `docs/API_TEST.md`，使用 curl 执行并自动生成。",
        "",
        "---",
        "",
        "## 1. 测试概要",
        "",
        "| 项 | 内容 |",
        "|----|------|",
        f"| 测试时间 | {now} |",
        f"| 环境 BASE_URL | {BASE_URL} |",
        "| 执行方式 | curl.exe（Windows） |",
        f"| 用例总数 | {total} |",
        f"| PASS | {pass_n} |",
        f"| FAIL | {fail_n} |",
        f"| BLOCKED | {blocked_n} |",
        f"| 通过率 | {rate}% |",
        "",
        "## 2. 用例结果",
        "",
        "| 编号 | 用例 | 结果 | 说明 |",
        "|------|------|------|------|",
    ]
    for r in results:
        lines.append(f"| {r['id']} | {r['name']} | **{r['status']}** | {r['detail']} |")

    lines.extend(["", "## 3. 响应摘要", ""])
    for r in results:
        lines.extend(
            [
                f"### {r['id']} {r['name']}",
                "",
                "```",
                r["evidence"],
                "```",
                "",
            ]
        )

    lines.append("## 4. 结论")
    lines.append("")
    if fail_n == 0 and blocked_n == 0:
        lines.append("全部用例通过，需求 2（医生列表）与需求 3（患者登录）相关接口符合预期。")
    elif blocked_n > 0:
        lines.append("存在 BLOCKED 用例，请检查服务/数据库环境后重跑。")
    else:
        lines.append("存在 FAIL 用例，请根据「响应摘要」排查。")

    lines.extend(
        [
            "",
            "## 5. 修订记录",
            "",
            "| 版本 | 日期 | 说明 |",
            "|------|------|------|",
            f"| v1.0 | {now[:10]} | 按 API_TEST.md 首次执行 |",
            "",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written: {REPORT_PATH}")
    print(f"PASS={pass_n} FAIL={fail_n} BLOCKED={blocked_n}")
    for r in results:
        print(f"{r['id']}\t{r['status']}\t{r['name']}\t{r['detail']}")

    return 1 if fail_n or blocked_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
