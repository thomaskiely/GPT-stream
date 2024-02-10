from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import readChat

def main():
    

  load_dotenv()

  client = OpenAI()

  #speech_file_path = Path(__file__).parent / "speech.mp3"
  """ response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input="Today is a wonderful day to build something people love!"
  )

  response.with_streaming_response.method("output.mp3") """


  print("hello")
  readChat.readTwitchChat() 


if __name__ == "__main__":
  main()