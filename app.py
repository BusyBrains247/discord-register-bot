import asyncio
import os
import sqlite3

import discord
from discord.ext import commands
from discord.utils import get

import servers


def create_db():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS table1 (username TEXT, Ad TEXT, Soyad TEXT,Okul TEXT, Bolum TEXT, Sinif TEXT, IlgiAlani TEXT)")
    con.commit()


def add_value(data_list, username):
    cursor.execute("INSERT INTO table1 VALUES(?,?,?,?,?,?,?)",
                   (username, data_list[0], data_list[1], data_list[2], data_list[3], data_list[4], data_list[5]))
    con.commit()


def sql_execute(execute_text):
    cursor.execute(execute_text)
    con.commit()


FILENAME = "kullanici_verileri.db"
list_keys = ["Ad: ", "Soyad: ", "Okul: ", "Bölüm: ", "Sınıf: ", "İlgilendiğiniz Alan: "]

con = sqlite3.connect(FILENAME)

cursor = con.cursor()

bot = commands.Bot(command_prefix="$")
token = os.getenv("DISCORD_BOT_TOKEN")


@bot.event
async def on_ready():
    create_db()
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("github.com/nurettinselim"))
    print("I am online")


@bot.event
async def on_message(message):
    if message.author != bot.user:
        print(message)
        await bot.process_commands(message)

        channel = message.channel
        register_channel = servers.get_register_channel_id(message.guild.id)

        if channel.id == register_channel:
            datas = list()
            try:
                datas = [i.split(":")[1].strip() for i in message.content.split("\n")]
                if len(datas) != 6:
                    raise Exception
            except:
                await message.delete()

                error_message = f"{message.author.mention} Bir hata oluştu! Formu kopyala yapıştır ile kolayca doldurabilirsin \N{WINKING FACE}"
                await channel.send(error_message, delete_after=15)
                print(len(datas))
                if len(datas) == 7:
                    await channel.send(
                        "Hatayı düzeltmen için ipucu:\n Formun sonuna fazladan bir satır koymuş olabilirsin",
                        delete_after=15)
                if len(datas) == 1:
                    await channel.send(
                        "Hatayı düzeltmen için ipucu:\n İstenilen formu birebir, satır satır yazmaya dikkat edebilirsin",
                        delete_after=15)

                return

            username = f"{message.author.name}#{message.author.discriminator}"

            data_text = '\n'.join([k + v for k, v in zip(list_keys, datas)])

            confirm_message_text = f""" {data_text}
{message.author.mention} Bilgilerini onaylıyorsan 15 saniye içerisinde 👍 tepkisini verebilirsin"""

            bot_message = await channel.send(confirm_message_text, delete_after=15)

            await bot_message.add_reaction("\N{THUMBS UP SIGN}")

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '👍'

            try:
                await bot.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await channel.send('Zaman aşımına uğradı', delete_after=15)
            else:
                await bot_message.delete()
                add_value(datas, username)
                role = get(message.author.guild.roles, id=761950751223447562)
                await message.author.add_roles(role)
                await channel.send(f'{message.author.mention} Kayıt başarılı!', delete_after=15)

            await message.delete()


@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong with {str(round(bot.latency, 2))}")


@bot.command()
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=amount)


@bot.command()
@commands.has_role('Yönetici')
async def download_data(ctx):
    await ctx.author.send(file=discord.File(FILENAME))


@bot.command()
@commands.has_role('DBAdmin')
async def download_data(ctx, arg1):
    try:
        sql_execute(arg1)
    except Exception as e:
        await ctx.send(f"Hata: {e}")


bot.run(token)
