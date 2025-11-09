import os
from pathlib import Path
from jinja2 import Template
from playwright.sync_api import sync_playwright


class ThumbnailGenerator:
    def __init__(self, template_path: Path, output_html: Path, output_image: Path):
        self.template_path = template_path
        self.output_html = output_html
        self.output_image = output_image

    def _adjust_font_size(self, title: str, base_size=82, max_chars=40, min_size=48):
        length = len(title)
        if length <= max_chars:
            return base_size
        scale = max(min_size, base_size - (length - max_chars) * 1.2)
        return round(scale)

    def render_template(self, data: dict):
        if "title" in data and "font_size" not in data:
            data["font_size"] = self._adjust_font_size(data["title"])

        with self.template_path.open("r", encoding="utf-8") as f:
            template = Template(f.read())
        rendered = template.render(**data)
        self.output_html.write_text(rendered, encoding="utf-8")

    def capture_with_playwright(self, width=1280, height=720):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=1
            )
            page = context.new_page()
            page.goto(self.output_html.resolve().as_uri(), wait_until="networkidle")
            page.wait_for_timeout(200)
            thumbnail = page.query_selector(".thumbnail")
            if thumbnail is None:
                page.screenshot(path=str(self.output_image))
            else:
                thumbnail.screenshot(path=str(self.output_image))
            browser.close()

    def generate_thumbnail(self, data: dict, width=1280, height=720):
        self.render_template(data)
        self.capture_with_playwright(width, height)


# Exemplo de uso
if __name__ == "__main__":
    TEMPLATE_PATH = Path("templates/thumbnail_template.html")
    OUTPUT_HTML = Path("thumbnail_temp.html")
    OUTPUT_IMAGE = Path("thumbnail_output.png")

    data = {
        "title": "O Tabernáculo",
        "speaker": "Cleiton Cunha",
        "image_path": Path("thumbnails/original_thumbnail_2025-08-31_xnlHx7Ttk64.jpg").resolve().as_uri()
    }

    generator = ThumbnailGenerator(TEMPLATE_PATH, OUTPUT_HTML, OUTPUT_IMAGE)
    generator.generate_thumbnail(data)
    print("Thumbnail salva em:", OUTPUT_IMAGE)
