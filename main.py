from youtube_video import YouTubeVideo
from iec_admin_panel import IECAdminPanel
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    USERNAME = os.getenv("ADMIN_PANEL_USERNAME")
    PASSWORD = os.getenv("ADMIN_PANEL_PASSWORD")

    YOUTUBE_LINKS = [
        'https://www.youtube.com/watch?v=SN7KqSAiw5g',
        'https://www.youtube.com/watch?v=aTGTfI5OzYY',
        'https://www.youtube.com/watch?v=ppFiuirk3sU',
        'https://www.youtube.com/watch?v=8RYhTUQf39c',
        'https://www.youtube.com/watch?v=8RYhTUQf39c'
    ]

    cms = IECAdminPanel()
    cms.login(USERNAME, PASSWORD)

    for link in YOUTUBE_LINKS:
        try:
            video = YouTubeVideo(link)
            video_data = video.get_video_data()

            video.download_thumbnail_no_bg(save_path="thumbnails")

            title_parts = video_data['title'].rsplit(' - ', 1)
            title = video_data['title']
            preacher_name = title_parts[1].strip() if len(title_parts) > 1 else "Unknown"

            cms.add_pregacao(
                link=link,
                title=title,
                description=video_data['description'],
                publish_date=video_data['publish_date'],
                preacher_name=preacher_name
            )

            print(f"Video '{video_data['title']}' processed successfully.")

        except Exception as e:
            print(f"Error while processing video '{link}': {e}")

    cms.close()

if __name__ == '__main__':
    main()
