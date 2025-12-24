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
import traceback
import re

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


#翻訳
from languages import dictionary
def tr(text):
    if LANG == "jp":
        # 日本語の場合はそのまま返す
        return text
    else:
        try:
            return dictionary[LANG][text]
        except KeyError:
            return "Sorry, translation into English failed. Displaying message in Japanese: " + text
    
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
            await interaction.response.send_message(error(tr("ワールドが見つかりませんでした"), tr("ワールドを作成してください。")), ephemeral=True)
        else:
            worlds_list = "\n".join(sorted(world_names))
            embed = discord.Embed(
                title=tr("サーバー内のワールド一覧"),
                color=0x00ff00,
                description=f"```\n{worlds_list}\n```"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(error(tr("ワールド一覧の取得中にエラーが発生しました。"), tr("以下はエラーの内容です：") + "\n" + str(e)), ephemeral=True)


# PaperMCを最新安定版に更新するコマンド
@tree.command(name="updatepaper", description=tr("PaperMCの最新のビルドをサーバーにダウンロードする"))
@app_commands.default_permissions(administrator=True)
@app_commands.describe(version=tr("バージョン（省略可）"))
async def updatepaper(interaction: discord.Interaction, version: str = None):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
        return

    # 安全にメッセージを送るヘルパー: まだ応答していなければ interaction.response を使い、
    # そうでなければ interaction.followup を使う。両方で失敗したらチャンネルへ直接送る。
    async def safe_send(*, content: str = None, embed: discord.Embed = None, ephemeral: bool = True):
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(content=content, embed=embed, ephemeral=ephemeral)
                return
        except Exception as e:
            print("safe_send: response.send_message failed:", e)
        try:
            await interaction.followup.send(content=content, embed=embed, ephemeral=ephemeral)
            return
        except Exception as e:
            print("safe_send: followup.send failed:", e)
        try:
            # 最後の手段としてチャンネルへ送信（公開）
            channel = interaction.channel
            if channel is not None:
                await channel.send(content=content, embed=embed)
                return
        except Exception as e:
            print("safe_send: channel.send failed:", e)

    print("updatepaper: starting update (no initial defer)")
    try:
        jar_path = os.path.join(SERVER_PATH, JAR_FILE)
        print(f"updatepaper: SERVER_PATH={SERVER_PATH}, JAR_FILE={JAR_FILE}, jar_path={jar_path}")

        # 1) 既存の jar はすぐ削除せずバックアップへ移動（失敗時に復元できるようにする）
        backup_path = jar_path + ".bak"
        if os.path.exists(jar_path):
            try:
                # 上書き可能にするため先に既存の bak を削除
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.replace(jar_path, backup_path)
                print(f"updatepaper: existing jar moved to backup: {backup_path}")
            except Exception as e:
                print("updatepaper: failed to backup existing jar:", e)

        else:
            print("updatepaper: no existing jar found, continuing")


        # Fill v3 API
        base = "https://fill.papermc.io/v3/projects/paper"
        headers = {
            "User-Agent": "DiscordLaunchMC/1.0 (+https://github.com/insane-catt/DiscordLaunchMC)",
            "Accept": "application/json"
        }

        # バージョン一覧取得（レスポンスが dict の場合 'versions' キーを利用）
        resp = requests.get(f"{base}/versions", headers=headers, timeout=30)
        resp.raise_for_status()
        versions_raw = resp.json()
        if isinstance(versions_raw, dict) and 'versions' in versions_raw:
            versions = versions_raw['versions']
        else:
            versions = versions_raw
        if not versions or not isinstance(versions, (list, tuple)):
            raise Exception(tr("PaperMCのバージョンが取得できませんでした。"))

        # versions 内には文字列だけでなく dict が混在することがある。
        # 各要素からバージョンIDを抽出してリスト化する。
        version_ids = []
        for v in versions:
            if isinstance(v, str):
                version_ids.append(v)
            elif isinstance(v, dict):
                if 'id' in v and isinstance(v['id'], str):
                    version_ids.append(v['id'])
                elif 'version' in v:
                    vv = v['version']
                    if isinstance(vv, dict) and 'id' in vv and isinstance(vv['id'], str):
                        version_ids.append(vv['id'])
                    elif isinstance(vv, str):
                        version_ids.append(vv)
                elif 'name' in v and isinstance(v['name'], str):
                    version_ids.append(v['name'])

        print(f"updatepaper: extracted version_ids={version_ids}")
        if not version_ids:
            raise Exception(tr("PaperMCのバージョンIDが抽出できませんでした。"))

        # ユーザーがバージョンを指定した場合はそれを使う
        if version:
            print(f"updatepaper: user requested version={version}")
            if version not in version_ids:
                # 指定バージョンが存在しない場合はバックアップを復元してエラーを返す
                if os.path.exists(backup_path) and not os.path.exists(jar_path):
                    try:
                        os.replace(backup_path, jar_path)
                        print("updatepaper: restored backup due to invalid requested version")
                    except Exception as e:
                        print("updatepaper: failed to restore backup after invalid version request:", e)
                await safe_send(embed=error(tr("指定されたバージョンが見つかりませんでした。"), tr("バージョン番号を確認して、もう一度試して下さい。") + "\n" + tr("指定されたバージョン：") + f"{version}"), ephemeral=True)
                return
            latest_version = version
            print(f"updatepaper: using requested version {latest_version}")
        

        # 安定版(Stable)を選ぶ: 'rc' や 'pre' を含むバージョンを除外
        def version_key(v):
            nums = re.findall(r"\d+", v)
            return tuple(int(x) for x in nums)

        # ユーザーがバージョンを指定している場合は、そのまま使う（下の自動選定ロジックはスキップ）
        if not version:
            stable_versions = [v for v in version_ids if not re.search(r'(?i)(?:rc|pre)', v)]
            latest_version = None
            if stable_versions:
                # 安定版の中で、まず channel=RECOMMENDED のビルドが存在する最新のものを探す。
                stable_sorted = sorted(stable_versions, key=version_key)
                # Try RECOMMENDED first
                for v in reversed(stable_sorted):
                    print(f"updatepaper: checking stable candidate {v} for RECOMMENDED build...")
                    try:
                        resp = requests.get(f"{base}/versions/{v}/builds/latest", headers=headers, params={"channel": "RECOMMENDED"}, timeout=20)
                        print(f"updatepaper: HTTP status for {v} (RECOMMENDED) -> {resp.status_code}")
                        if resp.status_code == 404:
                            print(f"updatepaper: no builds/latest (404) for {v} with channel=RECOMMENDED")
                            continue
                        resp.raise_for_status()
                        try:
                            candidate_build_info = resp.json()
                        except Exception as e:
                            print(f"updatepaper: failed to parse JSON for {v} (RECOMMENDED): {e}")
                            continue
                        if isinstance(candidate_build_info, dict):
                            keys = list(candidate_build_info.keys())
                            print(f"updatepaper: build_info keys for {v} (RECOMMENDED): {keys}")
                            downloads_summary = None
                            try:
                                downloads = candidate_build_info.get('downloads')
                                if isinstance(downloads, dict):
                                    downloads_summary = list(downloads.keys())
                            except Exception:
                                downloads_summary = str(type(downloads))
                            print(f"updatepaper: downloads keys for {v} (RECOMMENDED): {downloads_summary}")
                        build_info = candidate_build_info
                        latest_version = v
                        print(f"updatepaper: selected stable version with RECOMMENDED build={latest_version}")
                        break
                    except Exception as e:
                        print(f"updatepaper: exception while checking {v} for RECOMMENDED: {e}")
                        continue

                # If no RECOMMENDED build found, try STABLE
                if latest_version is None:
                    for v in reversed(stable_sorted):
                        print(f"updatepaper: checking stable candidate {v} for STABLE build...")
                        try:
                            resp = requests.get(f"{base}/versions/{v}/builds/latest", headers=headers, params={"channel": "STABLE"}, timeout=20)
                            print(f"updatepaper: HTTP status for {v} (STABLE) -> {resp.status_code}")
                            if resp.status_code == 404:
                                print(f"updatepaper: no builds/latest (404) for {v} with channel=STABLE")
                                continue
                            resp.raise_for_status()
                            try:
                                candidate_build_info = resp.json()
                            except Exception as e:
                                print(f"updatepaper: failed to parse JSON for {v} (STABLE): {e}")
                                continue
                            if isinstance(candidate_build_info, dict):
                                keys = list(candidate_build_info.keys())
                                print(f"updatepaper: build_info keys for {v} (STABLE): {keys}")
                                downloads_summary = None
                                try:
                                    downloads = candidate_build_info.get('downloads')
                                    if isinstance(downloads, dict):
                                        downloads_summary = list(downloads.keys())
                                except Exception:
                                    downloads_summary = str(type(downloads))
                                print(f"updatepaper: downloads keys for {v} (STABLE): {downloads_summary}")
                            build_info = candidate_build_info
                            latest_version = v
                            print(f"updatepaper: selected stable version with STABLE build={latest_version}")
                            break
                        except Exception as e:
                            print(f"updatepaper: exception while checking {v} for STABLE: {e}")
                            continue

            if latest_version is None:
                # fallback: 安定版でSTABLEが見つからなければ通常の最大選定
                if stable_versions:
                    latest_version = max(stable_versions, key=version_key)
                    print(f"updatepaper: no STABLE build found for any stable version, selected latest stable={latest_version}")
                else:
                    latest_version = max(version_ids, key=version_key)
                    print(f"updatepaper: no stable versions found, selected latest overall={latest_version}")

        # /builds/latest をチャネル優先で試す
        build_info = None
        for channel in ["RECOMMENDED", "STABLE", None]:
            params = {"channel": channel} if channel else None
            resp = requests.get(f"{base}/versions/{latest_version}/builds/latest", headers=headers, params=params, timeout=30)
            if resp.status_code == 404:
                continue
            try:
                resp.raise_for_status()
                build_info = resp.json()
                break
            except Exception:
                pass
        print(f"updatepaper: build_info obtained: {bool(build_info)}")

        # fallback: builds リストから最大の build id を取得
        if build_info is None:
            resp = requests.get(f"{base}/versions/{latest_version}/builds", headers=headers, timeout=30)
            resp.raise_for_status()
            builds = resp.json()
            ids = []
            for b in builds:
                if isinstance(b, dict):
                    ids.append(b.get('id') or b.get('build'))
                elif isinstance(b, int):
                    ids.append(b)
            if not ids:
                raise Exception(tr("ビルド番号が特定できませんでした。"))
            build_num = max(ids)
            resp = requests.get(f"{base}/versions/{latest_version}/builds/{build_num}", headers=headers, timeout=30)
            resp.raise_for_status()
            build_info = resp.json()

        downloads = build_info.get('downloads', {})
        if not downloads:
            raise Exception(tr("ダウンロード情報が見つかりませんでした。"))

        # server:default を優先
        download_obj = None
        if isinstance(downloads, dict):
            download_obj = downloads.get('server:default')
            if not download_obj:
                for v in downloads.values():
                    if isinstance(v, dict) and v.get('name', '').endswith('.jar'):
                        download_obj = v
                        break

        if not download_obj:
            raise Exception(tr("ダウンロード対象のファイルが見つかりませんでした。"))

        download_url = download_obj.get('url')
        if not download_url:
            raise Exception(tr("ダウンロードURLが取得できませんでした。"))
        print(f"updatepaper: download_url={download_url}")

        # 確認フロー：ユーザーにダウンロード候補を表示し、承認があるまで待つ
        try:
            info_title = latest_version
            build_id = None
            if isinstance(build_info, dict):
                build_id = build_info.get('id') or build_info.get('build')
            msg_text = tr("以下のバージョンをダウンロードします。よろしいですか？") + "\n"
            msg_text += f"Version: {latest_version}\n"
            if build_id is not None:
                msg_text += f"Build: {build_id}\n"

            class ConfirmView(discord.ui.View):
                def __init__(self, author):
                    super().__init__(timeout=60)
                    self.value = None
                    self.author = author
                    self.interaction_ref = None
                    self.message = None
                    self.progress_message = None

                @discord.ui.button(label=tr("ダウンロード"), style=discord.ButtonStyle.green)
                async def confirm(self, inter: discord.Interaction, button: discord.ui.Button):
                    if inter.user.id != self.author.id:
                        await inter.response.send_message(tr("あなたはこの操作を行えません。"), ephemeral=True)
                        return
                    # defer the component interaction so the user sees a waiting state
                    await inter.response.defer()
                    self.interaction_ref = inter
                    # delete the confirmation message (the one containing the buttons)
                    if self.message is not None:
                        try:
                            await self.message.delete()
                        except Exception:
                            pass
                    # send a plain progress message (non-ephemeral so it can be deleted later)
                    try:
                        self.progress_message = await inter.followup.send(tr("ダウンロードしています。おまちください..."), ephemeral=False)
                    except Exception:
                        self.progress_message = None
                    self.value = True
                    self.stop()

                @discord.ui.button(label=tr("キャンセル"), style=discord.ButtonStyle.red)
                async def cancel(self, inter: discord.Interaction, button: discord.ui.Button):
                    if inter.user.id != self.author.id:
                        await inter.response.send_message(tr("あなたはこの操作を行えません。"), ephemeral=True)
                        return
                    await inter.response.defer()
                    self.interaction_ref = inter
                    # delete the confirmation message
                    if self.message is not None:
                        try:
                            await self.message.delete()
                        except Exception:
                            pass
                    self.value = False
                    self.stop()

            view = ConfirmView(interaction.user)
            # send confirmation as the initial response so followups are available later
            await interaction.response.send_message(msg_text, ephemeral=False, view=view)
            # obtain the actual Message object for later deletion
            try:
                confirm_msg = await interaction.original_response()
            except Exception:
                confirm_msg = None
            # attach message object to view so callbacks can delete it
            view.message = confirm_msg

            # wait for the view to stop (timeout or button press)
            await view.wait()
            # If timed out, delete confirmation message (if still present) and restore backup
            if view.value is None:
                print("updatepaper: user confirmation timed out (buttons)")
                try:
                    if getattr(view, 'message', None):
                        await view.message.delete()
                except Exception:
                    pass
                if os.path.exists(backup_path) and not os.path.exists(jar_path):
                    try:
                        os.replace(backup_path, jar_path)
                        print("updatepaper: restored backup after timeout")
                    except Exception as e:
                        print("updatepaper: failed to restore backup after timeout:", e)
                await safe_send(content=tr("時間切れ：承認が得られませんでした。更新を中止しました。"), ephemeral=True)
                return
            if not view.value:
                # user cancelled
                print("updatepaper: user cancelled update via button")
                if os.path.exists(backup_path) and not os.path.exists(jar_path):
                    try:
                        os.replace(backup_path, jar_path)
                        print("updatepaper: restored backup after user cancellation")
                    except Exception as e:
                        print("updatepaper: failed to restore backup after cancellation:", e)
                # notify the user who pressed the button (use the component interaction followup if available)
                try:
                    if getattr(view, 'interaction_ref', None):
                        await view.interaction_ref.followup.send(tr("更新がユーザーによってキャンセルされました。"), ephemeral=True)
                    else:
                        await safe_send(content=tr("更新がユーザーによってキャンセルされました。"), ephemeral=True)
                except Exception:
                    try:
                        await safe_send(content=tr("更新がユーザーによってキャンセルされました。"), ephemeral=True)
                    except Exception:
                        pass
                return
            print("updatepaper: user confirmed update via button, proceeding to download")

        except Exception as e:
            print("updatepaper: error during confirmation flow:", e)
            # 確認処理で致命的な問題があれば中止
            if os.path.exists(backup_path) and not os.path.exists(jar_path):
                try:
                    os.replace(backup_path, jar_path)
                except Exception as e2:
                    print("updatepaper: failed to restore backup after confirmation error:", e2)
            await safe_send(embed=error(tr("更新中止"), tr("承認フローでエラーが発生しました。")), ephemeral=True)
            return

        # 2) ダウンロード（まず一時ファイルへ）
        tmp_name = os.path.basename(download_url) or (JAR_FILE + ".tmp")
        tmp_path = os.path.join(SERVER_PATH, tmp_name + ".tmp")
        try:
            with requests.get(download_url, headers=headers, stream=True, timeout=120) as r:
                r.raise_for_status()
                total = 0
                with open(tmp_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            total += len(chunk)
                print(f"updatepaper: downloaded {total} bytes to {tmp_path}")

            # ダウンロード成功：一時ファイルを最終パスへ置換
            os.replace(tmp_path, jar_path)

            # バックアップがあれば削除
            if os.path.exists(backup_path):
                try:
                    os.remove(backup_path)
                except Exception:
                    pass

            # ダウンロード完了：まずプログレスメッセージを削除してから success embed を送る
            try:
                if getattr(view, 'progress_message', None):
                    try:
                        await view.progress_message.delete()
                    except Exception:
                        pass
            except Exception:
                pass

            # ダウンロード完了：まずプログレスメッセージを削除してから success embed を送る
            try:
                if getattr(view, 'progress_message', None):
                    try:
                        await view.progress_message.delete()
                    except Exception:
                        pass
            except Exception:
                pass

            sent = False
            try:
                if getattr(view, 'interaction_ref', None):
                    await safe_send(embed=success(tr("更新完了"), tr("最新ビルドの paper.jar をダウンロードしました。") + f"\nVersion: {latest_version}\nBuild: {build_id}"), ephemeral=False)
                    sent = True
            except Exception:
                sent = False
            if not sent:
                await safe_send(embed=success(tr("更新完了"), tr("最新ビルドの paper.jar をダウンロードしました。") + f"\nVersion: {latest_version}\nBuild: {build_id}"), ephemeral=False)
        except Exception:
            # ダウンロード失敗時はバックアップを復元する
            print("updatepaper: download failed, attempting to restore backup")
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            if os.path.exists(backup_path) and not os.path.exists(jar_path):
                try:
                    os.replace(backup_path, jar_path)
                except Exception as e:
                    print("updatepaper: failed to restore backup:", e)
            raise

    except Exception as e:
        tb = traceback.format_exc()
        print("updatepaper error:", str(e))
        print(tb)
        # まず短いメッセージを返信し、詳細はフォローアップで送る
        await safe_send(embed=error(tr("更新失敗"), str(e)), ephemeral=True)
        # フォローアップでトレースバックも送信（長い場合はカットされます）
        try:
            content = "```\n" + tb + "\n```"
            await safe_send(content=content, ephemeral=True)
        except Exception:
            pass


# 新: ModrinthからDiscordSRVをpluginフォルダにダウンロードして更新するコマンド
@tree.command(name="updatesrv", description=tr("DiscordSRVをModrinthからダウンロードしてpluginsフォルダに配置します"))
@app_commands.default_permissions(administrator=True)
async def updatesrv(interaction: discord.Interaction):
    if is_server_running():
        await interaction.response.send_message(embed=server_is_running(), ephemeral=True)
        return

    async def safe_send(*, content: str = None, embed: discord.Embed = None, ephemeral: bool = True):
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(content=content, embed=embed, ephemeral=ephemeral)
                return
        except Exception as e:
            print("updatesrv: response.send_message failed:", e)
        try:
            await interaction.followup.send(content=content, embed=embed, ephemeral=ephemeral)
            return
        except Exception as e:
            print("updatesrv: followup.send failed:", e)
        try:
            channel = interaction.channel
            if channel is not None:
                await channel.send(content=content, embed=embed)
                return
        except Exception as e:
            print("updatesrv: channel.send failed:", e)

    try:
        base = "https://api.modrinth.com"
        plugin_dir = os.path.join(SERVER_PATH, "plugins")
        os.makedirs(plugin_dir, exist_ok=True)

        # まず既知のスラッグで試す（Modrinth上のプロジェクトスラッグは変わることがあるため複数候補を試す）
        slugs = ["discordsrv", "DiscordSRV", "discord-srv"]
        versions = None
        for s in slugs:
            try:
                resp = requests.get(f"{base}/v2/project/{s}/version", timeout=20)
                if resp.status_code == 200:
                    versions = resp.json()
                    break
            except Exception:
                continue

        # 見つからなければ検索でフォールバック
        if not versions:
            try:
                resp = requests.get(f"{base}/v2/search", params={"query": "DiscordSRV", "facets": "[]"}, timeout=20)
                resp.raise_for_status()
                data = resp.json()
                hits = data.get("hits", [])
                if hits:
                    # hitsの最初のプロジェクトのslugを取得して再試行
                    proj_slug = hits[0].get("slug") or hits[0].get("project_id")
                    if proj_slug:
                        resp2 = requests.get(f"{base}/v2/project/{proj_slug}/version", timeout=20)
                        if resp2.status_code == 200:
                            versions = resp2.json()
            except Exception:
                versions = None

        if not versions:
            await safe_send(embed=error(tr("取得失敗"), tr("ModrinthでDiscordSRVが見つかりませんでした。")), ephemeral=True)
            return

        # 日付で最新のバージョンを選択
        versions_sorted = sorted(versions, key=lambda v: v.get("date_published", ""), reverse=True)
        chosen = versions_sorted[0]

        # jarファイルを探す
        file_obj = None
        for f in chosen.get("files", []):
            if f.get("filename", "").endswith(".jar"):
                file_obj = f
                break

        if not file_obj:
            await safe_send(embed=error(tr("取得失敗"), tr("ダウンロード可能なjarが見つかりませんでした。")), ephemeral=True)
            return

        download_url = file_obj.get("url")
        filename = file_obj.get("filename", "DiscordSRV.jar")
        dest_path = os.path.join(plugin_dir, filename)
        backup_path = dest_path + ".bak"

        # バックアップ
        if os.path.exists(dest_path):
            try:
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.replace(dest_path, backup_path)
            except Exception as e:
                print("updatesrv: backup failed:", e)

        # 確認フロー
        msg_text = tr("以下のファイルをダウンロードしてpluginsに配置します。よろしいですか？") + "\n"
        msg_text += f"Version: {chosen.get('id')}\nFilename: {filename}\n"

        class ConfirmView(discord.ui.View):
            def __init__(self, author):
                super().__init__(timeout=60)
                self.value = None
                self.author = author
                self.interaction_ref = None
                self.message = None
                self.progress_message = None

            @discord.ui.button(label=tr("ダウンロード"), style=discord.ButtonStyle.green)
            async def confirm(self, inter: discord.Interaction, button: discord.ui.Button):
                if inter.user.id != self.author.id:
                    await inter.response.send_message(tr("あなたはこの操作を行えません。"), ephemeral=True)
                    return
                await inter.response.defer()
                self.interaction_ref = inter
                if self.message is not None:
                    try:
                        await self.message.delete()
                    except Exception:
                        pass
                try:
                    self.progress_message = await inter.followup.send(tr("ダウンロードしています。おまちください..."), ephemeral=False)
                except Exception:
                    self.progress_message = None
                self.value = True
                self.stop()

            @discord.ui.button(label=tr("キャンセル"), style=discord.ButtonStyle.red)
            async def cancel(self, inter: discord.Interaction, button: discord.ui.Button):
                if inter.user.id != self.author.id:
                    await inter.response.send_message(tr("あなたはこの操作を行えません。"), ephemeral=True)
                    return
                await inter.response.defer()
                self.interaction_ref = inter
                if self.message is not None:
                    try:
                        await self.message.delete()
                    except Exception:
                        pass
                self.value = False
                self.stop()

        view = ConfirmView(interaction.user)
        await interaction.response.send_message(msg_text, ephemeral=False, view=view)
        try:
            confirm_msg = await interaction.original_response()
        except Exception:
            confirm_msg = None
        view.message = confirm_msg

        await view.wait()
        if view.value is None:
            try:
                if getattr(view, "message", None):
                    await view.message.delete()
            except Exception:
                pass
            if os.path.exists(backup_path) and not os.path.exists(dest_path):
                try:
                    os.replace(backup_path, dest_path)
                except Exception as e:
                    print("updatesrv: restore after timeout failed:", e)
            await safe_send(content=tr("時間切れ：承認が得られませんでした。更新を中止しました。"), ephemeral=True)
            return
        if not view.value:
            if os.path.exists(backup_path) and not os.path.exists(dest_path):
                try:
                    os.replace(backup_path, dest_path)
                except Exception as e:
                    print("updatesrv: restore after cancel failed:", e)
            try:
                if getattr(view, "interaction_ref", None):
                    await view.interaction_ref.followup.send(tr("更新がユーザーによってキャンセルされました。"), ephemeral=True)
                else:
                    await safe_send(content=tr("更新がユーザーによってキャンセルされました。"), ephemeral=True)
            except Exception:
                pass
            return

        # ダウンロード処理
        tmp_path = dest_path + ".tmp"
        try:
            with requests.get(download_url, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(tmp_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            os.replace(tmp_path, dest_path)
            if os.path.exists(backup_path):
                try:
                    os.remove(backup_path)
                except Exception:
                    pass
            try:
                if getattr(view, "progress_message", None):
                    try:
                        await view.progress_message.delete()
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                if getattr(view, "interaction_ref", None):
                    await safe_send(embed=success(tr("更新完了"), tr("DiscordSRVをpluginsにダウンロードしました。") + f"\nVersion: {chosen.get('id')}\nFilename: {filename}"), ephemeral=False)
                else:
                    await safe_send(embed=success(tr("更新完了"), tr("DiscordSRVをpluginsにダウンロードしました。") + f"\nVersion: {chosen.get('id')}\nFilename: {filename}"), ephemeral=False)
            except Exception:
                pass
        except Exception as e:
            print("updatesrv: download failed:", e)
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            if os.path.exists(backup_path) and not os.path.exists(dest_path):
                try:
                    os.replace(backup_path, dest_path)
                except Exception as e2:
                    print("updatesrv: restore failed after download error:", e2)
            tb = traceback.format_exc()
            await safe_send(embed=error(tr("更新失敗"), str(e)), ephemeral=True)
            try:
                await safe_send(content="```\n" + tb + "\n```", ephemeral=True)
            except Exception:
                pass

    except Exception as e:
        tb = traceback.format_exc()
        print("updatesrv error:", e)
        print(tb)
        await safe_send(embed=error(tr("更新失敗"), str(e)), ephemeral=True)
        try:
            await safe_send(content="```\n" + tb + "\n```", ephemeral=True)
        except Exception:
            pass

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