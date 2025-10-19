import requests
import os
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from rembg import remove
from dotenv import load_dotenv

load_dotenv()

class YouTubeVideo:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    YOUTUBE_API_URL = os.getenv("YOUTUBE_API_URL")

    def __init__(self, video_url):
        self.video_url = video_url
        self.video_id = self.extract_video_id()

        params = {
            'id': self.video_id,
            'key': self.YOUTUBE_API_KEY,
            'part': 'snippet'
        }

        response = requests.get(self.YOUTUBE_API_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            if 'items' in data and data['items']:
                self.data = data
                print("Video data retrieved successfully.")
            else:
                raise ValueError(f"No video data found for: {self.video_url}")
        else:
            raise ValueError(f"Error while trying to gather video data: {self.video_url}")

    def extract_video_id(self):
        """
        Extracts the video ID from different YouTube URL formats.
        """
        parsed_url = urlparse(self.video_url)

        if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
            video_id = parse_qs(parsed_url.query).get("v")
            if video_id:
                return video_id[0]

        elif parsed_url.hostname in ("youtu.be",):
            return parsed_url.path.lstrip('/')

        return None

    def get_video_data(self):
        """
        Returns a dictionary with video title, description, and publish date.
        """
        snippet = self.data['items'][0]['snippet']
        return {
            'title': snippet['title'],
            'description': snippet['description'],
            'publish_date': snippet['publishedAt']
        }

    def get_thumbnail_url(self):
        """
        Retrieves the best available thumbnail URL.
        """
        snippet = self.data['items'][0]['snippet']
        thumbnails = snippet['thumbnails']
        best_quality = ["maxres", "standard", "high", "medium", "default"]

        for quality in best_quality:
            if quality in thumbnails:
                return thumbnails[quality]['url']

        return None

    def download_thumbnail(self, save_path, filename):
        """
        Downloads the video thumbnail and saves it to the specified path with the given filename.
        """
        thumbnail_url = self.get_thumbnail_url()
        if not thumbnail_url:
            raise ValueError("No thumbnail available for this video.")

        response = requests.get(thumbnail_url, stream=True)
        if response.status_code == 200:
            os.makedirs(save_path, exist_ok=True)
            file_path = os.path.join(save_path, filename)

            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print(f"Thumbnail saved at: {file_path}")
            return file_path
        else:
            raise ValueError("Failed to download the thumbnail.")

    def download_thumbnail_no_bg(self, save_path):
        """
        Downloads the video thumbnail, removes its background, and saves the processed image
        with the video’s publish date included in the filename.
        """
        # Extract publish date
        video_data = self.get_video_data()
        publish_date_str = video_data.get('publish_date', 'unknown_date')

        try:
            # Convert ISO date format to YYYY-MM-DD
            publish_date = datetime.strptime(publish_date_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        except ValueError:
            publish_date = "unknown_date"

        # Define filenames
        original_filename = f"original_thumbnail_{publish_date}_{self.video_id}.jpg"
        output_filename = f"thumbnail_no_bg_{publish_date}_{self.video_id}.png"

        # Download the original thumbnail
        original_path = self.download_thumbnail(save_path, original_filename)

        # Read original image
        with open(original_path, 'rb') as input_file:
            original_data = input_file.read()

        # Remove background
        processed_data = remove(original_data)

        # Ensure save path exists
        os.makedirs(save_path, exist_ok=True)

        # Save the processed image
        final_path = os.path.join(save_path, output_filename)
        with open(final_path, 'wb') as output_file:
            output_file.write(processed_data)

        print(f"Thumbnail with background removed saved at: {final_path}")
        return final_path
