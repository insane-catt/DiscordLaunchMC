# 以下は簡単な設定欄です。Below is a simple configuration field.
# 文字列はダブルクォーテーションで "このように" 囲ってください。Please enclose the string in double quotes "like this".

# 使用する言語を選択してください。日本語は"jp"、英語は"en"を入力してください。
# Please select the language you want to use. Enter "jp" for Japanese and "en" for English.
LANG = "jp"

# Discord botのトークンを入力してください。
# Please enter your Discord bot token.
TOKEN = "TOKEN"

# Minecraft実行ファイルのあるフォルダのホームディレクトリからのパスを入力してください。
# Please enter the path from the home directory of the folder where the Minecraft executable file is located.
SERVER_PATH = "/home/pi/minecraft/java/paper"

# 使用しているMinecraftサーバー実行ファイルの名前を入力してください。
# Please enter the name of the Minecraft server executable file you are using.
JAR_FILE = "paper.jar"

# 使用するscreenセッションの名前を入力してください。
# Please enter the name of the screen session you want to use.
SCREEN_NAME = "papermc"

# 使用する最大メモリと最小メモリを設定してください。
# Please set the maximum and minimum memory you want to use.
MAX_RAM = "5"
MIN_RAM = "2"



# 以下のコードは設定欄ではなく、変更は想定されていません。
# The following code is not a configuration section and is not intended to be changed.

import os

current_dir = os.getcwd()
jar_path = os.path.join(current_dir, JAR_FILE)
if os.path.isfile(jar_path):
    SERVER_PATH = current_dir