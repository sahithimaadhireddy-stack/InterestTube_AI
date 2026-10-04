import streamlit as st
import base64
from pathlib import Path
import speech_recognition as sr
import pyttsx3
from urllib.parse import quote_plus

from gemini_service import process_interests
from youtube_service import search_youtube


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="InterestTube AI",
    page_icon="🎬",
    layout="wide"
)


# =========================================================
# VOICE SEARCH FUNCTION
# =========================================================

def get_voice_input():

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            st.info(
                "🎤 Listening... Please speak now."
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        text = recognizer.recognize_google(
            audio
        )

        return text

    except sr.WaitTimeoutError:

        st.warning(
            "⏱️ I didn't hear anything. Please try again."
        )

        return ""

    except sr.UnknownValueError:

        st.warning(
            "❌ Sorry, I couldn't understand your voice."
        )

        return ""

    except sr.RequestError:

        st.error(
            "❌ Speech recognition service is unavailable."
        )

        return ""

    except Exception as e:

        st.error(
            f"❌ Microphone error: {e}"
        )

        return ""


# =========================================================
# AI VOICE RESPONSE FUNCTION
# =========================================================

def speak_response(message):

    try:

        engine = pyttsx3.init()

        engine.say(message)

        engine.runAndWait()

        engine.stop()

    except Exception as e:

        st.warning(
            f"🔊 Voice response could not be played: {e}"
        )


# =========================================================
# BACKGROUND IMAGE
# =========================================================

background_path = Path(__file__).parent / "background.png"

if background_path.exists():

    with open(background_path, "rb") as image_file:

        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(3, 5, 20, 0.30),
                    rgba(3, 5, 20, 0.78)
                ),
                url("data:image/png;base64,{encoded_image}");

            background-size: cover;
            background-position: center top;
            background-attachment: fixed;
            background-repeat: no-repeat;

            color: white;
        }}

        [data-testid="stAppViewContainer"] {{
            background: transparent;
        }}

        [data-testid="stMain"] {{
            background: transparent;
        }}

        .block-container {{
            max-width: 1250px;
            padding-top: 35px;
            padding-bottom: 60px;
            background: rgba(3, 5, 20, 0.12);
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        h1 {{
            text-align: center;

            font-size: 52px !important;
            font-weight: 900 !important;

            margin-bottom: 5px !important;

            background: linear-gradient(
                90deg,
                #ffffff,
                #9b5cff,
                #e879f9
            );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            text-shadow:
                0 0 20px rgba(124, 58, 237, 0.5);
        }}

        h2 {{
            color: white !important;
            font-weight: 800 !important;
        }}

        h3 {{
            color: white !important;
            font-weight: 750 !important;
        }}

        .stCaption {{
            color: #d4d4e8 !important;
        }}

        .stTextInput input {{
            background: rgba(12, 13, 35, 0.85) !important;

            color: white !important;

            border: 1px solid rgba(139, 92, 246, 0.65) !important;

            border-radius: 16px !important;

            height: 55px !important;

            font-size: 17px !important;

            padding-left: 18px !important;

            box-shadow:
                0 0 20px rgba(124, 58, 237, 0.15);
        }}

        .stTextInput input::placeholder {{
            color: #aaaac4 !important;
        }}

        .stTextInput input:focus {{
            border-color: #a855f7 !important;

            box-shadow:
                0 0 0 1px #a855f7,
                0 0 25px rgba(168, 85, 247, 0.35) !important;
        }}

        [data-baseweb="select"] > div {{
            background: rgba(12, 13, 35, 0.85) !important;

            border: 1px solid rgba(139, 92, 246, 0.55) !important;

            border-radius: 14px !important;

            color: white !important;
        }}

        .stButton button {{
            width: 100%;

            height: 55px;

            border-radius: 16px;

            border: 1px solid rgba(168, 85, 247, 0.7);

            background: linear-gradient(
                90deg,
                #5b21b6,
                #7c3aed,
                #9333ea
            );

            color: white !important;

            font-size: 17px;

            font-weight: 800;

            box-shadow:
                0 8px 25px rgba(124, 58, 237, 0.30);
        }}

        .stButton button:hover {{
            background: linear-gradient(
                90deg,
                #7c3aed,
                #9333ea,
                #c026d3
            );

            box-shadow:
                0 12px 35px rgba(168, 85, 247, 0.45);
        }}

        [data-testid="stMetric"] {{
            background: rgba(8, 10, 32, 0.80);

            border: 1px solid rgba(139, 92, 246, 0.35);

            border-radius: 18px;

            padding: 18px;

            min-height: 105px;

            box-shadow:
                0 8px 30px rgba(0, 0, 0, 0.25);

            backdrop-filter: blur(10px);
        }}

        [data-testid="stMetricLabel"] {{
            color: #c4b5fd !important;
        }}

        [data-testid="stMetricValue"] {{
            color: white !important;
            font-weight: 800 !important;
        }}

        [data-testid="stAlert"] {{
            background:
                linear-gradient(
                    135deg,
                    rgba(91, 33, 182, 0.30),
                    rgba(30, 41, 90, 0.65)
                ) !important;

            border: 1px solid rgba(168, 85, 247, 0.45) !important;

            border-radius: 20px !important;

            color: white !important;

            box-shadow:
                0 10px 35px rgba(0, 0, 0, 0.25);
        }}

        [data-testid="column"] {{
            background: rgba(7, 9, 28, 0.72);

            border: 1px solid rgba(139, 92, 246, 0.30);

            border-radius: 18px;

            padding: 12px;

            margin-bottom: 18px;

            box-shadow:
                0 8px 30px rgba(0, 0, 0, 0.30);

            backdrop-filter: blur(10px);
        }}

        [data-testid="column"]:hover {{
            border-color: rgba(168, 85, 247, 0.70);

            box-shadow:
                0 10px 35px rgba(124, 58, 237, 0.25);
        }}

        img {{
            border-radius: 13px !important;
        }}

        [data-testid="stLinkButton"] a {{
            border-radius: 12px !important;

            background: linear-gradient(
                90deg,
                #dc2626,
                #ef4444
            ) !important;

            border: none !important;

            color: white !important;

            font-weight: 700 !important;
        }}

        [data-testid="stLinkButton"] a:hover {{
            background: linear-gradient(
                90deg,
                #ef4444,
                #f43f5e
            ) !important;
        }}

        hr {{
            border: none !important;

            height: 1px !important;

            background: linear-gradient(
                90deg,
                transparent,
                rgba(139, 92, 246, 0.8),
                rgba(236, 72, 153, 0.8),
                transparent
            ) !important;

            margin-top: 30px !important;

            margin-bottom: 30px !important;
        }}

        footer {{
            visibility: hidden;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HEADER
# =========================================================

st.title("🎬 InterestTube AI")

st.caption(
    "AI-Powered Personalized YouTube Video Discovery"
)

st.write("")


# =========================================================
# SEARCH SECTION
# =========================================================

st.subheader(
    "🔎 What do you want to learn today?"
)

st.caption(
    "Enter your interests or use voice search and let AI discover relevant YouTube videos for you."
)


# =========================================================
# TEXT SEARCH
# =========================================================

user_interests = st.text_input(
    "Your interests",
    placeholder="Python, Java, Generative AI, Machine Learning",
    label_visibility="collapsed"
)


# =========================================================
# VOICE SEARCH
# =========================================================

st.write("")

voice_col1, voice_col2 = st.columns([3, 1])

with voice_col1:

    st.caption(
        "🎙️ Don't want to type? Speak your learning interests."
    )

with voice_col2:

    voice_button = st.button(
        "🎙️ Voice Search"
    )


# =========================================================
# PROCESS VOICE INPUT
# =========================================================

if voice_button:

    voice_text = get_voice_input()

    if voice_text:

        st.success(
            f"🎤 You said: {voice_text}"
        )

        user_interests = voice_text


st.write("")


# =========================================================
# OPTIONS
# =========================================================

option_col1, option_col2 = st.columns(2)

with option_col1:

    selected_language = st.selectbox(
        "🌐 Video Language",
        [
            "English",
            "Telugu",
            "Hindi",
            "Spanish",
            "French"
        ]
    )

with option_col2:

    videos_per_topic = st.selectbox(
        "🎬 Videos per Topic",
        [3, 6, 9, 12],
        index=1
    )


st.write("")


# =========================================================
# DISCOVER BUTTON
# =========================================================

discover_button = st.button(
    "🚀 Discover Videos"
)


# =========================================================
# DISCOVERY REQUEST
# =========================================================

discover_request = (
    discover_button
    or voice_button
)


# =========================================================
# MAIN LOGIC
# =========================================================

if discover_request:

    if not user_interests.strip():

        st.warning(
            "⚠️ Please enter at least one interest."
        )

    else:

        try:

            # =================================================
            # GEMINI PROCESSING
            # =================================================

            with st.spinner(
                "🤖 AI is understanding your interests..."
            ):

                topics = process_interests(
                    user_interests
                )


            # =================================================
            # GET YOUTUBE RESULTS
            # =================================================

            all_videos = []

            channel_names = set()

            topic_video_data = {}

            quota_error_topics = []


            with st.spinner(
                "🔎 Discovering personalized YouTube videos..."
            ):

                for topic in topics:

                    try:

                        videos = search_youtube(
                            topic,
                            videos_per_topic,
                            selected_language
                        )

                        topic_video_data[topic] = videos

                        all_videos.extend(videos)

                        for video in videos:

                            channel_names.add(
                                video["channel"]
                            )


                    except Exception as youtube_error:

                        error_text = str(
                            youtube_error
                        ).lower()

                        if (
                            "quota" in error_text
                            or "429" in error_text
                            or "ratelimit" in error_text
                            or "rate limit" in error_text
                        ):

                            topic_video_data[topic] = []

                            quota_error_topics.append(
                                topic
                            )

                        else:

                            raise youtube_error


            # =================================================
            # DISCOVERY DASHBOARD
            # =================================================

            st.divider()

            st.subheader(
                "📊 Discovery Dashboard"
            )

            dashboard_col1, dashboard_col2, dashboard_col3, dashboard_col4 = st.columns(4)

            with dashboard_col1:

                st.metric(
                    label="🎯 Topics Discovered",
                    value=len(topics)
                )

            with dashboard_col2:

                st.metric(
                    label="🎬 Videos Found",
                    value=len(all_videos)
                )

            with dashboard_col3:

                st.metric(
                    label="📺 Channels",
                    value=len(channel_names)
                )

            with dashboard_col4:

                st.metric(
                    label="🌐 Language",
                    value=selected_language
                )


            # =================================================
            # YOUTUBE QUOTA NOTICE
            # =================================================

            if quota_error_topics:

                st.warning(
                    "⚠️ YouTube API search quota is temporarily "
                    "unavailable. Your AI processing is working "
                    "correctly. Use the YouTube search links below "
                    "to continue exploring these topics."
                )


            # =================================================
            # AI LEARNING PROFILE
            # =================================================

            st.subheader(
                "🤖 AI Learning Profile"
            )

            st.info(
                f"""
Based on your interests, InterestTube AI identified
**{len(topics)} learning topics** and discovered
**{len(all_videos)} YouTube videos** in **{selected_language}**.

🎯 **Your current learning interests:**

{" • ".join(topics)}
"""
            )


            # =================================================
            # YOUR INTERESTS
            # =================================================

            st.subheader(
                "✨ Your AI-Processed Interests"
            )

            st.write(
                "  •  ".join(topics)
            )


            # =================================================
            # YOUTUBE RESULTS
            # =================================================

            for topic in topics:

                st.divider()

                st.header(
                    f"🎥 {topic}"
                )

                videos = topic_video_data.get(
                    topic,
                    []
                )


                if videos:

                    columns = st.columns(3)

                    for index, video in enumerate(videos):

                        with columns[index % 3]:

                            # ---------------------------------
                            # THUMBNAIL
                            # ---------------------------------

                            st.image(
                                video["thumbnail"],
                                use_container_width=True
                            )


                            # ---------------------------------
                            # VIDEO TITLE
                            # ---------------------------------

                            st.markdown(
                                f"**{video['title']}**"
                            )


                            # ---------------------------------
                            # CHANNEL
                            # ---------------------------------

                            st.caption(
                                f"📺 {video['channel']}"
                            )


                            # ---------------------------------
                            # YOUTUBE LINK
                            # ---------------------------------

                            st.link_button(
                                "▶ Watch on YouTube",
                                video["video_url"],
                                use_container_width=True
                            )


                else:

                    # =========================================
                    # QUOTA FALLBACK
                    # =========================================

                    if topic in quota_error_topics:

                        st.info(
                            f"🔎 YouTube API quota is currently "
                            f"unavailable for **{topic}**."
                        )

                        youtube_search_url = (
                            "https://www.youtube.com/results?search_query="
                            + quote_plus(topic)
                        )

                        st.link_button(
                            "▶ Search this topic on YouTube",
                            youtube_search_url,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            f"📭 No videos found for {topic}."
                        )


            # =================================================
            # AI VOICE RESPONSE
            # =================================================

            if voice_button:

                if len(quota_error_topics) > 0:

                    voice_message = (
                        f"I identified {len(topics)} learning topics. "
                        f"The YouTube search service is temporarily "
                        f"unavailable, but you can still search each "
                        f"topic directly on YouTube."
                    )

                elif len(all_videos) > 0:

                    voice_message = (
                        f"I found {len(topics)} learning topics "
                        f"and {len(all_videos)} YouTube videos "
                        f"for you. Happy learning!"
                    )

                else:

                    voice_message = (
                        "I could not find any videos for your "
                        "interests. Please try another topic."
                    )


                st.success(
                    "🔊 AI Voice Response: "
                    + voice_message
                )

                speak_response(
                    voice_message
                )


        except Exception as e:

            st.error(
                "❌ Something went wrong."
            )

            st.code(
                str(e)
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎬 InterestTube AI  •  Gemini AI  •  YouTube Data API  •  Python"
)