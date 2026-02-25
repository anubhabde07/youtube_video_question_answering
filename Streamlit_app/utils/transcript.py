from serpapi import GoogleSearch
import streamlit as st

SERPAPI_API_KEY = st.secrets["SERPAPI_API_KEY"]

def get_transcript(video_id: str):
    try:
        params = {
            "api_key": SERPAPI_API_KEY,
            'engine': 'youtube_video_transcript',
            'v': video_id
        }

        search = GoogleSearch(params)
        result = search.get_dict()

        return '\n\n'.join(s.get('snippet', '') for s in result['transcript'])
    
    except Exception as e:
        print(f"Error has occured. ", e)
        return ''

   
