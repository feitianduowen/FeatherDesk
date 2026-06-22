"""
添加 5 个国内可访问、不需要登录的网站。

选择标准:
1. 国内网络可直接访问
2. 不需要登录即可使用核心功能
3. 页面结构清晰，易于自动化
4. 有明确的搜索/导航功能
"""

from __future__ import annotations

import base64
import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.browser_manager import get_browser_manager, reset_browser_manager
from src.core.script_engine import get_script_engine, reset_script_engine
from src.core.script_generator import ScriptGenerator
from src.layer_2.controls import get_controls_exports


# ---------------------------------------------------------------------------
# 视觉模型配置
# ---------------------------------------------------------------------------

VISION_API_BASE = "https://token-plan-cn.xiaomimimo.com/v1"
VISION_API_KEY = os.getenv("VISION_API_KEY", "")
VISION_MODEL = "mimo-v2.5"


# ---------------------------------------------------------------------------
# 5 个新网站的任务定义
# ---------------------------------------------------------------------------

NEW_TASKS = [
    {
        "id": "17.1",
        "site": "juejin",
        "task": "在掘金搜索Python",
        "expected": "页面包含Python相关内容，显示了文章或教程列表",
        "search_url": "juejin.cn/search",
        "keywords": ["Python"],
        "priority": 1,
    },
    {
        "id": "18.1",
        "site": "ithome",
        "task": "在IT之家搜索人工智能",
        "expected": "页面包含IT之家内容，显示了新闻或文章",
        "search_url": "ithome.com",
        "keywords": ["人工智能"],
        "priority": 1,
    },
    {
        "id": "19.1",
        "site": "runoob",
        "task": "在菜鸟教程搜索Python",
        "expected": "页面包含Python教程内容",
        "search_url": "runoob.com",
        "keywords": ["Python"],
        "priority": 1,
    },
    {
        "id": "20.1",
        "site": "oschina",
        "task": "在开源中国搜索机器学习",
        "expected": "页面包含机器学习相关内容",
        "search_url": "oschina.net",
        "keywords": ["机器学习"],
        "priority": 1,
    },
    {
        "id": "21.1",
        "site": "segmentfault",
        "task": "在思否搜索Python爬虫",
        "expected": "页面包含Python爬虫相关技术文章",
        "search_url": "segmentfault.com",
        "keywords": ["Python"],
        "priority": 1,
    },
]


# ---------------------------------------------------------------------------
# 网站配置
# ---------------------------------------------------------------------------

SITE_CONFIGS = {
    "juejin": {
        "url": "https://juejin.cn/search?query=",
        "name": "掘金",
        "search_type": "url",  # URL 直接搜索
    },
    "ithome": {
        "url": "https://www.ithome.com/search?word=",
        "name": "IT之家",
        "search_type": "url",
    },
    "runoob": {
        "url": "https://www.runoob.com/?s=",
        "name": "菜鸟教程",
        "search_type": "url",
    },
    "oschina": {
        "url": "https://www.oschina.net/search?q=",
        "name": "开源中国",
        "search_type": "url",
    },
    "segmentfault": {
        "url": "https://segmentfault.com/search?q=",
        "name": "思否",
        "search_type": "url",
    },
}


# ---------------------------------------------------------------------------
# 脚本生成
# ---------------------------------------------------------------------------


def generate_script(site: str, keyword: str) -> str:
    """为指定网站生成搜索脚本。"""
    cfg = SITE_CONFIGS.get(site)
    if not cfg:
        return None

    if cfg["search_type"] == "url":
        return (
            f'goto("{cfg["url"]}{keyword}")\n'
            f'wait_for_navigation()\n'
            f'wait(5)\n'
            f'log("{cfg["name"]}搜索完成: {keyword}")'
        )
    else:
        # 表单搜索
        inp = cfg.get("input", "input[type='search']")
        btn = cfg.get("submit", "button[type='submit']")
        return (
            f'goto("{cfg["url"]}")\n'
            f'wait_for_navigation()\n'
            f"run_js('document.querySelector(\\\"{inp}\\\").value = \\\"{keyword}\\\"')\n"
            f"run_js('document.querySelector(\\\"{btn}\\\").click()')\n"
            f'wait(5)\n'
            f'log("{cfg["name"]}搜索完成: {keyword}")'
        )


# ---------------------------------------------------------------------------
# 视觉验证
# ---------------------------------------------------------------------------


