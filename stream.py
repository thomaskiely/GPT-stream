import os
from dotenv import load_dotenv
import irc.bot
import pygame
load_dotenv()


class TwitchChatBot(irc.bot.SingleServerIRCBot):
  def __init__(self, username, token, channel):
    self.token = token
    self.channel = channel
    server = 'irc.chat.twitch.tv'
    port = 6667
    irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

 
  def on_welcome(self, connection, event):
       
        connection.join(self.channel)
        print("joined channel" + self.channel)



  def on_pubmsg(self, connection, event):
        try:
            if event.target == self.channel:
                username = event.source.split('!')[0]
                message = event.arguments[0]
                print(f'{username}: {message}')
                self.callOpenAI()
        except Exception as e:
            print("Error in on_pubmsg:", e)

  def callOpenAI(self):
      print("TODO: call OPEN AI with message")
      self.drawSam()

  def drawSam(self):
     
      #FIX THIS
      screen = pygame.display.set_mode((800, 800))
      talkingSam = pygame.image.load('samTalking.png')
      notTalkingSam = pygame.image.load('samNotTalking.png')
      screen.blit(talkingSam,(200,200))
      pygame.display.update()
      pygame.event.pump()
      print("Draw Samantha")




if __name__ == "__main__":
  TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')
  TWITCH_CLIENT_ID= os.getenv('TWITCH_CLIENT_ID')
  TWITCH_USERNAME= os.getenv('TWITCH_USERNAME')
  CHANNEL = '#' + TWITCH_USERNAME
  pygame.init()
  bot = TwitchChatBot(TWITCH_USERNAME, TWITCH_TOKEN, CHANNEL)
  bot.start()