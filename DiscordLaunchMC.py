# EN: This file is DiscordLaunchMC (Japanese version). If you want to use English, please use DiscordLaunchMC-en.
# JP: このファイルはDiscordLaunchMC（日本語版）です。英語を使用したい場合は、DiscordLaunchMC-enを使用してください。
# DiscordLaunchMC-en: https://github.com/insane-catt/DiscordLaunchMC-en

#以前ここにあった設定欄はconfig.pyに移動しました。
from config import *


# 以下はコードです。必要に応じていじってください

import discord
from discord import app_commands
import subprocess
import sys
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


#翻訳
from languages import dictionary
def tr(text):
    if LANG == "jp":
        return text
    else:
        return dictionary[LANG][text]



#コマンド群 ------------------------------------------------------


#helloコマンド
@tree.command(name="hello", description="Hello, world!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(tr("こんにちは、") + interaction.user.name + tr("さん！"))


#サーバー起動
@tree.command(name="start", description=tr("サーバーを起動する"))
@app_commands.default_permissions(administrator=True)
async def start(interaction: discord.Interaction):
    if is_server_running():
        embed = discord.Embed(
            description=tr("サーバーは既に起動しています")
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        start_server()
        embed = discord.Embed(
            title=tr("サーバーを起動します"),
            color=0x00ff00,
            description=tr("しばらくおまちください。")
            )
        await interaction.response.send_message(embed=embed)


#シード値設定
@tree.command(name="setseed", description=tr("ワールドのシード値を設定する。seed引数を設定せずに実行できます。"))
@app_commands.default_permissions(administrator=True)
@app_commands.describe(seed=tr('シード値'))
async def setseed(interaction: discord.Interaction, seed: str = None):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        search_text = "level-seed="
        replace_text = f"level-seed={seed}"
        if seed == None:
            replace_text = "level-seed="

        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'w') as file:
            for line in lines:
                if search_text in line:
                    line = replace_text + '\n'
                file.write(line)

        if seed == None:
            embed = discord.Embed(
                title=tr("シード値を変更しました"),
                color=0x00ff00,
                description=tr("シード値が設定されていないので、世界はランダムに生成されます。")
                )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title=tr("シード値を変更しました"),
                color=0x00ff00,
                description=tr("新しいシード値: ") + f"`{seed}`"
                )
            await interaction.response.send_message(embed=embed)


#最大プレイヤー数
@tree.command(name="setmaxplayers", description=tr("最大プレイヤー数を変更する"))
@app_commands.default_permissions(administrator=True)
@app_commands.describe(maxplayers=tr('最大プレイヤー数'))
async def setmaxplayers(interaction: discord.Interaction, maxplayers: int):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        search_text = "max-players="
        replace_text = f"max-players={maxplayers}"

        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'w') as file:
            for line in lines:
                if search_text in line:
                    line = replace_text + '\n'
                file.write(line)
        embed = discord.Embed(
            title=tr("最大プレイヤー数を変更しました"),
            color=0x00ff00,
            description=tr("新しい最大プレイヤー数: ") + f"`{maxplayers}`"
            )
        await interaction.response.send_message(embed=embed)


#PVP設定
@tree.command(name="setpvp", description=tr("PVPの設定を変更する"))
@app_commands.default_permissions(administrator=True)
@app_commands.describe(on_or_off=tr("オンかオフか"))
@app_commands.choices(
    on_or_off=[
        discord.app_commands.Choice(name=tr("オン"),value="true"),
        discord.app_commands.Choice(name=tr("オフ"),value="false")
    ]
)
async def setpvp(interaction: discord.Interaction, on_or_off: str):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        search_text = "pvp="
        replace_text = f"pvp={on_or_off}"
        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'w') as file:
            for line in lines:
                if search_text in line:
                    line = replace_text + '\n'
                file.write(line)

        if on_or_off == "true":
            on_or_off = tr("オン")
        else:
            on_or_off = tr("オフ")

        embed = discord.Embed(
            title=tr("PVPの設定を変更しました"),
            color=0x00ff00,
            description=tr("新しいPVPの設定: ") + f"**{on_or_off}**"
            )
        await interaction.response.send_message(embed=embed)


#hardcore設定
@tree.command(name="sethardcore", description=tr("ハードコアの設定を変更する"))
@app_commands.default_permissions(administrator=True)
@app_commands.describe(on_or_off=tr("オンかオフか"))
@app_commands.choices(
    on_or_off=[
        discord.app_commands.Choice(name=tr("オン"),value="true"),
        discord.app_commands.Choice(name=tr("オフ"),value="false")
    ]
)
async def sethardcore(interaction: discord.Interaction, on_or_off: str):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        search_text = "hardcore="
        replace_text = f"hardcore={on_or_off}"
        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'w') as file:
            for line in lines:
                if search_text in line:
                    line = replace_text + '\n'
                file.write(line)

        if on_or_off == "true":
            on_or_off = tr("オン")
        else:
            on_or_off = tr("オフ")

        embed = discord.Embed(
            title=tr("ハードコアの設定を変更しました"),
            color=0x00ff00,
            description=tr("新しいハードコアの設定: ") + f"**{on_or_off}**"
            )
        await interaction.response.send_message(embed=embed)


