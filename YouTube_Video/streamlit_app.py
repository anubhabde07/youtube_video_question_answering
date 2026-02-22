import streamlit as st
from utils.transcript import get_youtube_transcript
from utils.vectorstore import create_vectorstore
from utils.chain import build_chain
from utils.url_to_id import get_videoID

st.title("YouTube Transcript ChatBot")

video_url = st.text_input("Enter YouTube Video URL")
# api_key = st.text_input("Enter api key")

video_id = ""
if video_url:
    video_id += get_videoID(video_url)

if video_id:
    transcript = get_youtube_transcript(video_id)

    if not transcript:
        st.error("Transcript could not be fetched.")
        st.stop()
    else:
        vectorStore = create_vectorstore(transcript)
        chain = build_chain(vectorStore)

        query = st.text_input("Ask a question")

        if query:
            answer = chain.invoke(query)

            st.write(answer)




