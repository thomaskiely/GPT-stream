import os
from dotenv import load_dotenv
import irc.bot
import pygame
from openai import OpenAI
load_dotenv()


class TwitchChatBot(irc.bot.SingleServerIRCBot):
  def __init__(self, username, token, channel):
    self.token = token
    self.channel = channel
    server = 'irc.chat.twitch.tv'
    port = 6667
    self.client = OpenAI()
    irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    print("call inital open ai")
    
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    game = os.getenv('GAME')

    gpt_promt =  "you are an ai virtual assistant named Onyx for mrtommy's stream, he is playing " + game + "give the viewers some tips" \
                  "Refer to the viwers as chat"

    completion = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": gpt_promt},
        {"role": "user", "content": "Who are you?"}
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
      # output text to speech here
      print(completion.choices[0].message.content)
      self.drawSam()

  def drawSam(self):
     #print("Draw Samantha")
      #FIX THIS
     """  screen = pygame.display.set_mode((800, 800))
      talkingSam = pygame.image.load('samTalking.png')
      notTalkingSam = pygame.image.load('samNotTalking.png')
      screen.blit(talkingSam,(200,200))
      pygame.display.update()
      pygame.event.pump() """
    




if __name__ == "__main__":
  TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')
  TWITCH_CLIENT_ID= os.getenv('TWITCH_CLIENT_ID')
  TWITCH_USERNAME= os.getenv('TWITCH_USERNAME')
  CHANNEL = '#' + TWITCH_USERNAME
  pygame.init()
  bot = TwitchChatBot(TWITCH_USERNAME, TWITCH_TOKEN, CHANNEL)
  bot.start()