import discord
from discord.ext import commands
from config import Token
from imageai.Detection import ObjectDetection
# Replace with your actual bot token

intents=discord.Intents.default()
intents.message_content = True  # Enable message content intent
# Initialize bot
bot = commands.Bot(command_prefix='$', intents=intents)

# Initialize the ObjectDetection detector
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("yolov3.pt")  # Make sure you have the yolo.h5 model file in your directory
detector.loadModel()

@bot.event
async def on_ready():
    print(f' {bot.user} olarak giriş yapıldı!')
@bot.command()
async def check(ctx):
    if not ctx.message.attachments:
        await ctx.send("Lütfen bir resim yükle!")
        return

    attachment = ctx.message.attachments[0]
    await attachment.save("input.jpg")

    detections = detector.detectObjectsFromImage(
        input_image="input.jpg",
        output_image_path="output.jpg"
    )

    if detections:
        mesaj = "Bulunan nesneler:\n" + "\n".join(obj['name'] for obj in detections)
        await ctx.send(mesaj, file=discord.File("output.jpg"))
    else:
        mesaj = "Hiç nesne bulunamadı."
        await ctx.send(mesaj)

    #await ctx.send(mesaj, file=discord.File("output.jpg"))

bot.run(Token)