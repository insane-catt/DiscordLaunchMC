# EN: This file is DiscordLaunchMC (Japanese version). If you want to use English, please use DiscordLaunchMC-en.
# JP: このファイルはDiscordLaunchMC（日本語版）です。英語を使用したい場合は、DiscordLaunchMC-enを使用してください。
# DiscordLaunchMC-en: https://github.com/insane-catt/DiscordLaunchMC-en


# 以下は簡単な設定欄です

TOKEN = "TOKEN"  # Discord botのトークンを入力してください
SERVER_PATH = "minecraft/java/paper"  # Minecraft実行ファイルのあるフォルダのホームディレクトリからのパスを入力してください
HOME_DIRECTORY = "/home/pi"  # ホームディレクトリのパスを入力してください
JAR_FILE = "paper.jar"  # 使用しているMinecraftサーバー実行ファイルの名前を入力してください
SCREEN_NAME = "papermc"  # 使用するscreenセッションの名前を入力してください
MAX_RAM = "5"  #使用する最大メモリを設定してください。デフォルトは5
MIN_RAM = "2"  #使用する最小メモリを設定してください。デフォルトは2



# 以下はコードです。必要に応じていじってください

import discord
from discord import app_commands
import subprocess
import sys

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="hello", description="Hello, world!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}!')


@tree.command(name="start", description="サーバーを起動する")
@app_commands.default_permissions(administrator=True)
async def start(interaction: discord.Interaction):
    if is_server_running():
        await interaction.response.send_message('サーバーは既に起動しています')
    else:
        start_server()
        await interaction.response.send_message('サーバーを起動します。しばらくおまちください')


@tree.command(name="setseed", description="ワールドのシード値を設定する")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(seed='シード値')
async def setseed(interaction: discord.Interaction, seed: str = None):
    if is_server_running():
        await interaction.response.send_message('サーバーが起動中のため、そのコマンドは実行できません')
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
            await interaction.response.send_message("シード値をデフォルト（ランダム）に変更しました")
        else:
            await interaction.response.send_message(f"シード値を【{seed}】に変更しました")


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
        await interaction.response.send_message("サーバーが起動中のため、そのコマンドは実行できません")
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
            await interaction.response.send_message("PVPの設定を **オン** に変更しました")
        else:
            await interaction.response.send_message("PVPの設定を **オフ** に変更しました")



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
        await interaction.response.send_message("サーバーが起動中のため、そのコマンドは実行できません")
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
            await interaction.response.send_message("ゲーム難易度を **ピースフル** に変更しました")
        elif difficulty == "easy":
            await interaction.response.send_message("ゲーム難易度を **イージー** に変更しました")
        elif difficulty == "normal":
            await interaction.response.send_message("ゲーム難易度を **ノーマル** に変更しました")
        else:
            await interaction.response.send_message("ゲーム難易度を **ハード** に変更しました")
        


@tree.command(
        name="changeworld", 
        description="遊ぶワールドを変更する。存在しないワールド名を入力することで、新しいワールドが生成される。"
        )
@app_commands.default_permissions(administrator=True)
@app_commands.describe(world='ワールド名')
async def changeworld(interaction: discord.Interaction, world: str):
    if is_server_running():
        await interaction.response.send_message('サーバーが起動中のため、そのコマンドは実行できません')
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

        await interaction.response.send_message(f"ワールドを **{world}** に変更しました")


@tree.command(name="logout", description="このbotをログアウトさせる")
@app_commands.default_permissions(administrator=True)
async def exitbot(interaction: discord.Interaction):
    if is_server_running():
        await interaction.response.send_message('サーバーが起動しています。そのコマンドを実行するには、サーバーを終了してください。')
    else:
        await interaction.response.send_message('ログアウトを実行します')
        print("The logout command has been executed.")
        sys.exit()


def is_server_running():
    process = subprocess.Popen(f"screen -ls {SCREEN_NAME}", stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    return SCREEN_NAME in output.decode()

def start_server():
    subprocess.Popen(f"screen -dmS {SCREEN_NAME} java -Xmx{MAX_RAM}G -Xms{MIN_RAM}G -jar {JAR_FILE} nogui", shell=True)


@client.event
async def on_ready():
        await client.change_presence(activity=discord.Game(name="Minecraft"))
        await tree.sync()
        print("login complete")

client.run(TOKEN)