import streamlit as st
from api_calling import note_generator, audio_transcription, quiz_generator
from PIL import Image

st.title("Note Summary and Quiz Generator")
st.markdown("Upload upto 3 images to generate Note Summary and Quizzes")
st.divider()

with st.sidebar:
    st.header("Controls")
    images = st.file_uploader(
        "Uploade images of your note",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True
    )

    pil_images = []

    for img in images:
        pil_img = Image.open(img)
        pil_images.append(pil_img)

    if images:
        if len(images)>3:
            st.error("Uploade at max 3 images")
        else:
            st.subheader("Your Uploaded images")

            col = st.columns(len(images))

            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)

    selected_options = st.selectbox(
        "Select the difficulty of your quiz",
        ("Easy", "Medium", "Hard"),
        index=None

    )    

    pressed = st.button("Click here to initiate AI", type="primary") 

if pressed:
    if not images:
        st.error("You must upload one image")
    if not selected_options:
        st.error("You must select a difficulty")

    if images and selected_options:

        with st.container(border=True):
            st.subheader("Your Note")

            with st.spinner("Ai is writing notes for you"):

                generated_notes = note_generator(pil_images)
                st.markdown(generated_notes)     

        with st.container(border=True):
            st.subheader("Audio Transcription")

            with st.spinner("Ai is generating audio transcript for you"):

                generated_notes = generated_notes.replace("#","")
                generated_notes = generated_notes.replace("*","")
                generated_notes = generated_notes.replace("-","")
                generated_notes = generated_notes.replace("$","")
                generated_notes = generated_notes.replace(":","")

                audio_transcript = audio_transcription(generated_notes)  
                st.audio(audio_transcript)


        with st.container(border=True):
            
            st.subheader(f"Quiz ({selected_options}) Difficulty")

            with st.spinner("Ai is generating the quizzes"):
                quizzes = quiz_generator(pil_images,selected_options)
                st.markdown(quizzes)                   