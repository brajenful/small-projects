import sys
import os
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

import textwrap
import json

class MemeGenerator:

	def __init__(self, bot):
		self.bot = bot

		self.config_path = '/resources/meme_generator/templates.json' #This is the path for the config file
		with open(self.config_path, 'r') as file:
			self.config = json.loads(file.read())

		self.template_folder = self.config['template_folder']
		self.fonts_folder = self.config['fonts_folder']
		self.output_folder = self.config['output_folder']

	def get_template_info(self, template):
		template = self.config['templates'][template]

		self.font = ImageFont.truetype(f"{self.fonts_folder}/{template['font']}", size=template['font_size'])
		self.image = Image.open(f"{self.template_folder}/{template['template_file']}").convert('RGB')
		self.draw = ImageDraw.Draw(self.image)

		self.output_path = f"{self.output_folder}/{template['output_subfolder']}"

		self.coordinates = template['coordinates']
		self.panel_count = template['panel_count']
		self.panel_width = template['panel_width']
		self.offset = template['offset']
	async def generate_meme(self, ctx, text):

		panels = text.split(',')[:self.panel_count]
		
		for k, text in enumerate(panels):
			text = text.strip(' ')
			wrapped = textwrap.wrap(text, width=self.panel_width)
			offset = 0
			for text in wrapped:
				self.draw.text((self.coordinates[k][0], self.coordinates[k][1]+offset), text, fill=(0, 0, 0), font=self.font)
				offset += self.offset

		output_path = f'{self.output_path}/{ctx.message.author.name}_{ctx.message.id}.jpg'
		self.image.save(output_path) #If you don't want to save the image locally, comment this line out.

		with open(output_path, 'rb') as file:
			await ctx.send(file=discord.File(file))

	@commands.command(brief='Creates an expanding brain meme.')
	async def brain(self, ctx, *, text):
		self.get_template_info('expanding_brain') #This is the line that tells the code which template to use. 
							  #Just change its parameter to the name of the template you want to use, and that should do it.
		await self.generate_meme(ctx, text)

def setup(bot):
	bot.add_cog(MemeGenerator(bot))
