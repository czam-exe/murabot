import discord
import random
from datetime import datetime
from store import load, reset
from config import FINE_PER_SWEAR

BIBLE_VERSES = [
    ('"Ang mabuting tao ay nagsasalita ng mabuti."', 'Mateo 12:35'),
    ('"Ang dila ay maliit na bahagi ng katawan, ngunit napakalaki ng magagawa nito."', 'Santiago 3:5'),
    ('"Huwag lumabas sa inyong bibig ang anumang masamang salita."', 'Efeso 4:29'),
    ('"Ang maingat sa salita ay maingat din sa buong buhay."', 'Santiago 3:2'),
    ('"Ang mga salitang inyong sinasabi ay magpapakita kung ano kayo."', 'Mateo 12:37'),
    ('"Ang puso ng matuwid ay nag-iisip bago magsalita."', 'Kawikaan 15:28'),
    ('"Ang malambot na sagot ay nagpapatahimik ng galit."', 'Kawikaan 15:1'),
    ('"Ang Panginoon ay nagmamahal sa mga taong matuwid ang puso at dila."', 'Kawikaan 22:11'),
    ('"Ang bawat salita mo ay dapat magbigay ng buhay, hindi kamatayan."', 'Kawikaan 18:21'),
    ('"Magingat sa inyong mga salita, sapagkat kayo ay susukatin sa mga ito."', 'Mateo 12:36'),
]

async def post_leaderboard(bot, channel):
    data = load()
    if not data:
        await channel.send("No data recorded today.")
        reset()
        return

    swearers = {uid: v for uid, v in data.items() if v["daily_count"] > 0}
    saints = [v for v in data.values() if v["sent_message_today"] and v["daily_count"] == 0]
    total_today = sum(v["daily_count"] for v in data.values())
    today_str = datetime.now().strftime("%B %d, %Y")

    # Bible verse
    verse, reference = random.choice(BIBLE_VERSES)
    verse_embed = discord.Embed(description=f"*{verse}*\n— **{reference}**", color=discord.Color.blurple())
    await channel.send(embed=verse_embed)

    await channel.send(f"**Mura Daily Leaderboard — {today_str}**\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Hall of Shame — one embed per swearer with profile pic
    if swearers:
        await channel.send("**HALL OF SHAME**")
        for i, (uid, v) in enumerate(sorted(swearers.items(), key=lambda x: -x[1]["daily_count"]), 1):
            top = max(v["daily_words"], key=v["daily_words"].get)
            fine = v["daily_count"] * FINE_PER_SWEAR
            shame_embed = discord.Embed(title=f"#{i} — Pinaka gago ngayong araw" if i == 1 else f"#{i}", color=discord.Color.red())
            shame_embed.set_thumbnail(url=v["avatar_url"])
            shame_embed.add_field(name="User", value=v["username"], inline=True)
            shame_embed.add_field(name="Swears", value=str(v["daily_count"]), inline=True)
            shame_embed.add_field(name="Most Used", value=f"`{top}`", inline=True)
            shame_embed.add_field(name="Owes Jar", value=f"PHP {fine}", inline=True)
            await channel.send(embed=shame_embed)
    else:
        await channel.send("Nabuhusan ng holy water ang lahat.")

    await channel.send("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Saints
    saint_names = ", ".join(s["username"] for s in saints) or "Wala"
    saint_embed = discord.Embed(title="Saints of the Day", description=saint_names, color=discord.Color.green())
    await channel.send(embed=saint_embed)

    # Foulness Index
    yesterday = getattr(post_leaderboard, "_yesterday_total", None)
    if yesterday is None:
        trend = "Binasag na nya ang sumpa."
    elif total_today > yesterday:
        trend = f"Mas masahol ngayon ({yesterday} -> {total_today})"
    elif total_today < yesterday:
        trend = f"Mas masahol kahapon ({yesterday} -> {total_today})"
    else:
        trend = f"Tamang timpla ({total_today})"
    post_leaderboard._yesterday_total = total_today

    index_embed = discord.Embed(title="Server Foulness Index", description=trend, color=discord.Color.orange())
    await channel.send(embed=index_embed)
    await channel.send("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    reset()
