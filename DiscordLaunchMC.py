# 重要：ライセンスを変更しました。詳しくはREADMEとLICENSEを参照してください。
# Important note: The license has been changed. Please refer to README and LICENSE for details.

#以前ここにあった設定欄はconfig.pyに移動しました。
from config import *


# 以下はコードです。必要に応じていじってください

import discord
from discord import app_commands
import subprocess
import sys
import asyncio
from datetime import datetime, timedelta
import os
import requests
import json

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
    
# bot名の確認
async def daily_task():
    await client.wait_until_ready()
    while not client.is_closed():
        print(f"このbotは{client.user.name}です")
        now = datetime.now()
        # 翌日0時
        next_run = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        sleep_time = (next_run - now).total_seconds()
        await asyncio.sleep(sleep_time)



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

        with open(f"{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{SERVER_PATH}/server.properties", 'w') as file:
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

        with open(f"{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{SERVER_PATH}/server.properties", 'w') as file:
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
        with open(f"{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{SERVER_PATH}/server.properties", 'w') as file:
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
        with open(f"{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{SERVER_PATH}/server.properties", 'w') as file:
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
        with open(f"{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{SERVER_PATH}/server.properties", 'w') as file:
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

        with open(f"{SERVER_PATH}/server.properties", 'r') as file:
            lines = file.readlines()

        with open(f"{SERVER_PATH}/server.properties", 'w') as file:
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


#server.propertiesの直接編集コマンド
@tree.command(name="setdirectly", description=tr("server.propertiesを直接編集する。※間違えないように慎重に使ってください！"))
@app_commands.default_permissions(administrator=True)
@app_commands.describe(property_name=tr("プロパティ名"))
async def setdirectly(interaction: discord.Interaction, property_name: str):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        search_text = f"{property_name}="
        with open(f"{SERVER_PATH}/server.properties", 'r') as file:
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

        with open(f"{SERVER_PATH}/server.properties", 'w') as file:
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


#server.properties内のプロパティの検索コマンド
@tree.command(name="searchproperty", description=tr("プロパティ名の一部を指定して一致するプロパティを検索する"))
@app_commands.default_permissions(administrator=True)
@app_commands.describe(partial_name=tr("プロパティ名の一部"))
async def searchproperty(interaction: discord.Interaction, partial_name: str):
    search_text = partial_name
    matching_properties = []

    with open(f"{SERVER_PATH}/server.properties", 'r') as file:
        lines = file.readlines()

    for line in lines:
        if search_text in line:
            matching_properties.append(line.strip())

    if not matching_properties:
        await interaction.response.send_message(tr(f"次に一致する設定が見つかりませんでした:\n") + f"`{partial_name}`", ephemeral=True)
    else:
        properties_list = "\n".join(matching_properties)
        embed = discord.Embed(
            title=tr("一致するプロパティが見つかりました"),
            color=0x00ff00,
            description=tr("次のプロパティが見つかりました:\n") + f"```\n{properties_list}\n```"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


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


#allowlistの設定
@tree.command(name="allowlist", description=tr("サーバーに参加できるユーザーの許可リストを設定する"))
@app_commands.default_permissions(administrator=True)
@app_commands.describe(add_or_delete=tr("追加または削除"), user=tr("許可するユーザー"))
@app_commands.choices(
    add_or_delete=[
        discord.app_commands.Choice(name=tr("追加"), value="add"),
        discord.app_commands.Choice(name=tr("削除"), value="remove")
    ]
)
async def allowlist(interaction: discord.Interaction, add_or_delete: str, user: str):
    whitelist_file = f"{SERVER_PATH}/whitelist.json"
    def get_uuid(username):
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if response.status_code == 200:
            data = response.json()
            uuid = data["id"]
            uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
            return uuid
        return None
    if os.path.exists(whitelist_file):
        with open(whitelist_file, 'r') as f:
            try:
                whitelist = json.load(f)
            except Exception:
                whitelist = []
    else:
        whitelist = []
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
    else:
        if add_or_delete == "add":
            uuid = get_uuid(user)
            if not uuid:
                await interaction.response.send_message(embed=error(tr("UUIDの取得に失敗しました"), tr("ユーザー名：") + user), ephemeral=True)
                return
            # ユーザーが既に許可リストに存在するか確認
            if any(entry['uuid'] == uuid for entry in whitelist):
                await interaction.response.send_message(embed=error(tr("このユーザーは既に許可リストに存在します"), tr("ユーザー名：") + user), ephemeral=True)
                return
            whitelist.append({"uuid": uuid, "name": user})
            # allowlist.jsonに書き込む
            with open(whitelist_file, 'w') as f:
                json.dump(whitelist, f, indent=2)
            await interaction.response.send_message(embed=success(tr("許可リストに追加しました"), tr("許可リストに追加されたユーザー：") + user))
        elif add_or_delete == "remove":
            new_whitelist = [entry for entry in whitelist if entry['name'] != user]
            if len(new_whitelist) == len(whitelist):
                await interaction.response.send_message(embed=error(tr("このユーザーは許可リストに存在しません"), tr("ユーザー名：") + user), ephemeral=True)
                return
            with open(whitelist_file, 'w') as f:
                json.dump(new_whitelist, f, indent=2)
            await interaction.response.send_message(embed=success(tr("許可リストから削除しました"), tr("許可リストから削除されたユーザー：") + user))
        else:
            await interaction.response.send_message(embed=error(tr("無効なオプションです。"), ephemeral=True))


# ワールド一覧を表示する
@tree.command(name="listworlds", description=tr("サーバー内のワールド一覧を表示する"))
@app_commands.default_permissions(administrator=True)
async def listworlds(interaction: discord.Interaction):
    try:
        dirs = [d for d in os.listdir(SERVER_PATH) if os.path.isdir(os.path.join(SERVER_PATH, d))]
        world_names = set()
        for d in dirs:
            if d.endswith("_nether") or d.endswith("_the_end"):
                continue
            # ワールド名のディレクトリが存在し、_netherと_the_endも存在するか確認
            nether = f"{d}_nether"
            the_end = f"{d}_the_end"
            if nether in dirs and the_end in dirs:
                world_names.add(d)
        if not world_names:
            await interaction.response.send_message(error(tr("ワールドが見つかりませんでした"), "ワールドを作成してください。"), ephemeral=True)
        else:
            worlds_list = "\n".join(sorted(world_names))
            embed = discord.Embed(
                title=tr("サーバー内のワールド一覧"),
                color=0x00ff00,
                description=f"```\n{worlds_list}\n```"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(error(tr("ワールド一覧の取得中にエラーが発生しました。"), tr("以下はエラーの内容です：\n") + str(e)), ephemeral=True)


#コマンド群ここまで ------------------------------------------------------


def success(title, description):
    embed = discord.Embed(
        title=title,
        color=0x00ff00, # 緑
        description=description
        )
    return embed

def error(title, description):
    embed = discord.Embed(
        title=title,
        color=0xff0000, # 赤
        description=description
        )
    return embed

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
        client.loop.create_task(daily_task())

client.run(TOKEN)