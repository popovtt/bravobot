import sqlite3
from telethon import TelegramClient, events
from config import *

client = TelegramClient('session_name3', API_ID, API_HASH)
client.start()

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS article (
                    article_id TEXT PRIMARY KEY,
                    url TEXT
                )''')


@client.on(events.NewMessage(pattern=r'/start'))
async def handler(event):
    await event.respond("Hello World EBAL NAHUI IVASIUK")

@client.on(events.NewMessage(pattern=r'/find', from_users=WHITELIST))
async def handler(event):
    parts = event.raw_text.split()
    cursor.execute("SELECT url FROM article WHERE article_id = ?", (parts[1], ))
    result = cursor.fetchone()
    await event.respond(result[0])

@client.on(events.NewMessage(pattern=r'/add', from_users=WHITELIST))
async def handler(event):
    parts = event.raw_text.split()
    cursor.execute("INSERT OR REPLACE INTO article (article_id, url) VALUES (?, ?)", (parts[1],parts[2]))
    connection.commit()
    await event.respond(f"Added {parts[1]} successfully")  

@client.on(events.NewMessage(pattern=r'/remove', from_users=WHITELIST))
async def handler(event):
    parts = event.raw_text.split()
    cursor.execute("DELETE FROM article WHERE article_id = ?", (parts[1], ))
    connection.commit()
    await event.respond(f"Removed {parts[1]} successfully")

@client.on(events.NewMessage(pattern=r'/list', from_users=WHITELIST))
async def handler(event):
    cursor.execute("SELECT * FROM article")
    result = cursor.fetchall()
    txt=''
    for article_id, url in result:
        txt+=f"{article_id} - {url}\n"
    await event.respond("Articles: - URLs:\n" + txt)

client.run_until_disconnected()