#ゲーム難易度設定
@tree.command(name="setdifficulty", description=tr("ゲーム難易度を変更する"))
@app_commands.default_permissions(administrator=True)
@app_commands.describe(difficulty=tr("ゲーム難易度"))
@app_commands.choices(
    difficulty=[
        discord.app_commands.Choice(name=tr("ピースフル"),value="peaceful"),
        discord.app_commands.Choice(name=tr("イージー"),value="easy"),
        discord.app_commands.Choice(name=tr("ノーマル"),value="normal"),
        discord.app_commands.Choice(name=tr("ハード"),value="hard")
    ]
)
async def setdifficulty(interaction: discord.Interaction, difficulty: str):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        search_text = "difficulty="
        replace_text = f"difficulty={difficulty}"
        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'w') as file:
            for line in lines:
                if search_text in line:
                    line = replace_text + '\n'
                file.write(line)
        if difficulty == "peaceful":
            difficulty = tr("ピースフル")
        elif difficulty == "easy":
            difficulty = tr("イージー")
        elif difficulty == "normal":
            difficulty = tr("ノーマル")
        else:
            difficulty = tr("ハード")
        embed = discord.Embed(
            title=tr("ゲーム難易度を変更しました"),
            color=0x00ff00,
            description=tr("新しいゲーム難易度: ") + f"**{difficulty}**"
            )
        await interaction.response.send_message(embed=embed)
        

#ワールド名指定
@tree.command(
        name="changeworld", 
        description=tr("遊ぶワールドを変更する。存在しないワールド名を入力することで、新しいワールドが生成される。")
        )
@app_commands.default_permissions(administrator=True)
@app_commands.describe(world=tr('ワールド名'))
async def changeworld(interaction: discord.Interaction, world: str):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        search_text = "level-name="
        replace_text = f"level-name={world}"

        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'w') as file:
            for line in lines:
                if search_text in line:
                    line = replace_text + '\n'
                file.write(line)
        embed = discord.Embed(
            title=tr("遊ぶワールドを変更しました"),
            color=0x00ff00,
            description=tr("次のワールドが読み込まれます: ") + f"`{world}`"
            )
        await interaction.response.send_message(embed=embed)


@tree.command(name="setdirectly", description=tr("server.propertiesを直接編集する。※間違えないように慎重に使ってください！"))
@app_commands.default_permissions(administrator=True)
@app_commands.describe(property_name=tr("プロパティ名"))
async def setdirectly(interaction: discord.Interaction, property_name: str):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        search_text = f"{property_name}="
        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        property_found = False
        for line in lines:
            if search_text in line:
                property_found = True
                break

        if not property_found:
            await interaction.response.send_message((tr("次に一致する設定が見つかりませんでした:\n") + f"`{property_name}`"), ephemeral=True)
            return

        await interaction.response.send_message((tr("一致する設定が見つかりました:\n") + f"`{property_name}`\n" + tr("`=`に続く設定したい値を入力してください。")), ephemeral=True)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await client.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await interaction.followup.send(tr("時間切れです。もう一度やり直してください。"), ephemeral=True)
            return
        
        new_value = msg.content.strip()
        
        replace_text = f"{property_name}={new_value}"

        with open(f"{HOME_DIRECTORY}/{SERVER_PATH}/server.properties", 'w') as file:
            for line in lines:
                if search_text in line:
                    line = replace_text + '\n'
                file.write(line)

        embed = discord.Embed(
            title=tr("設定を変更しました"),
            color=0x00ff00,
            description=tr("設定を以下のように編集しました。\n") + f"```\n{replace_text}\n```"
        )
        await interaction.followup.send(embed=embed)


#botの停止
@tree.command(name="logout", description=tr("このbotをログアウトさせる"))
@app_commands.default_permissions(administrator=True)
async def exitbot(interaction: discord.Interaction):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        embed = discord.Embed(
            title=tr("ログアウトします"),
            description=tr("botは停止されます。")
            )
        await interaction.response.send_message(embed=embed)
        print("The logout command has been executed.")
        sys.exit()


#コマンド群ここまで ------------------------------------------------------


def is_server_running():
    process = subprocess.Popen(f"screen -ls {SCREEN_NAME}", stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    return SCREEN_NAME in output.decode()

def server_is_running():
    embed = discord.Embed(
        title=tr("エラー：サーバーが起動中です"),
        color=0xff0000,
        description=tr("そのコマンドを実行するには、サーバーを終了してください。")
        )
    return embed

def start_server():
    subprocess.Popen(f"screen -dmS {SCREEN_NAME} java -Xmx{MAX_RAM}G -Xms{MIN_RAM}G -jar {JAR_FILE} nogui", shell=True)


@client.event
async def on_ready():
        await client.change_presence(activity=discord.Game(name="Minecraft"))
        await tree.sync()
        print("login complete")

client.run(TOKEN)