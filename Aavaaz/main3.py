import gtts
import playsound

text=input("Enter something here : ")
sound=gtts.gTTS(text,lang='en')
sound.save("tp.mp3")
playsound.playsound("tp.mp3")
