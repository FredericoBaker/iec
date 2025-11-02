from playwright.sync_api import sync_playwright

# Caminho para seu arquivo HTML
html_file = "thumbnails\template_2.html"
output_png = "thumbnail.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    page.goto(f"file:///{html_file}")
    page.screenshot(path=output_png)
    browser.close()

print("✅ Thumbnail salva como", output_png)
