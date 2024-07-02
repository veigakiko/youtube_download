import streamlit as st
from pytube import YouTube
import os

def download_youtube_video(url, output_path, file_format, progress_callback):
    try:
        yt = YouTube(url, on_progress_callback=progress_callback)

        if file_format == "MP4":
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        elif file_format == "MP3":
            stream = yt.streams.filter(only_audio=True).first()

        stream.download(output_path)
        if file_format == "MP3":
            base = stream.default_filename
            new_file = base.replace(".mp4", ".mp3")
            output_file = os.path.join(output_path, new_file)
            os.rename(os.path.join(output_path, stream.default_filename), output_file)

        st.success(f"Download completed: {yt.title}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    st.title("YouTube Video Downloader")

    url = st.text_input("YouTube URL")
    output_path = st.text_input("Output Path", value=os.getcwd())
    file_format = st.radio("Format", options=["MP3", "MP4"])

    if st.button("Download"):
        if url and output_path and file_format:
            progress_bar = st.progress(0)
            def progress_function(stream, chunk, bytes_remaining):
                total_size = stream.filesize
                bytes_downloaded = total_size - bytes_remaining
                percentage = (bytes_downloaded / total_size) * 100
                progress_bar.progress(int(percentage))

            download_youtube_video(url, output_path, file_format, progress_function)
        else:
            st.warning("Please provide URL, output path, and select a format.")

if __name__ == "__main__":
    main()
