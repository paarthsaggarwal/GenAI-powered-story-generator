from story import *
from gtts import gTTS # importing google text to speech module (used for video audio)
from moviepy.editor import * # importing moviepy (used for combining video audio and images)
import os 
from dotenv import find_dotenv, load_dotenv # importing dotenv to acquire the path to the API keys in the .env file

# Acquiring the path to the .env file which contains the API keys
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Acquiring the API Keys of OpenAI and ElevenLabs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Setting te layout of the page using streamlit
st.set_page_config(page_title='GenAI powered stories for younger kids', page_icon="🔥",
                   layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("GenAI powered creative approach to create stories for younger kids")
st.sidebar.title("Pick a name of the character, a character, genre, setting, plot")


name = st.sidebar.text_input("Select a name for the character", value = "", max_chars = 15)

character = st.sidebar.selectbox("Select a character:", ('Huntsman', 'Fairy', 'King', "Lion"))  

genre = st.sidebar.selectbox("Select a Genre:", ('Action', 'Adventure', 'Fantasy', 'Mystery'))

setting = st.sidebar.selectbox("Select a setting:", ('enchanted forest', 'large castle centuries ago', 'A magical world'))

plot = st.sidebar.selectbox("Select an initial plot:", ('baboon king is threathening all animals and stealing their food', 'a mission to break the spell that has been cast on the kingdom' , 'discovery of a secret portal hat allows travel to world of danger and excitement'))

options = ["Bella", "Arnold", "Elli", "Josh"]
voice = st.sidebar.selectbox("Select a voice to narrate the story:", options)

# Using an if statement to detect whether user presses the "Generate Mew Story" button
if st.sidebar.button("Generate New Story"):
    generated_text = generate_story(name, character, genre, setting, plot)
    with open("generated_text.txt", "w") as file:
        file.write(generated_text.strip())
    st.subheader("The story is shown below")
    st.write(generated_text)

    audio = generate_audio(generated_text, voice) # generating audio
    
    st.subheader("The audio which narrates the story is shown below")
    st.audio(audio, format='audio/mp3')

    paragraphs = re.split(r"[,.]", generated_text)
   
    i=1
    for para in paragraphs[:-1]:
        response = openai.Image.create(
        prompt=para.strip(),
        n=1,
        size="512x512"
        )
        image_url = response['data'][0]['url']
        urllib.request.urlretrieve(image_url, f"images/image{i}.jpg")
        tts = gTTS(text=para, lang='en', slow=False)
        tts.save(f"audio/voiceover{i}.mp3") # saving audio in a directory called audio
        # Loading the audio file using moviepy
        audio_clip = AudioFileClip(f"audio/voiceover{i}.mp3")
        audio_duration = audio_clip.duration

        # Loading the image files using moviepy
        image_clip = ImageClip(f"images/image{i}.jpg").set_duration(audio_duration)

        # Use moviepy to create a text clip from the text
        text_clip = TextClip(para, font="Lane", size=(400, 0), color="black", bg_color="aqua")
        text_clip = text_clip.set_pos('center').set_duration(audio_duration)

        # Use moviepy to create a video for each "paragraph" by concatenating
        clip = image_clip.set_audio(audio_clip)
        video = CompositeVideoClip([clip, text_clip])

        # Save the videos in a directory
        video = video.write_videofile(f"videos/video{i}.mp4", fps=24)


        i+=1
    image_folder = "images"
    # Get a list of image files in the folder
    image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    st.subheader("The images for the story is shown below")
    st.image(image_files) # displaying images on website using streamlit 

    clips = []
    l_files = os.listdir("videos")
    for file in l_files:
        clip = VideoFileClip(f"videos/{file}")
        clips.append(clip)

    # Merging the audio and image files to create a final video
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.write_videofile("final_video.mp4")

    video_file = open('final_video.mp4', 'rb') 
    video_bytes = video_file.read() 
    st.subheader("The video narrating the story with images is shown below")
    st.video(video_bytes) #displaying the final video using streamlit

else:
    st.write("Click the button to generate the story.")