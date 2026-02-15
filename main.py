from youtube_video import YouTubeVideo
from iec_admin_panel import IECAdminPanel
from thumb_generator import ThumbnailGenerator
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

BASE_FONT_SIZE = 75

def main():
    USERNAME = os.getenv("ADMIN_PANEL_USERNAME")
    PASSWORD = os.getenv("ADMIN_PANEL_PASSWORD")

    YOUTUBE_LINKS = [
        'https://www.youtube.com/watch?v=hfEvH4QSrB8',
        'https://www.youtube.com/watch?v=ZmYy5pff53E',
        'https://www.youtube.com/watch?v=WmmvzdQQr4c',
        'https://www.youtube.com/watch?v=hOrL011wjLg'
    ]

    cms = IECAdminPanel()
    cms.login(USERNAME, PASSWORD)

    for link in YOUTUBE_LINKS:
        try:
            video = YouTubeVideo(link)
            video_data = video.get_video_data()

            # thumbnail_path = video.download_thumbnail_no_bg(save_path="thumbnails")
            filename = f"thumbnail_{video_data['id']}.png"
            thumbnail_path = video.download_thumbnail(save_path="thumbnails", filename=filename)

            title_parts = video_data['title'].rsplit(' - ', 1)
            title = video_data['title']
            preacher_name = title_parts[1].strip() if len(title_parts) > 1 else "Unknown"

            generator = ThumbnailGenerator(
                template_path=Path("templates/thumbnail_template.html"),
                output_html=Path("thumbnail_temp.html"),
                output_image=Path(f"thumbnails/{video_data['id']}_custom_thumbnail.png")
            )

            generator.generate_thumbnail({
                "title": title_parts[0].strip(),
                "speaker": preacher_name,
                "image_path": Path(thumbnail_path).resolve().as_uri(),
                "font_size": BASE_FONT_SIZE,
                "badge_content": video_data['publish_date'].strftime("%d/%m/%Y")
            })

            cms.add_pregacao(
                link=link,
                title=title,
                description=video_data['description'],
                publish_date=video_data['publish_date'].strftime("%Y-%m-%dT%H:%M:%SZ"),
                preacher_name=preacher_name
            )

            print(f"Video '{video_data['title']}' processed successfully.")

        except Exception as e:
            print(f"Error while processing video '{link}': {e}")

    cms.close()

if __name__ == '__main__':
    main()
