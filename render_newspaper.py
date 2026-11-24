#!/usr/bin/env python3
"""Render newspaper.html to frontpage.png (1024x1024) plus a 300px-wide legibility check.

Same Playwright method as render.py. No network is needed: the page is local
and all art is inline SVG.
"""
import hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PAGE = HERE / "newspaper.html"
OUT = HERE / "frontpage.png"
SMALL = Path("/tmp/news-image-24-frontpage-300px.png")

def sha256_of(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1024, "height": 1024},
                                device_scale_factor=1)
        page.goto(PAGE.as_uri())
        page.wait_for_timeout(400)
        page.screenshot(path=str(OUT))
        # Legibility check: same page at ~300px across.
        small = browser.new_page(viewport={"width": 1024, "height": 1024},
                                 device_scale_factor=300 / 1024)
        small.goto(PAGE.as_uri())
        small.wait_for_timeout(400)
        small.screenshot(path=str(SMALL))
        browser.close()
    print("wrote", OUT, OUT.stat().st_size, "bytes", "sha256", sha256_of(OUT))
    print("wrote", SMALL, SMALL.stat().st_size, "bytes")

if __name__ == "__main__":
    main()
