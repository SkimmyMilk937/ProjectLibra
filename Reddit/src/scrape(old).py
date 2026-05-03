import argparse
import os
import sys
import google.generativeai as genai
import praw
import random
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *

dir = os.getcwd()

def main(numPosts):
    
    clips = os.listdir(f"{dir}/morgs/clips")
    nums = int(numPosts)

    GOOGLE_API_KEY=('xxxxxxxxxxxxxxxxxxxxxxxxxx')
    genai.configure(api_key=GOOGLE_API_KEY)


    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    
    reddit = praw.Reddit(client_id="xxxxxxxxxxxxx", 
                            client_secret="xxxxxxxxxxxxxx",
                            user_agent="xxxxxxxxxxxxx",
                            username="xxxxxxxxxxxxxxxxxxxxxx",
                            password="xxxxxxxxxxxxxxxxx"
                            )
    
    try:
        subs = open("morgs/subreddits.txt", "r").read().splitlines()
        querys = open("morgs/querys.txt", "r").read().splitlines()
        ids = open("morgs/postIDS.txt", "r").read().splitlines()
        message = open("morgs/message.txt", "r").read()
    except:
        print("Text files are not written :(")
        print("Please fill them in now and then try again")
        sys.exit()

    
    for x in subs:
        subreddit = reddit.subreddit(x)
        for quest in querys:
            for post in subreddit.search(query=quest, sort="new", limit=nums):
                if "?" in post.title and not(post.stickied) and not(post.id in ids):
                    f = open(f"{dir}/postIDS.txt", "a")
                    submission = reddit.submission(post.id)
                    f.write(post.id + "\n")
                    f.close()
                    
                        
                    f = open(f"{dir}/log.txt", "a")
                    f.write(f"Written to postIDLIST: {post.id}\n")
                    f.write("Read message from message.txt\n")
                    
                    response = model.generate_content(post.title + "answer should be less than 300 tokens and read like a person is giving advice", safety_settings=True)
                    text = response.text.replace("**", "")
                    text.replace("* ", "")
                    text = (post.title + "\n" + text).replace("\n", "")
                    f.write(f"Got gemani response. {post.id}")
                    tts(text, post.id)

                    clipToUse = (random.choice(clips))
                    clip = VideoFileClip(f"morgs/clips/{clipToUse}")
                    audioToUse = AudioFileClip(f"{dir}/morgs/speech/{post.id}.mp3") #1efnj42
                    clip = clip.set_audio(audioToUse)
                    clip.write_videofile(filename=f"{dir}/morgs/shorts/{clipToUse}", threads=12)
                    f.write(f"Made video {post.id}")
                    os.system(f"python YoutubeShorts/youtube_uploader_selenium/upload.py --video=morgs/shorts/{clipToUse} --profile=C:/Users/nicol/AppData/Roaming/Mozilla/Firefox/Profiles/suu68dnw.default-release")
                    f.write("Uploaded to Youtube")
                    
                    response = model.generate_content(post.title) #reddit full length response
                    
                    try:
                        reddit.redditor(submission.author.name).message(subject=f"Hello!", message=message) #message
                        f.write(f"Sent message to redditor: {post.author.name}\n")
                        submission.reply(response.text)
                    except Exception as e:
                        f.write("Could not PM reddit, Exception: {e}\n")
                        submission.reply(response.text + "\n\n" + message) #comment response
                        
                    f.write(f"replied to post: {post.id}\n")

                else:
                    nums+=1
                    continue
                # time.sleep(20)
                
def tts(text, id):

    client = ElevenLabs(
    api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Defaults to ELEVEN_API_KEY
    )
    
    audio = client.generate(
        text=text,
        voice="xxxxx",
        model="eleven_multilingual_v2"
    )
    
    
    save(audio, f"{dir}/morgs/speech/{id}.mp3")


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--numPosts", help="how many posts for each query in each subreddit", required=False)
    args = parser.parse_args()

    main(args.numPosts)
    print("Complete")
