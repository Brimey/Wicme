import discord


def create_conn():
    conn = discord.Client(intents=discord.Intents.default())
    return conn
