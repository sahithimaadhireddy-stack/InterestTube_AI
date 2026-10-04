import os

from dotenv import load_dotenv
from googleapiclient.discovery import build


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")


# =========================================================
# YOUTUBE API CLIENT
# =========================================================

youtube = build(
    "youtube",
    "v3",
    developerKey=api_key
)


# =========================================================
# LANGUAGE MAPPING
# =========================================================

LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Spanish": "es",
    "French": "fr"
}


# =========================================================
# LANGUAGE SEARCH KEYWORDS
# =========================================================

LANGUAGE_KEYWORDS = {
    "English": "English",
    "Hindi": "Hindi",
    "Telugu": "Telugu Telugu-language",
    "Spanish": "Spanish",
    "French": "French"
}


# =========================================================
# SEARCH YOUTUBE
# =========================================================

def search_youtube(
    topic,
    max_results=6,
    language="English"
):

    # -----------------------------------------------------
    # Get YouTube language code
    # -----------------------------------------------------

    language_code = LANGUAGE_CODES.get(
        language,
        "en"
    )


    # -----------------------------------------------------
    # Get language keyword
    # -----------------------------------------------------

    language_keyword = LANGUAGE_KEYWORDS.get(
        language,
        "English"
    )


    # -----------------------------------------------------
    # Create language-aware search query
    # -----------------------------------------------------

    if language == "English":

        search_query = topic

    else:

        search_query = f"{topic} {language_keyword}"


    # -----------------------------------------------------
    # Create YouTube search request
    # -----------------------------------------------------

    request = youtube.search().list(
        part="snippet",

        q=search_query,

        type="video",

        maxResults=max_results,

        relevanceLanguage=language_code,

        regionCode="IN"
    )


    # -----------------------------------------------------
    # Execute API request
    # -----------------------------------------------------

    response = request.execute()


    # -----------------------------------------------------
    # Store videos
    # -----------------------------------------------------

    videos = []


    # -----------------------------------------------------
    # Process results
    # -----------------------------------------------------

    for item in response.get("items", []):

        # Make sure the result contains a video ID
        if "videoId" not in item.get("id", {}):
            continue


        video_id = item["id"]["videoId"]


        # -------------------------------------------------
        # Create video object
        # -------------------------------------------------

        video = {

            "title": item["snippet"]["title"],

            "channel": item["snippet"]["channelTitle"],

            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],

            "video_url":
                f"https://www.youtube.com/watch?v={video_id}"
        }


        videos.append(video)


    # -----------------------------------------------------
    # Return videos
    # -----------------------------------------------------

    return videos