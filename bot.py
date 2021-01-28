# bot.py - trontina_project
import os
import random
import discord
import asyncio
import praw # API para conexão com o Reddit.
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime, timedelta, timezone
print ('Starting Trontina...')

# Tokens - Discord e Reddit.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
R_ID = os.getenv('R_ID')
R_SECRET = os.getenv('R_SECRET')
R_USER = os.getenv('R_USER')
reddit = praw.Reddit(client_id=R_ID, client_secret=R_SECRET, user_agent=R_USER)

# Pré-fixo que usaremos para invocar a Trontina no servidor.
bot = commands.Bot(command_prefix='$')

# Data da última mensagem da Trontina.
trontinaNextMessageAt = datetime.now()

# Status da Trontina.
@bot.event
async def on_ready():
    # watching
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="twitch.tv/tront_"))
    print ("Trontina says: Showing status as a charm!")

# Interações da Trontina.
@bot.event
async def on_message(message):
    global trontinaNextMessageAt
    now = datetime.now()

    # Não queremos que ela responda a si mesmo, certo? certo!
    if message.author == bot.user:
        if 'bom dia' in message.content.lower():
            trontinaNextMessageAt = message.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None) + timedelta(minutes=5)
        return

    # Bom dia!
    if 'bom dia' in message.content.lower():

        # Não queremos que ela se canse de responder bom dias, não é mesmo?
        if trontinaNextMessageAt.timestamp() > now.timestamp():
            return

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

    # Trontina posta fotos de comida - busca feita no Reddit usando a API praw.
    if 'fome' in message.content.lower():
        memes_submissions = reddit.subreddit('FoodPorn').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

            trontina_food = [
                'Hmmmmm :fork_and_knife: :yum: que tal?',
                'Olha :heart_eyes: o que tem pra :fork_and_knife: hoje!',
                'Pode comer se quiser, eu me alimento com bytes :blush: beep-boop',
                'Não quero te deixar com vontade :grimacing: mas'
            ]

            trontina_awf = random.choice(trontina_food)

        await message.channel.send(trontina_awf)
        await message.channel.send(submission.url)

    await bot.process_commands(message)

# Lista de ajuda com comandos úteis ($trontina).
@bot.command(pass_context=True)
async def ajuda(ctx):
    embed = discord.Embed(
        colour = discord.Colour.magenta() )
    embed.set_author(name='Oi, meu nome é Trontina! Sou a assistente pessoal do streamer que mais cresce no Brasil. Veja abaixo como posso ser útil:')
    embed.add_field(name='$links', value='Links úteis do streamer que mais cresce no Brasil', inline=False)
    embed.add_field(name='$lives', value='Informações sobre as lives do Tront', inline=False)
    embed.add_field(name='$memes', value='Memes fresquinhos para animar os seguidores', inline=False)
    embed.add_field(name='$ping', value='Informações sobre sua conexão com o servidor', inline=False)
    embed.add_field(name='$setup', value='Equipamentos do streamer da bola azul', inline=False)
    await ctx.send(embed=embed)

# Comando ($links) - mostra os links úteis.
@bot.command(name="links")
async def links(ctx):
    embed = discord.Embed(
        colour = discord.Colour.magenta() )
    embed.set_author(name='Links úteis do streamer que mais cresce no Brasil')
    embed.add_field(name='Doações', value='[streamelements.com/tront_](https://streamelements.com/tront_/tip)', inline=False)
    embed.add_field(name='Instagram', value='[instagram.com/tronttv](https://instagram.com/tronttv)', inline=False)
    embed.add_field(name='TikTok', value='[tiktok.com/@tront_](https://tiktok.com/@tront_)', inline=False)
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
    embed.add_field(name='Quando acontece?', value='De terça a domingo, a partir das 19h - Horário de Brasília', inline=False)
    await ctx.send(embed=embed)

# Comando ($setup) - lista o setup do streamer da bola azul.
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

# Comando ($ping) - trontina responde com seu ping, se você perguntar.
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong  :sunglasses:  {round (bot.latency * 1000)}ms ')

# Comando ($memes) - trontina busca memes no reddit usando a API praw.
@bot.command(name='memes')
async def memes(ctx):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await ctx.send(submission.url)

# Mensagem de retorno em caso de erros.
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'Deu ruim :exploding_head: né? Para saber as palavras mágicas, digite: $ajuda | ({error})')

# Em execução.
print ('Trontina says: Bom dia!')
bot.run(TOKEN)
