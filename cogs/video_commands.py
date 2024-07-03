import discord
from discord.ext import commands
from moviepy.editor import VideoFileClip
from PIL import Image
import io
import os
import logging
from utils.image_utils import save_attachment, cleanup_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gifitize(self, ctx):
        try:
            video_attachment = None

            # Check if the command is replying to a message
            if ctx.message.reference:
                try:
                    replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
                    if replied_message.attachments:
                        video_attachment = replied_message.attachments[0]
                except discord.NotFound:
                    logger.error("Referenced message not found.")
                except Exception as e:
                    logger.error(f"Error fetching referenced message: {str(e)}")
            
            # If no video in reply, check the command message itself
            if not video_attachment and ctx.message.attachments:
                video_attachment = ctx.message.attachments[0]

            # If still no video, search for the last video in the channel
            if not video_attachment:
                async for message in ctx.channel.history(limit=100):
                    if message.attachments:
                        for attachment in message.attachments:
                            if attachment.filename.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
                                video_attachment = attachment
                                break
                    if video_attachment:
                        break

            if not video_attachment:
                await ctx.send("No video found in recent messages. Please attach a video, reply to a message with a video, or ensure there's a video in recent chat history.")
                return

            if not video_attachment.filename.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
                await ctx.send("Please provide a valid video file.")
                return


            file_path = await save_attachment(video_attachment)

            video = VideoFileClip(file_path)
            if video.duration > 20:
                video = video.subclip(0, 20)

            # Set the frame rate to 10 fps
            video = video.set_fps(10)

            frames = []
            for frame in video.iter_frames():
                img = Image.fromarray(frame)
                frames.append(img)

            output = io.BytesIO()
            # Set duration to 100 ms per frame (10 fps)
            frames[0].save(output, format='GIF', save_all=True, append_images=frames[1:], loop=0, duration=100)
            output.seek(0)

            await ctx.send(file=discord.File(output, filename='converted.gif'))

        except Exception as e:
            logger.error(f"Error in convert_to_gif: {str(e)}")
            await ctx.send(f"An error occurred while processing the video: {str(e)}")
        
        finally:
            if 'video' in locals():
                video.close()
            if 'file_path' in locals():
                await cleanup_file(file_path)

async def setup(bot):
    await bot.add_cog(VideoCommands(bot))