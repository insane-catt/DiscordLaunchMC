# DiscordLaunchMC
MinecraftサーバーをDiscordから起動するツールです。<br>
If you need an English version, [the English README is available here.](#discordlaunchmc-english-readme)<br>
**DiscordLaunchMC can now be changed to English in the settings. Therefore, DiscordLaunchMC-en, which was provided as an English version, is no longer supported.**<br>
以下の環境構築、botの初期設定が既に完了しているなら、[ここからbotのコマンドを確認できます。](#使えるコマンド一覧)<br>
If you have already completed the following environment setup and initial configuration of the bot, [you can check the bot commands from here.](#list-of-available-commands)
## 概要
- 任意の設定で新しくワールドを作ったり、サーバーの設定を変更する際、いちいちSSHで接続してserver.propertiesを編集しなくちゃいけないのがだるくなりそうな気がしたので、例のDiscord botに、Discordから簡単なコマンドを打てばserver.propertiesを編集してくれる機能を持たせることにした。
- また、前回のスクリプト（[Qiitaで書いた記事](https://qiita.com/insane_catt/items/f8cc4053a65334a8c9c4)）のままだと、管理者権限を持ってない人でも/startコマンドを打てたりしてしまうので、管理者権限を持つ人だけが実行できるように改良した。
- そして、この記事を見た人が簡単に実行できるように、**GitHubで配布することにした。**
## 実行環境
### 筆者の動作環境
- 動作コンピューター：Raspberry Pi 4 Model B （RAM8GB、SDカード64GB）
- 利用しているMinecraftサーバーソフト：Paper 1.20.1（プラグインとして、**DiscordSRV**、GeyserMC（floodgate付き）を導入済み）

### 必要な環境構築
- **Python3**：Python製のbotなので、当たり前だが必要。
- **discord.py**：Discord botを動かすために必要なライブラリ。Pycordなどと混同しないで。ターミナルで以下のコマンドを入力し、インストールする。
```shell
python3 -m pip install -U discord.py
```
- **Paper**：軽量で、**プラグインを導入可能**な、SpigotベースのJava版Minecraftサーバーソフトウェアである。これの上に、次に説明するDiscordSRVや、これは任意だが、統合版とのクロスプレイを可能にするGeyserMCを導入することができる。
- **DiscordSRV**：Discordに、サーバーの参加ログなどや、Minecraftサーバーのコンソールを表示させることができるプラグイン。筆者はこれのコンソールを利用しているので、自作のDiscord botにはMinecraftサーバーを終了させるコマンドを持たせていない。なので、DiscordSRVを導入しない場合や、公式配布のMinecraftサーバーソフトウェア（重い、プラグイン入らない）を使用する場合には、SSHなどからscreenに接続し、stopコマンドを打つ手間があるので、めんどくさい。DiscordSRVの使い方は長くなるので割愛するが、便利だし有名なので導入するべき。
![SRV_1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3530195/462ce4eb-3ff2-20f7-7e28-6db318c84b4c.png)
図１：参加ログ以外にも、進捗の達成や、死亡メッセージを表示することも可能
![SRV_2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3530195/507aceb4-f63b-e836-8b02-fb24a64245cd.png)
図2：Minecraftサーバーに直接コマンドを打つことが可能なコンソール画面。古い画像なのでメッセージの仕様が異なります。
seedコマンドとかも普通に使える。
PaperLaunchBotというのが、今回自作したbot。

- **screen**：Minecraftサーバーをバックグラウンドで動作させ、またそれに自由に接続・切断することを可能にするソフト。以下のコマンドをターミナルで実行し、インストールできる。
```shell
sudo apt install screen -y
```
## 初期設定
**PaperでのMinecraftサーバーは既に構築された状態を想定しています。** まずそれだけやって、それから以下のようにしてください。
1. 画面右のRelasesより`DiscordLaunchMC.zip`をダウンロードする。
1. パッケージ内の`DiscordLaunchMC.py`、`config.py`、`languages.py`をサーバーの実行ファイルのあるディレクトリに移動し、config.pyをエディタで開く。
1. 設定欄を任意で書き換えるか、ディレクトリ構成を「`/home/pi/minecraft/java/paper`」にし、そのpaperディレクトリをサーバーの実行ファイルのあるフォルダにする。
1. https://discord.com/developers/applications にアクセスし、ログインし、New Applicationボタンをクリック。名前を付け、チェックを入れ、Createする。
1. 画面左にBotと出るので、クリックし、Reset Tokenボタンを押し、Yes, do it!をクリック、その後Copyボタンを押して**トークンを**`config.py`**内の「TOKEN」と置き換える。**
1. Privileged Gateway Intentsのところの切り替えスイッチを全部オンにし、下に出てきたSave changesボタンをクリック。
1. 画面左のOAuth2→URL Generatorとクリックし、大量のチェックボックスの中から`bot`、`applications.commands`にチェックを入れる。その後、下にまた出てきた大量のチェックボックスの中から、もうめんどくさいので`Administrator`（管理者って意味）をクリック。（セキュリティー的に怖かったらいちいち設定する必要があるけど攻撃されるかもとか思わなければ管理者でいいと思う、自分のbotだしトークンを人に教えたり流出しなければいい。）
1. 一番下に出たGENERATED URLをコピーしてブラウザで開き、botをDiscordサーバーに招待する。
1. 以下のコマンドで実行する。
```shell
python3 DiscordLaunchMC.py
```

## 使えるコマンド一覧
### いつでも使えるコマンド
- `/hello`：こんにちは、【コマンドを実行したユーザー】さん！と返してくれる。誰でも使えるコマンド。botの動作確認などに使用できる。
### サーバー停止中にDiscordサーバー管理者のみ使えるコマンド
- **`/start`**：サーバーを起動するコマンド。
- `/changeworld`：遊ぶワールドを変更する。引数として、ワールド名を入力する必要がある。存在しないワールド名を入力することで、新しいワールドが生成される。
- `/setseed`：シード値を指定する。引数を指定しなかった場合、ランダムなシード値にする。
- `/setdifficulty`：ゲーム難易度を引数で変更する。
- `/setpvp`：PVPのオンオフを引数で変更する。
- `/sethardcore`：ハードコアのオンオフを引数で変更する。
- `/setmaxplayers`：最大プレイヤー数を変更できる。
- `/setdirectly`：server.propertiesのプロパティ名を入れ、コマンドを送信後、`=`に続く設定したい値を送信すると、server.propertiesのプロパティを直接編集できる。このコマンドは慎重に使わないとサーバーが意図しない動作をする可能性があるので、気を付けて。
- `/searchproperty`：`/setdirectly`コマンドを使う際などにプロパティ名の一部しか覚えていない場合、このコマンドでプロパティ名の一部を送信するとプロパティを検索することができる。プロパティの現在の設定もここで確認できる。
- `/logout`：Botを停止させる。

その他、ゲームモード（サバイバルとかクリエイティブとか）だったりはサーバー起動中にSRVとかのコンソールとかに入力してください。**気が向いたり要望があれば機能追加します。コメントください。**

## 上手くいかない場合の連絡先
Twitter（X笑）
https://twitter.com/insane_catt

DMまでどうぞ

## バージョン履歴
- v1.1.1：毎日botの名前を出力することでコンソールでどのbotが稼働しているかわかるようにした。
- v1.1：config.pyから英語を利用可能にした。また、/setmaxplayersコマンド、/setdirectlyコマンド、/searchpropertyコマンドを実装した。
- v1.0.7：README更新とコメントの修正
- v1.0.6：簡単な設定をconfig.pyに移動
- v1.0.5：READMEの更新、ENバージョンの分離
- v1.0.4：READMEの更新
- v1.0.3：READMEの更新
- v1.0.2：/logoutコマンドの実装
- v1.0.1：サーバーを起動する際のメッセージ若干変更
- v1.0.0

# DiscordLaunchMC (English README)
A Discord bot that can start a Minecraft server with custom settings.
This English text was translated using Bing Chat and DeepL. We do our best to ensure the quality of the translation, but just in case, please watch out for translation errors.
If you have already completed the following environment setup and initial configuration of the bot, [you can check the bot commands from here.](#list-of-available-commands)
## Overview
- I thought it would be tedious to have to connect via SSH and edit the server.properties file every time I wanted to create a new world with different settings or change the server settings, so I decided to add a feature to the Discord bot that allows me to edit the server.properties file by typing simple commands on Discord.
- Also, in the previous script ([the article I wrote on Qiita](https://qiita.com/insane_catt/items/f8cc4053a65334a8c9c4)), anyone could use the /start command even if they didn't have administrator privileges, so I improved it so that only people with administrator privileges could execute it.
- And, to make it easy for anyone who sees this article to run it, I decided to **distribute it on GitHub**.
## Execution environment
### My operating environment
- Operating computer: Raspberry Pi 4 Model B (RAM 8GB, SD card 64GB)
- Minecraft server software used: Paper 1.20.1 (with **DiscordSRV** and GeyserMC (with floodgate) plugins installed)

### Required environment setup
- **Python3**: It's a Python-based bot, so obviously it's necessary.
- **discord.py**: A library required to run a Discord bot. Don't confuse it with Pycord or something. Enter the following command in the terminal and install it.
```shell
python3 -m pip install -U discord.py
```
- **Paper**: A lightweight, Spigot-based Java edition Minecraft server software that allows you to install **plugins**. On top of this, you can install DiscordSRV and GeyserMC, which are optional but allow cross-play with the integrated version, which I will explain next.
- **DiscordSRV**: A plugin that allows you to display server join logs and Minecraft server console on Discord. I use this console, so I don't have a command to stop the Minecraft server in my custom Discord bot. So, if you don't install DiscordSRV or use the official Minecraft server software (heavy, no plugins), you have to go through the hassle of connecting to screen via SSH and typing the stop command. I won't explain how to use DiscordSRV because it's long, but it's useful and famous so you should install it.
![SRV_1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3530195/462ce4eb-3ff2-20f7-7e28-6db318c84b4c.png)
Figure 1: In addition to join logs, you can also display achievements and death messages.
![SRV_2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3530195/507aceb4-f63b-e836-8b02-fb24a64245cd.png)
Figure 2: A console screen that allows you to directly enter commands on the Minecraft server. This is an old image, so the message specifications are different.
You can also use commands like seed normally.
PaperLaunchBot is the bot I made this time.

- **screen**: A software that allows you to run a Minecraft server in the background and connect and disconnect from it freely. You can install it by running the following command in the terminal.
```shell
sudo apt install screen -y
```
## Initial configuration
**It is assumed that you have already set up a Minecraft server with Paper.** First, do that, and then follow these steps.
1. Download the package from the Releases on the right side of the screen.
1. Move `DiscordLaunchMC.py` , `config.py` and `languages.py` from the package to the directory where the server executable file is located, and open `config.py` with an editor.
1. Either modify the settings section as desired or set the directory structure to `/home/pi/minecraft/java/paper` and make the `paper` directory the folder where the server executable file is located.
1. Go to https://discord.com/developers/applications, log in, and click the New Application button. Give it a name, check the box, and create it.
1. On the left side of the screen, click on "Bot", then click the "Reset Token" button, confirm by clicking "Yes, do it!", and finally click the "Copy" button. **Replace the TOKEN in `config.py` with this copied token.**
1. **If you want to use this bot in English, change the `LANG = "jp"` setting in `config.py` to `LANG = "en"`.**
1. Turn on all the toggle switches in Privileged Gateway Intents and click the Save changes button that appears at the bottom.
1. Click OAuth2 → URL Generator on the left side of the screen and check `bot` and `applications.commands` from a large number of checkboxes. Then, from another large number of checkboxes that appear below, click `Administrator` because it's too much trouble. (You may need to set each one individually for security reasons, but I think it's fine to be an administrator if you don't worry about being attacked or something. It's your own bot and you just have to keep your token from being leaked or told to anyone.)
1. Copy the GENERATED URL that appears at the bottom and open it in your browser to invite the bot to your Discord server.
1. Run it with the following command.
```shell
python3 DiscordLaunchMC.py
```

## List of available commands
### Commands that can be used at any time
- `/hello`: Replies with "Hello, [user who executed the command]!" This command can be used by anyone to check if the bot is working properly.
### Commands that can only be used by Discord server administrators when the server is stopped
- **`/start`**: A command to start the server.
- `/changeworld`: Change the world you play in. You need to enter the world name as an argument. Entering a non-existent world name will generate a new world.
- `/setseed`: Specify a seed value. If no argument is specified, it will use a random seed value.
- `/setdifficulty`: Change the game difficulty with an argument.
- `/setpvp`: Change PVP on/off by argument.
- `/sethardcore`: Change hardcore on/off by argument.
- `/setmaxplayers`: change the maximum number of players.
- `/setdirectly`: You can edit the properties of server.properties directly by entering the property name in server.properties and sending the value you want to set following `=` after sending the command. This command must be used carefully or the server may behave in an unintended way.
- `/searchproperty`: If you only remember part of a property name, such as when using the `/setdirectly` command, you can search for a property by sending part of the property name with this command.The property's current settings can also be viewed here.
- `/logout`: Stop the bot.

For other things like game mode (survival or creative or something), please enter them on SRV or something console or something while the server is running. **I will add features if I feel like it or if there are requests. Please comment.**

## Contact information in case of trouble
Twitter (X lol)<br>
https://twitter.com/insane_catt

Please DM me

## Version history
- v1.1.1: Added functionality to output the bot's name daily, making it easier to identify which bot is running in the console.
- v1.1: Enabled to use English from the config.py. Also, implemented /setmaxplayers, /setdirectly and /searchproperty command.
- v1.0.7-en: Updated README and revised comments
- v1.0.6-en: Moved simple settings to config.py
- v1.0.5-en: Updated README and separated the English version
- v1.0.4: Updated README
- v1.0.3: Updated README
- v1.0.2: Implemented /logout command
- v1.0.1: Slightly changed message when starting server
- v1.0.0