def verify_with_vision(screenshot_path: str, expected: str) -> dict:
    """用视觉模型验证截图。"""
    with open(screenshot_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    prompt = f"""你是一个网页测试验证专家。请分析这张截图，判断是否符合预期。

预期行为: {expected}

请严格按以下 JSON 格式返回:
{{"passed": true/false, "reason": "简短原因", "details": "详细分析"}}"""

    try:
        response = httpx.post(
            f"{VISION_API_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {VISION_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": VISION_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}},
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
                "max_tokens": 500,
            },
            timeout=60.0,
        )
        response.raise_for_status()
        data = response.json()
        msg = data["choices"][0]["message"]
        content = msg.get("content", "") or msg.get("reasoning_content", "")

        json_start = content.find("{")
        json_end = content.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            result = json.loads(content[json_start:json_end])
            return {
                "passed": result.get("passed", False),
                "reason": result.get("reason", ""),
                "details": result.get("details", ""),
            }

        return {"passed": False, "reason": "无法解析返回", "details": content}
    except Exception as e:
        return {"passed": False, "reason": f"API调用失败: {e}", "details": ""}


# ---------------------------------------------------------------------------
# 测试循环
# ---------------------------------------------------------------------------


def run_tests():
    """运行 5 个新网站的测试。"""
    import base64

    results = []
    total = len(NEW_TASKS)

    print(f"\n{'='*60}")
    print(f"测试 5 个新网站")
    print(f"总任务数: {total}")
    print(f"{'='*60}\n")

    for i, task in enumerate(NEW_TASKS, 1):
        print(f"\n[{i}/{total}] 任务 {task['id']}: {task['task']}")
        print(f"  网站: {task['site']}")

        # 生成脚本
        keyword = task["keywords"][0] if task["keywords"] else ""
        script = generate_script(task["site"], keyword)

        if not script:
            print(f"  无法生成脚本")
            results.append({"id": task["id"], "site": task["site"], "status": "SKIP", "reason": "无法生成脚本"})
            continue

        print(f"  脚本: {script[:80]}...")

        # 重置并执行
        reset_browser_manager()
        reset_script_engine()

        try:
            bm = get_browser_manager()
            bm.launch(headless=True)

            engine = get_script_engine()
            engine.register_functions(get_controls_exports())

            result = engine.execute(script)
            print(f"  执行: {'成功' if result.success else '失败'}")
            print(f"  URL: {bm.get_page().url}")

            # 截图
            screenshot_path = f"logs/test_{task['id']}.png"
            os.makedirs("logs", exist_ok=True)
            bm.get_page().screenshot(path=screenshot_path, full_page=True)

            # 视觉验证
            if VISION_API_KEY:
                print(f"  视觉验证中...")
                vision = verify_with_vision(screenshot_path, task["expected"])
                print(f"  结果: {'PASS' if vision['passed'] else 'FAIL'}")
                print(f"  原因: {vision['reason']}")

                if vision["passed"]:
                    results.append({"id": task["id"], "site": task["site"], "status": "PASS", "reason": vision["reason"]})
                else:
                    results.append({"id": task["id"], "site": task["site"], "status": "FAIL", "reason": vision["reason"]})
            else:
                # 无视觉验证，检查 URL
                url = bm.get_page().url
                cfg = SITE_CONFIGS.get(task["site"], {})
                search_url = cfg.get("url", "")
                if search_url and keyword in url:
                    results.append({"id": task["id"], "site": task["site"], "status": "PASS", "reason": "URL 包含搜索词"})
                    print(f"  结果: PASS (URL 包含搜索词)")
                else:
                    results.append({"id": task["id"], "site": task["site"], "status": "FAIL", "reason": "URL 不包含搜索词"})
                    print(f"  结果: FAIL (URL 不包含搜索词)")

            bm.close()
        except Exception as e:
            print(f"  异常: {e}")
            results.append({"id": task["id"], "site": task["site"], "status": "ERROR", "reason": str(e)})
            try:
                reset_browser_manager()
            except:
                pass

    # 报告
    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"\n{'='*60}")
    print(f"测试报告")
    print(f"{'='*60}")
    print(f"总任务数: {total}")
    print(f"通过: {passed}")
    print(f"失败: {total - passed}")
    print(f"通过率: {passed/total*100:.1f}%")
    print()
    for r in results:
        print(f"  {r['id']:5s} {r['site']:10s} {r['status']:5s} {r['reason'][:40]}")
    print(f"{'='*60}")

    # 保存报告
    report = {
        "timestamp": time.time(),
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total * 100, 1),
        "results": results,
    }
    with open("new_sites_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: new_sites_report.json")


if __name__ == "__main__":
    run_tests()
