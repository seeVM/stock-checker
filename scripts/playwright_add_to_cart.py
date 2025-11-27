import os
import time
import sys
from playwright.sync_api import sync_playwright

# ------- CONFIG -------
PRODUCT_URL = "https://shop.iqoo.com/in/product/2038?skuId=8246"
# Persistent profile stores login/session. Change path if you want.
USER_DATA_DIR = os.path.expanduser("~/iqoo_playwright_profile")
# How long to keep browser open after actions (ms)
KEEP_OPEN_MS = 5 * 60 * 1000  # 5 minutes
# Add small human-like delays (seconds)
CLICK_DELAY = 0.25
# CSS/XPath/text selectors to try (ordered)
SELECTORS = [
    "text=Add to cart",
    "button:has-text('Add to cart')",
    "text=Add to Cart",
    "text=Buy now",
    "button:has-text('Buy Now')",
    "button.add-to-cart",
    "button#add-to-cart",
    "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to cart')]",
]
# ------- END CONFIG -------

def try_click(page):
    """Try selectors in order and click the first matching visible element."""
    for sel in SELECTORS:
        try:
            locator = page.locator(sel)
            if locator.count() > 0:
                # choose the first visible one
                for i in range(locator.count()):
                    el = locator.nth(i)
                    if el.is_visible():
                        print(f"Found selector: {sel} (index {i}), clicking...")
                        el.scroll_into_view_if_needed()
                        time.sleep(CLICK_DELAY)
                        el.click(force=True)
                        time.sleep(0.5)
                        return True
        except Exception as e:
            print("Selector check error for", sel, "->", e)
    return False

def run_once():
    with sync_playwright() as p:
        # launch persistent context so login persists between runs
        print("Launching Chromium with user data dir:", USER_DATA_DIR)
        browser = p.chromium.launch_persistent_context(USER_DATA_DIR, headless=False,
                                                       args=["--start-maximized"])
        page = browser.new_page()
        page.goto(PRODUCT_URL, wait_until="domcontentloaded")
        time.sleep(2)

        # debug helper: save screenshot in case selectors fail
        try:
            page.screenshot(path="playwright_debug_initial.png", full_page=True)
        except Exception:
            pass

        clicked = try_click(page)
        if clicked:
            print("Clicked add-to-cart / buy. Attempting to go to cart/checkout page.")
            # try to open common cart/checkout pages
            try:
                page.goto("https://shop.iqoo.com/in/cart", wait_until="domcontentloaded")
                time.sleep(1)
            except Exception:
                pass
            # take a screenshot of cart for debugging
            try:
                page.screenshot(path="playwright_debug_after_click.png", full_page=True)
            except Exception:
                pass
            print("Please complete checkout manually in the opened browser.")
        else:
            print("No matching add-to-cart / buy selector found. Saved screenshot as playwright_debug_initial.png")
            print("Check page and update SELECTORS if needed.")

        # keep browser open so user can interact (login / finish checkout)
        try:
            print(f"Keeping browser open for {KEEP_OPEN_MS/1000:.0f} seconds...")
            page.wait_for_timeout(KEEP_OPEN_MS)
        except KeyboardInterrupt:
            pass
        browser.close()

if __name__ == "__main__":
    run_once()
