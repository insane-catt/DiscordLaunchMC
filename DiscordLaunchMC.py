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

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


#コマンド群 ------------------------------------------------------


#helloコマンド
@tree.command(name="hello", description="Hello, world!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}!')


#サーバー起動
@tree.command(name="start", description="サーバーを起動する")
@app_commands.default_permissions(administrator=True)
async def start(interaction: discord.Interaction):
    if is_server_running():
        embed = discord.Embed(
            description="サーバーは既に起動しています"
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        start_server()
        embed = discord.Embed(
            title="サーバーを起動します",
            color=0x00ff00,
            description="しばらくおまちください。"
            )
        await interaction.response.send_message(embed=embed)


#シード値設定
@tree.command(name="setseed", description="ワールドのシード値を設定する。seed引数を設定せずに実行できます。")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(seed='シード値')
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
                title="シード値を変更しました",
                color=0x00ff00,
                description="シード値が設定されていないので、世界はランダムに生成されます。"
                )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="シード値を変更しました",
                color=0x00ff00,
                description=f"新しいシード値は `{seed}` です。"
                )
            await interaction.response.send_message(embed=embed)


#最大プレイヤー数
@tree.command(name="setmaxplayers", description="最大プレイヤー数を変更する")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(maxplayers='最大プレイヤー数')
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
            title="最大プレイヤー数を変更しました",
            color=0x00ff00,
            description=f"新しい最大プレイヤー数は `{maxplayers}` です。"
            )
        await interaction.response.send_message(embed=embed)


#PVP設定
@tree.command(name="setpvp", description="PVPの設定を変更する")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(on_or_off="オンかオフか")
@app_commands.choices(
    on_or_off=[
        discord.app_commands.Choice(name="オン",value="true"),
        discord.app_commands.Choice(name="オフ",value="false")
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
            embed = discord.Embed(
                title="PVPの設定を変更しました",
                color=0x00ff00,
                description=f"PVPの設定は **オン** になりました"
                )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="PVPの設定を変更しました",
                color=0x00ff00,
                description=f"PVPの設定は **オフ** になりました"
                )
            await interaction.response.send_message(embed=embed)


#ゲーム難易度設定
@tree.command(name="setdifficulty", description="ゲーム難易度を変更する")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(difficulty="難易度")
@app_commands.choices(
    difficulty=[
        discord.app_commands.Choice(name="ピースフル",value="peaceful"),
        discord.app_commands.Choice(name="イージー",value="easy"),
        discord.app_commands.Choice(name="ノーマル",value="normal"),
        discord.app_commands.Choice(name="ハード",value="hard")
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
            difficulty = "ピースフル"
        elif difficulty == "easy":
            difficulty = "イージー"
        elif difficulty == "normal":
            difficulty = "ノーマル"
        else:
            difficulty = "ハード"
        embed = discord.Embed(
            title="ゲーム難易度を変更しました",
            color=0x00ff00,
            description=f"ゲーム難易度は **{difficulty}** になりました"
            )
        await interaction.response.send_message(embed=embed)
        

#ワールド名指定
@tree.command(
        name="changeworld", 
        description="遊ぶワールドを変更する。存在しないワールド名を入力することで、新しいワールドが生成される。"
        )
@app_commands.default_permissions(administrator=True)
@app_commands.describe(world='ワールド名')
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
            title="遊ぶワールドを変更しました",
            color=0x00ff00,
            description=f"サーバーを起動すると、ワールド名 `{world}` が読み込まれます"
            )
        await interaction.response.send_message(embed=embed)


#botの停止
@tree.command(name="logout", description="このbotをログアウトさせる")
@app_commands.default_permissions(administrator=True)
async def exitbot(interaction: discord.Interaction):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        embed = discord.Embed(
            title="ログアウトします",
            description="botは停止されます。"
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
        title="エラー：サーバーが起動中です",
        color=0xff0000,
        description="そのコマンドを実行するには、サーバーを終了してください。"
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