import os
import json
import asyncio
from typing import Dict
from playwright.async_api import async_playwright


class ExecutorAgent:
    """
    Executes a test case using Playwright Async API and captures artifacts
    """

    def __init__(self):
        self.base_artifact_path = "backend/artifacts"

        os.makedirs(f"{self.base_artifact_path}/screenshots", exist_ok=True)
        os.makedirs(f"{self.base_artifact_path}/dom", exist_ok=True)
        os.makedirs(f"{self.base_artifact_path}/logs", exist_ok=True)

    async def execute_test(self, url: str, test_case: Dict) -> Dict:
        print("🔥 ASYNC PLAYWRIGHT EXECUTOR RUNNING 🔥")

        test_id = test_case["id"]

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            console_logs = []

            page.on(
                "console",
                lambda msg: console_logs.append(
                    {"type": msg.type, "text": msg.text}
                )
            )

            # Open URL
            await page.goto(url, timeout=60000)
            await asyncio.sleep(3)

            # Screenshot BEFORE
            before_path = f"{self.base_artifact_path}/screenshots/{test_id}_before.png"
            await page.screenshot(path=before_path, full_page=True)

            # Safe interaction (generic)
            buttons = await page.query_selector_all("button")
            if buttons:
                try:
                    await buttons[0].click()
                    await asyncio.sleep(2)
                except Exception:
                    pass

            # Screenshot AFTER
            after_path = f"{self.base_artifact_path}/screenshots/{test_id}_after.png"
            await page.screenshot(path=after_path, full_page=True)

            # DOM snapshot
            dom_content = await page.content()
            dom_path = f"{self.base_artifact_path}/dom/{test_id}.html"
            with open(dom_path, "w", encoding="utf-8") as f:
                f.write(dom_content)

            # Console logs
            log_path = f"{self.base_artifact_path}/logs/{test_id}.json"
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(console_logs, f, indent=2)

            await browser.close()

        return {
            "test_id": test_id,
            "status": "executed",
            "artifacts": {
                "before_screenshot": before_path,
                "after_screenshot": after_path,
                "dom_snapshot": dom_path,
                "console_logs": log_path,
            },
        }
