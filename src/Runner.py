#selenium_firefox==0.2.7 selenium==3.141.0 geckodriver 0.21.0- 0.29.1
import os

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

if __name__ == '__main__':

    print("start")
    os.system("python YoutubeShorts/youtube_uploader_selenium/upload.py --video=YoutubeShorts/videos/film.mp4 --profile=C:/Users/nicol/AppData/Roaming/Mozilla/Firefox/Profiles/suu68dnw.default-release")
    print("done")                                                                                                                  
    
    