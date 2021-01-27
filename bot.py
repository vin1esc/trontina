# bot.py - trontina_project
import os
import random
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
print ('Starting Trontina...')

# Token privado que faz ligação com o Discord.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Pré-fixo que usaremos para invocar a Trontina no servidor.
bot = commands.Bot(command_prefix='$')

# Status da Trontina.
@bot.event
async def on_ready():
    # watching
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="twitch.tv/tront_"))
    print ("Trontina says: Showing status as a charm!")

# Interações da Trontina.
@bot.event
async def on_message(message):

    # Não queremos que ela responda a si messmo, certo? certo!
    if message.author == bot.user:
        return

    # Bom dia!
    if 'bom dia?' in message.content.lower():
        await message.reply('Bom dia :sun_with_face: ', mention_author=True)

    # Mensagens pré-programadas.
    trontina_quotes = [
        'Ouvi meu nome :face_with_monocle: neste canal? Saiba mais digitando $ajuda',
        'Bom dia :sun_with_face: Precisa de uma mãozinha? É só digitar $ajuda'
    ]

    if 'trontina' in message.content.lower():
        response = random.choice(trontina_quotes)
        await message.channel.send(response)

    # Easteregg - com amor, Vini.
    if 'sasha' in message.content.lower():
        emoji = '\N{EYES}'
        await message.add_reaction(emoji)

    await bot.process_commands(message)

# Lista de ajuda com comandos úteis ($trontina).
@bot.command(pass_context=True)
async def ajuda(ctx):
    embed = discord.Embed(
        colour = discord.Colour.magenta() )
    embed.set_author(name='Oi, meu nome é Trontina! Sou a assistente pessoal do streamer que mais cresce no Brasil. Veja abaixo como posso te ajudar:')
    embed.add_field(name='$links', value='Links úteis do streamer que mais cresce no Brasil', inline=False)
    embed.add_field(name='$lives', value='Informações sobre as lives do Tront', inline=False)
    embed.add_field(name='$ping', value='Informações sobre sua conexão com o servidor', inline=False)
    embed.add_field(name='$setup', value='Setup do streamer da bola azul', inline=False)
    await ctx.send(embed=embed)

# Comando ($links) - mostra os links úteis.
@bot.command(name="links")
async def links(ctx):
    embed = discord.Embed(
        colour = discord.Colour.magenta() )
    embed.set_author(name='Links úteis do streamer que mais cresce no Brasil')
    embed.add_field(name='Doações', value='[streamelements.com/tront_](https://streamelements.com/tront_/tip)', inline=False)
    embed.add_field(name='Instagram', value='[instagram.com/tronttv](https://instagram.com/tronttv)', inline=False)
    embed.add_field(name='Twitch', value='[twitch.tv/tront_](https://www.twitch.tv/tront_/)', inline=False)
    embed.add_field(name='Twitter', value='[twitter.com/vitortront](https://twitter.com/vitortront)', inline=False)
    embed.add_field(name='Youtube', value='[youtube.com/tront_](https://youtube.com/tront_)', inline=False)
    await ctx.send(embed=embed)

# Comando ($lives) - mostra informações sobre as lives do Tront.
@bot.command(name="lives")
async def lives(ctx):
    embed = discord.Embed(
        colour = discord.Colour.magenta() )
    embed.set_author(name='Informações da livestream que mais cresce no Brasil')
    embed.add_field(name='Onde acontece?', value='Ao vivo na [twitch.tv/tront_](https://www.twitch.tv/tront_/)', inline=False)
    embed.add_field(name='Quando acontece?', value='De terça a sexta, às 19h - Horário de Brasília', inline=False)
    await ctx.send(embed=embed)

# Comando ($tront) - mostra algumas curiosidades.
@bot.command(name="setup")
async def setup(ctx):
    embed = discord.Embed(
        colour = discord.Colour.magenta() )
    embed.set_author(name='Setup do streamer da bola azul')
    embed.add_field(name='CPU', value='Intel Core i7 7700K 4.2GHz', inline=False)
    embed.add_field(name='Placa de vídeo', value='EVGA NVIDIA GeForce GTX 1070 Ti SC Gaming 8GB', inline=False)
    embed.add_field(name='Memória RAM', value='HyperX FURY 8GB 2400Mhz (4x)', inline=False)
    embed.add_field(name='Fonte', value='Corsair 550W 80 Plus White VS550', inline=False)
    embed.add_field(name='Gabinete', value='Aerocool Cylon', inline=False)
    embed.add_field(name='Volante', value='Logitech G29', inline=False)
    embed.add_field(name='Controle', value='Dualshock 4', inline=False)
    embed.add_field(name='Teclado', value='Redragon Kala Rgb Abnt2 Switch Blue', inline=False)
    embed.add_field(name='Mouse', value='Logitech Hero G Series G502', inline=False)

    await ctx.send(embed=embed)

# Remove do comando padrão de ajuda (pois criamos uma lista de ajuda personalizada, acima).
bot.remove_command('help')

# Trontina responde com seu ping, se você perguntar.
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong  :sunglasses:  {round (bot.latency * 1000)}ms ')

# Mensagem de retorno em caso de erros.
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'Deu ruim :exploding_head: né? Para saber as palavras mágicas, digite: $ajuda | ({error})')

# Em execução.
print ('Trontina says: Bom dia!')
bot.run(TOKEN)
