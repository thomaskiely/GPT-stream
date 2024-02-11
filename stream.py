import os
from dotenv import load_dotenv
import irc.bot
import pygame
from openai import OpenAI
from pathlib import Path
from pygame import mixer
import random
import time
load_dotenv()


class TwitchChatBot(irc.bot.SingleServerIRCBot):
  def __init__(self, username, token, channel):
    self.token = token
    self.channel = channel
    server = 'irc.chat.twitch.tv'
    port = 6667
    self.client = OpenAI()
    irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    mixer.init()
    pygame.init()
    display_width = 800
    display_height = 800

    self.game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Onyx')

    self.talking_img = pygame.image.load('onyxTalking.png')
    self.waiting_img = pygame.image.load('onyxNotTalking.png')

    self.drawOnyx(self.game_display, self.waiting_img, 0, 0)
    pygame.event.pump()
    
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    game = os.getenv('GAME')

    gpt_promt =  "you are an ai virtual assistant named Onyx for mrtommy's stream, he is playing " + game + "give the viewers some tips" \
                  "Refer to the viwers as chat" \
                  "keep your responses to 2 sentences or less"

    completion = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": gpt_promt}
    ],
    max_tokens=100
  )

    print(completion.choices[0].message.content)



 
  def on_welcome(self, connection, event):
       
        connection.join(self.channel)
        print("joined channel" + self.channel)



  def on_pubmsg(self, connection, event):
        try:
            if event.target == self.channel:
                username = event.source.split('!')[0]
                message = event.arguments[0]
                print(f'{username}: {message}')
                self.callOpenAI(username, message)
        except Exception as e:
            print("Error in on_pubmsg:", e)



  def callOpenAI(self, username, message):
      completion = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": username + "says " + message}
    ],
    max_tokens=100
  )
      onyxResponse = completion.choices[0].message.content
      self.textToSpeech(onyxResponse)
      print(onyxResponse)


  def textToSpeech(self, onyxResponse):
      speech_file_path = Path(__file__).parent / "speech.mp3"
      response = self.client.audio.speech.create(
      model="tts-1",
      voice="onyx",
      input= onyxResponse
    )
      response.stream_to_file(speech_file_path)
      self.moveOnyx(speech_file_path)


  
  def moveOnyx(self, onyxSpeech):
      mixer.music.load(onyxSpeech)
      mixer.music.play()
      while mixer.music.get_busy():
          pygame.event.pump()
          self.drawOnyx(self.game_display, self.talking_img, random.randint(0,10), random.randint(0,10))
          time.sleep(.08)
      self.drawOnyx(self.game_display, self.waiting_img,0,0)
      mixer.music.unload()

  def drawOnyx(self, game_display, image, x, y):
      pink = (255, 0, 255)
      game_display.fill(pink)
      game_display.blit(image, (x, y))
      pygame.display.update()
    




if __name__ == "__main__":
  TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')
  TWITCH_CLIENT_ID= os.getenv('TWITCH_CLIENT_ID')
  TWITCH_USERNAME= os.getenv('TWITCH_USERNAME')
  CHANNEL = '#' + TWITCH_USERNAME
  pygame.init()
  bot = TwitchChatBot(TWITCH_USERNAME, TWITCH_TOKEN, CHANNEL)
  bot.start()