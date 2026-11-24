"""Capturas reais da homepage na branch, sem sintetizar telas.
Instalar: pip install playwright; python -m playwright install chromium
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidencias" / "capturas"
OUTPUT.mkdir(parents=True, exist_ok=True)
URL = "http://127.0.0.1:8765"
DATE_LOCAL = "2026-11-23"  # Data editorial do projeto; horário da execução em generated_at_utc.

def wait_for_server():
    for _ in range(90):
        try:
            with urllib.request.urlopen(URL + "/api/health", timeout=2) as res:
                if res.status == 200:
                    return
        except Exception:
            time.sleep(.5)
    raise RuntimeError("A API não respondeu no endereço local, screenshots não produzidos")

def snap(page, path: str, full=False, selector=None):
    page.evaluate("() => document.fonts.ready")
    page.wait_for_timeout(350)
    if selector:
        page.locator(selector).screenshot(path=str(OUTPUT / path),animations="disabled",timeout=15000)
    else:
        page.screenshot(path=str(OUTPUT / path),full_page=full,animations="disabled",timeout=20000)
    print("CAPTURA", path)

def assert_no_overflow(page, label):
    widths=page.evaluate("""() => ({
      doc: document.documentElement.scrollWidth,
      viewport: window.innerWidth,
      body: document.body.scrollWidth
    })""")
    assert widths["doc"] <= widths["viewport"]+2, f"{label}: overflow horizontal na página: {widths}"
    return widths

def main():
    names = []
    metadata = {}
    with tempfile.TemporaryDirectory(prefix="nexo-alpha-capture-") as temp:
        env = dict(os.environ)
        env.update({
            "NEXO_DB_PATH": str(Path(temp) / "capture.sqlite3"),
            "NEXO_DEMO": "1",
            "NEXO_SECURE_COOKIES": "0",
            "NEXO_LEADS_ADMIN_EMAIL": "admin@nexo.local",
            "NEXO_RATE_LIMIT_SECRET": "local-only-screenshots-not-a-production-secret",
        })
        with open(Path(temp) / "server.log", "wb") as logfile:
            server=subprocess.Popen(
                [sys.executable,"-m","uvicorn","backend.main:app",
                 "--host","127.0.0.1","--port","8765"],
                cwd=str(ROOT / "alpha-snapshot"),env=env,
                stdout=logfile,stderr=subprocess.STDOUT)
            try:
                wait_for_server()
                with sync_playwright() as p:
                    browser=p.chromium.launch(headless=True,args=["--no-sandbox"])
                    desktop=browser.new_context(
                        viewport={"width":1440,"height":960},
                        device_scale_factor=1,reduced_motion="reduce",
                        locale="pt-BR",color_scheme="dark")
                    page=desktop.new_page()
                    page.goto(URL + "/",wait_until="domcontentloaded",timeout=30000)
                    page.locator(".briefing-preview").wait_for()
                    metadata["desktop"] = assert_no_overflow(page,"desktop")
                    snap(page,"home-hero-desktop.png")
                    snap(page,"home-completa-desktop.png",full=True)
                    snap(page,"home-comparativo.png",selector="#cotacao")
                    snap(page,"home-demonstracao.png",selector="#demonstracao")
                    page.locator(".login-trigger").click()
                    page.locator("#login-dialog[open]").wait_for()
                    snap(page,"home-login.png")
                    page.locator(".close-dialog").click()
                    names.extend(["home-hero-desktop.png","home-completa-desktop.png",
                        "home-comparativo.png","home-demonstracao.png","home-login.png"])
                    mobile=browser.new_context(
                        viewport={"width":390,"height":844},device_scale_factor=1,
                        is_mobile=True,has_touch=True,reduced_motion="reduce",
                        locale="pt-BR",color_scheme="dark")
                    mob=mobile.new_page()
                    mob.goto(URL + "/",wait_until="domcontentloaded",timeout=30000)
                    mob.locator(".briefing-preview").wait_for()
                    metadata["mobile"] = assert_no_overflow(mob,"mobile")
                    snap(mob,"home-mobile.png",full=True)
                    mob.locator(".menu-toggle").click()
                    assert mob.locator(".menu-toggle").get_attribute("aria-expanded") == "true"
                    snap(mob,"home-menu-mobile.png")
                    names.extend(["home-mobile.png","home-menu-mobile.png"])
                    browser.close()
            finally:
                server.terminate()
                try:server.wait(timeout=8)
                except subprocess.TimeoutExpired:server.kill()
    manifest={
        "date_reference_local":DATE_LOCAL,
        "generated_at_utc":datetime.now(timezone.utc).isoformat(),
        "commit_source":os.environ.get("GITHUB_SHA","local"),
        "branch":os.environ.get("GITHUB_REF_NAME","local"),
        "source":"Aplicação FastAPI servindo a homepage real de homepage/dist/",
        "auth_note":"Formulários de exemplo sobre banco efêmero, sem dados reais",
        "screenshots":names,
        "viewport_check":metadata,
        "disclaimer":"Capturas de branch de revisão; não são site de produção nem editor final do workspace"
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("OK:",len(names),"capturas. Manifesto salvo.")

if __name__ == "__main__":
    main()
