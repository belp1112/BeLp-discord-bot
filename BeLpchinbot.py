from asyncio import TimeoutError
from os import getenv

import discord
from requests import get
from unicodedata import name
from riot import return_collect_champion_name, retrieve_championdata, return_skinlist, shape_to_discordmsg

TOKEN = getenv('BeLChinBotTOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print('Bot is online')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if not message.content.startswith('!lol'):
        return

    #sender_id = message.author.id
    #channel_id = message.channel.id
    message_split = message.content.split( )
    #エラー処理 チャンピオン名を入力しなかった場合
    if len(message_split) < 2:
        await message.reply('チャンピオン名を入力してください')
        return

    if message_split[1] == 'patch':
        patch_ver = list(get('https://ddragon.leagueoflegends.com/api/versions.json').json())[0]
        await message.reply(patch_ver)
    else:
        champion_name = message_split[1]
        language = language_judge(champion_name)
        if language == 'en_US':
            champion_name = champion_name.capitalize()
        id_champion_name = return_collect_champion_name(language,champion_name)
        champion_data = retrieve_championdata(id_champion_name, language)
        if type(champion_data) is not dict:
            await message.reply(champion_data)
            return
        else:
            skin_list = return_skinlist(champion_data, id_champion_name)
            shaped_skinlist = shape_to_discordmsg(skin_list)
            await message.reply(shaped_skinlist)

        def check(m) -> bool:
            return True

        try:
            msg = await client.wait_for('message', check=check, timeout=90)
            nums = msg.content.split(' ')
            skin_num = []
            for i in nums:
                skin_num.append(skin_list[int(i) - 1]['num'])
            skin_num_list = []
            for i in skin_num:
                skin_num_list.append(
                "http://ddragon.leagueoflegends.com"
                f"/cdn/img/champion/splash/{id_champion_name}_{i}.jpg"
                )
            for i in skin_num_list:
                await msg.reply(i)
        except TimeoutError:
            await message.reply("キャンセルされました")
        return


def language_judge(champion_name):
    '''文字の最初の一文字を判定して言語名を返す'''
    jadged_language = name(champion_name[0]).split(' ')
    if jadged_language[0] == 'LATIN':
        return 'en_US'
    elif jadged_language[0] == 'KATAKANA':
        return 'ja_JP'
    elif jadged_language[0] == 'HANGUL':
        return 'ko_KR'


client.run(TOKEN)
