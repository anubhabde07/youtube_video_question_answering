from serpapi import GoogleSearch
import streamlit as st

def get_youtube_transcript(video_id):
    api_key = st.secrets["SERPAPI_KEY"]
    params = {
        "api_key": api_key,
        "engine": "youtube_video_transcript",
        "v": video_id
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        if "transcript" in results:
            # We use 'snippet' because that is the key where SerpApi stores the text
            full_transcript = " ".join([s.get("snippet", "") for s in results["transcript"]])
            return full_transcript
        else:
            print(f"Error from SerpApi: {results.get('error', 'No transcript found')}")
            return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    except Exception as e:
        print("ERROR TYPE:", type(e))
        print("ERROR MESSAGE:", str(e))




