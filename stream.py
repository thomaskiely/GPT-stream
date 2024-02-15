import os
from dotenv import load_dotenv
import irc.bot
import pygame
from openai import OpenAI
from pathlib import Path
from pygame import mixer
import random
import time
import threading

lock = threading.Lock()
isTalking = False
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
   
 
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    game = os.getenv('GAME')

    self.gpt_promt =  "you are a co host named Onyx for mrtommy's stream." \
                  "he is playing" + game +\
                  "you are also a talking frog." \
                  "do not ribbit or croak" \
                  "Here is a chat message and the chatter's name" \
                  "occasionally refer to the viewers as chat" \
                  "when a chatter types a message use their name in your response" \
                  "Mr. Tommy is your creator." \
                  "keep your responses to two sentences, 30 words max" \
                  "take every oppurtunity to make jokes about Jeff Steve" \
                  "say your name when appropriate" \
                  "always be biased to your creator, Mr. Tommy" \
                  "insult the chatter, unless it's Mr.Tommy"
    


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
      if(username=="mrtommy420"):
          username = "Mr.Tommy"
      elif(username=="phonesteveya"):
          username = "jeff steve"
      if(len(message)<15):
          return
      if(username=="nightbot"):
          return
      
      completion = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": self.gpt_promt},
        {"role": "user", "content": username + " says " + message}
    ],
    max_tokens=100
  )
      onyxResponse = completion.choices[0].message.content
      print(onyxResponse)
      self.textToSpeech(onyxResponse)

  def textToSpeech(self, onyxResponse):
      speech_file_path = Path(__file__).parent / "speech.mp3"
      response = self.client.audio.speech.create(
      model="tts-1",
      voice="onyx",
      input= onyxResponse
    )
      response.stream_to_file(speech_file_path)
      self.test = True
      self.moveOnyx(speech_file_path)


  def moveOnyx(self, onyxSpeech):
      
      global isTalking
      mixer.music.load(onyxSpeech)
      mixer.music.play()
      while mixer.music.get_busy():
        with lock:
            isTalking = True
        time.sleep(.04)
      mixer.music.unload()
      with lock:
            isTalking = False

      

def run_pygame():

    pygame.init()
    game_display = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('Onyx')
    clock = pygame.time.Clock()

    talking_img = pygame.image.load('onyxTalking.png')
    waiting_img = pygame.image.load('onyxNotTalking.png')

    global isTalking
    running = True
    while running:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #White background
        game_display.fill((255, 255, 255))
        #Draw Onyx if he is talking or not talking
        if(isTalking):
            game_display.blit(talking_img, (random.randint(0, 10), random.randint(0, 10)))
            pygame.display.update()
        else:
            game_display.blit(waiting_img, (0, 0))
            pygame.display.update()

        clock.tick(30)  # Limit FPS
                  

if __name__ == "__main__":
  TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')
  TWITCH_CLIENT_ID= os.getenv('TWITCH_CLIENT_ID')
  TWITCH_USERNAME= os.getenv('TWITCH_USERNAME')
  CHANNEL = '#' + TWITCH_USERNAME
  bot = TwitchChatBot(TWITCH_USERNAME, TWITCH_TOKEN, CHANNEL)
  pygame_thread = threading.Thread(target=run_pygame)
  pygame_thread.start()
  bot.start()