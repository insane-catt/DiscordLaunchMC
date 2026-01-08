最新バージョン (latest version): v1.3.1

### 重要
ライセンスを変更しました。詳しくは[こちら](#license--ライセンスが変更されました)と`LICENSE`ファイルをご覧ください。

### Important Notice
The license has been changed. For details, please see [here](#license-has-been-changed) and the `LICENSE` file.

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

### 前提の環境構築
- **Python3**：Python（3系）製のbotなので、当たり前だが必要。Raspberry Pi OSには同梱されていますが、もし無ければインストールしておいてください。<br>
以下のコマンドを実行し、正常にPython（3系）の情報が表示されればOK。
```shell
python3 --version
```
- **discord.py**：Discord botを動かすために必要なライブラリ。Pycordとは別物です。ターミナルで以下のコマンドを入力し、インストールする。
```shell
python3 -m pip install -U discord.py
```
- **Paper**：軽量で、**プラグインを導入可能**な、SpigotベースのJava版Minecraftサーバーソフトウェアである。これの上に、次に説明するDiscordSRVや、これは任意だが、統合版とのクロスプレイを可能にするGeyserMCを導入することができる。<br>
初期設定として、下のようなコマンドで一度最初に起動させ、eula.txtを編集する必要がある。詳しくはPaperでのMinecraftサーバーの構築の仕方を調べてほしい。<br>
（ダウンロードしてきたPaperの実行ファイルの名前に`paper-1.21.8-40.jar`のようにバージョン情報が含まれていたら、名前は`paper.jar`に変更する。）
```shell
java -Xmx1024M -Xms1024M -jar paper.jar nogui
```
- **screen**：Minecraftサーバーをバックグラウンドで動作させ、またそれに自由に接続・切断することを可能にするソフト。以下のコマンドをターミナルで実行し、インストールできる。
```shell
sudo apt install screen -y
```
- **DiscordSRV**：Discordに、サーバーの参加ログなどや、Minecraftサーバーのコンソールを表示させることができるプラグイン。筆者はこれのコンソールを利用しているので、自作のDiscord botにはMinecraftサーバーを終了させるコマンドを持たせていない。なので、DiscordSRVを導入しない場合や、公式配布のMinecraftサーバーソフトウェア（重い、プラグイン入らない）を使用する場合には、SSHなどからscreenに接続し、stopコマンドを打つ手間があるので、めんどくさい。DiscordSRVの使い方は長くなるので割愛するが、便利だし有名なので導入するべき。
![SRV_1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3530195/462ce4eb-3ff2-20f7-7e28-6db318c84b4c.png)
図１：参加ログ以外にも、進捗の達成や、死亡メッセージを表示することも可能
![SRV_2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3530195/507aceb4-f63b-e836-8b02-fb24a64245cd.png)
図2：Minecraftサーバーに直接コマンドを打つことが可能なコンソール画面。seedコマンドとかも普通に使える。<br>
古い画像なのでDiscordLaunchMC（ここではPaperLaunchBot）のメッセージの仕様が異なります。

## 初期設定
**前項の環境構築を済ませてから** 以下のようにしてください。
1. 画面右のRelasesより`DiscordLaunchMC.zip`をダウンロードする。
1. パッケージ内の`DiscordLaunchMC.py`、`config.py`、`languages.py`を`paper.jar`のあるディレクトリに移動し、`config.py`をエディタで開く。
1. `config.py`の設定欄を任意で書き換える。[次項「config.py」](#configpy)で説明する。

### config.py
初期設定において重要なファイルなので、`config.py`に予め書かれているコメントもしっかり確認しながら編集してください。<br>
文字列はダブルクォーテーションで "このように" 囲ってください。
1. `LANG`：「jp」にするとbotは日本語で応答する。「en」にするとbotは英語で応答する。
1. `TOKEN`：[次項「Discord botの組み立て」](#discord-botの組み立て)で触れる、Discord botのトークンをここに入力しておく。
1. `SERVER_PATH`：`paper.jar`と、`DiscordLaunchMC.py`、`config.py`、`languages.py`が同じディレクトリにあるなら、ここは特に設定する必要はない。
1. `JAR_FILE`：サーバーの実行ファイルを`paper.jar`以外の名前で起動したい場合、ここを任意の名前に変える。問題なければ、設定する必要はない。
1. `SCREEN_NAME`：screenでサーバーを起動する際のセッション名をここで設定できる。複数のサーバーを稼働させる場合、サーバーそれぞれの`config.py`でこの部分を`server_a`、`server_b`のように分けると便利かもしれない。
1. `MAX_RAM`、`MIN_RAM`：サーバーを稼働させるコンピューターの性能に応じて設定する。デフォルトでは私のRaspberry Piの8GBのRAMをたくさん使う設定にしているので、ここの変更はマストかと思われる。
ここより下に書いてあるコードは変更されることを想定していないので、分からなければいじらなくていい。

### Discord botの組み立て
1. https://discord.com/developers/applications にアクセスし、ログインし、New Applicationボタンをクリック。名前を付け、チェックを入れ、Createする。
1. 画面左にBotと出るので、クリックし、Reset Tokenボタンを押し、Yes, do it!をクリック、その後Copyボタンを押して**トークンを**`config.py`**内の「TOKEN」と置き換える。**
1. Privileged Gateway Intentsのところの切り替えスイッチを全部オンにし、下に出てきたSave changesボタンをクリック。
1. 画面左のOAuth2→URL Generatorとクリックし、大量のチェックボックスの中から`bot`、`applications.commands`にチェックを入れる。その後、下にまた出てきた大量のチェックボックスの中から、もうめんどくさいので`Administrator`（管理者って意味）をクリック。（セキュリティー的に怖かったらいちいち設定する必要があるけど攻撃されるかもとか思わなければ管理者でいいと思う、自分のbotだしトークンを人に教えたり流出しなければいい。）
1. 一番下に出たGENERATED URLをコピーしてブラウザで開き、botをDiscordサーバーに招待する。

## 実行する
ここまでの[前提の環境構築](#前提の環境構築)と[初期設定](#初期設定)を完了したら、準備ができている。<br>
`DiscordLaunchMC.py`のあるディレクトリに移動し、以下のコマンドで実行する。
```shell
python3 DiscordLaunchMC.py
```

## 使えるコマンド一覧
### いつでも使えるコマンド
- `/hello`：こんにちは、【コマンドを実行したユーザー】さん！と返してくれる。誰でも使えるコマンド。botの動作確認などに使用できる。
<hr>

### サーバー停止中にDiscordサーバー管理者のみ使えるコマンド
- **`/start`**：サーバーを起動するコマンド。
<hr>

- `/changeworld`：遊ぶワールドを変更する。引数として、ワールド名を入力する必要がある。存在しないワールド名を入力することで、新しいワールドが生成される。
- `/setseed`：シード値を指定する。引数を指定しなかった場合、ランダムなシード値にする。
- `/setdifficulty`：ゲーム難易度を引数で変更する。
- `/setpvp`：PVPのオンオフを引数で変更する。
- `/sethardcore`：ハードコアのオンオフを引数で変更する。
- `/setmaxplayers`：最大プレイヤー数を変更できる。
- `/setdirectly`：server.propertiesのプロパティ名を入れ、コマンドを送信後、`=`に続く設定したい値を送信すると、server.propertiesのプロパティを直接編集できる。このコマンドは慎重に使わないとサーバーが意図しない動作をする可能性があるので、気を付けて。
- `/searchproperty`：`/setdirectly`コマンドを使う際などにプロパティ名の一部しか覚えていない場合、このコマンドでプロパティ名の一部を送信するとプロパティを検索することができる。プロパティの現在の設定もここで確認できる。
- `/allowlist`：サーバーに参加できるユーザーを、`user`引数にいれて追加できる。許可リスト（whitelist.json）を編集する。
- `/listworlds`：サーバーディレクトリ内に存在するワールド一覧を表示する。
<hr>

- `/updatepaper`：PaperMCの最新ビルドを公式アプリを利用しダウンロードする。Minecraftのバージョンを`version`引数に入れて旧バージョンをダウンロードできる。入れなければAPIで入手できる最新バージョンがダウンロードされる。
- `/updategeyser`：GeyserMCとそれに付属するfloodgateの最新バージョンを公式APIを利用しpluginsディレクトリにダウンロードする。
- `/updatesrv`：DiscordSRVの最新バージョンをModrinthのAPIを利用しpluginsディレクトリにダウンロードする。
<hr>

- `/logout`：Botを停止させる。

その他、ゲームモード（サバイバルとかクリエイティブとか）だったりはサーバー起動中にSRVとかのコンソールとかに入力してください。**気が向いたり要望があれば機能追加します。コメントください。**

## 上手くいかない場合の連絡先
Twitter（X笑）
https://twitter.com/insane_catt

DMまでどうぞ

## License / ライセンスが変更されました。
本ソフトウェアは、もともと MIT ライセンスのもとで公開されていました。

バージョン 1.2.0 以降は、MIT ライセンスを基にした独自の倫理的ライセンスのもとで配布されています。  
この新しいライセンスでは、戦争、差別、社会的弱者への加害などの目的での使用を禁止しています。  
詳細は `LICENSE` ファイルをご覧ください。

### なぜライセンスを変更したのか？

私は、ソフトウェアが他者を傷つけたり、不正義に加担することに使われるべきではないと考えています。  
このライセンスは、戦争、差別、抑圧に反対する私自身の立場を反映したものです。

## バージョン履歴
- v1.3.1：コマンドに絵文字を追加
- v1.3：各種アップデートコマンドを追加
- v1.2.3：翻訳の挙動の改善
- v1.2.2：翻訳バグ修正
- v1.2.1：bot名の定期通知のバグ修正とlistworldsコマンドの追加など
- v1.2.0：**ライセンスの変更**、READMEの更新、`/allowlist`コマンドの追加
- v1.1.1：毎日botの名前を出力することでコンソールでどのbotが稼働しているかわかるようにした。
- v1.1：`config.py`から英語を利用可能にした。また、`/setmaxplayers`コマンド、`/setdirectly`コマンド、`/searchproperty`コマンドを実装した。
- v1.0.7：README更新とコメントの修正
- v1.0.6：簡単な設定を`config.py`に移動
- v1.0.5：READMEの更新、ENバージョンの分離
- v1.0.4：READMEの更新
- v1.0.3：READMEの更新
- v1.0.2：`/logout`コマンドの実装
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
- **Python3**: Since this bot is written in Python 3, you need to have Python 3 installed. Raspberry Pi OS comes with it, but if not, please install it.  
Check if Python 3 is installed by running:
```shell
python3 --version
```
- **discord.py**: Required library to run the Discord bot. This is different from Pycord. Install it by running:
```shell
python3 -m pip install -U discord.py
```
- **Paper**: A lightweight, Spigot-based Java edition Minecraft server software that allows you to install **plugins**. On top of this, you can install DiscordSRV and, optionally, GeyserMC for cross-play.  
For initial setup, you need to start the server once and edit `eula.txt`. Please refer to the official Paper documentation for details.  
If the downloaded Paper file is named like `paper-1.21.8-40.jar`, rename it to `paper.jar`.
```shell
java -Xmx1024M -Xms1024M -jar paper.jar nogui
```
- **screen**: Software that allows you to run the Minecraft server in the background and connect/disconnect freely. Install it by running:
```shell
sudo apt install screen -y
```
- **DiscordSRV**: A plugin that allows you to display server join logs and the Minecraft server console on Discord. Since this bot does not have a command to stop the Minecraft server, you need DiscordSRV to manage the server from Discord. If you do not use DiscordSRV or use the official Minecraft server software (which is heavier and does not support plugins), you will need to connect via SSH and use screen to stop the server manually.  
DiscordSRV is very useful and well-known, so it is highly recommended.

## Initial configuration
**Please complete the environment setup above before proceeding.**
1. Download `DiscordLaunchMC.zip` from Releases.
1. Move `DiscordLaunchMC.py`, `config.py`, and `languages.py` to the directory where `paper.jar` is located, and open `config.py` with an editor.
1. Edit the settings section of `config.py` as needed. See the next section ["config.py"](#configpy) for details.

### config.py
This is an important file for initial setup. Please read the comments in `config.py` carefully and edit as needed.  
Strings should be enclosed in double quotes, like "this".

1. `LANG`: Set to "jp" for Japanese or "en" for English responses.
1. `TOKEN`: Enter the Discord bot token here (see ["Building the Discord bot"](#building-the-discord-bot)).
1. `SERVER_PATH`: If `paper.jar`, `DiscordLaunchMC.py`, `config.py`, and `languages.py` are in the same directory, you do not need to change this.
1. `JAR_FILE`: If you want to use a different name for the server executable, change this. Otherwise, leave as is.
1. `SCREEN_NAME`: Set the session name for screen. If you run multiple servers, you can set different names in each `config.py`.
1. `MAX_RAM`, `MIN_RAM`: Set according to your computer's specs. The default is for a Raspberry Pi 8GB RAM, so you may need to change this.

Do not change the code below these settings unless you know what you are doing.

### Building the Discord bot
1. Go to https://discord.com/developers/applications, log in, and click "New Application". Name it and create.
1. Click "Bot" on the left, click "Reset Token", confirm, and copy the token. **Paste this token into `TOKEN` in `config.py`.**
1. Turn on all Privileged Gateway Intents and click "Save changes".
1. Click OAuth2 → URL Generator, check `bot` and `applications.commands`, then check `Administrator` in the permissions. (For security, you can set permissions individually, but Administrator is fine if you keep your token safe.)
1. Copy the GENERATED URL at the bottom, open it in your browser, and invite the bot to your Discord server.

## Running the bot
After completing the [Required environment setup](#required-environment-setup) and [Initial configuration](#initial-configuration), you are ready to run the bot.  
Move to the directory containing `DiscordLaunchMC.py` and run:
```shell
python3 DiscordLaunchMC.py
```

## List of available commands
### Commands available to everyone
- `/hello`: Replies with "Hello, [user who executed the command]!" Useful for checking if the bot is working.
<hr>

### Commands available only to Discord server administrators when the server is stopped
- **`/start`**: Starts the server.
<hr>

- `/changeworld`: Change the world to play in. Requires the world name as an argument. Entering a non-existent world name will generate a new world.
- `/setseed`: Specify a seed value. If no argument is specified, a random seed will be used.
- `/setdifficulty`: Change the game difficulty.
- `/setpvp`: Toggle PVP on/off.
- `/sethardcore`: Toggle hardcore mode on/off.
- `/setmaxplayers`: Change the maximum number of players.
- `/setdirectly`: Directly edit a property in server.properties by specifying the property name and value. Use with caution.
- `/searchproperty`: Search for a property in server.properties by part of its name. Also shows the current value.
- `/allowlist`: Add users to the allowlist (`whitelist.json`) by specifying the `user` argument.
- `/listworlds`: Display a list of worlds in the server directory.
<hr>

- `/updatepaper`: Downloads the latest build of PaperMC using the official application. You can download an older version by including the Minecraft version in the `version` argument. If not specified, the latest version available through the API will be downloaded.
- `/updategeyser`: Downloads the latest versions of GeyserMC and its accompanying floodgate to the plugins directory using the official API.
- `/updatesrv`: Downloads the latest version of DiscordSRV to the plugins directory using the Modrinth API.
<hr>

- `/logout`: Stop the bot.

For other settings like game mode (survival, creative, etc.), please use the server console (e.g., via DiscordSRV) while the server is running.  
**Features may be added upon request. Please comment if you have suggestions.**

## Contact information in case of trouble
Twitter (X lol)<br>
https://twitter.com/insane_catt

Please DM me

## License has been changed.
This software was originally released under the MIT License.

Starting from version 1.2.0, it is released under a custom ethical license based on the MIT License.  
This new license prohibits the use of the software for war, discrimination, or harm against vulnerable people.  
Please refer to the `LICENSE` file for details.

### Why the License Change
I believe software should not be used to harm others or support injustice.  
This license reflects my personal stance against war, discrimination, and oppression.

## Version history
- v1.3.1: Added emojis to the command
- v1.3: Added various update commands
- v1.2.3: Improved translation behavior
- v1.2.2: Fixed translation bugs
- v1.2.1: Fixed periodic bot name notification bug and added `listworlds` command, etc.
- v1.2.0: **License change**, updated README, added `/allowlist` command
- v1.1.1: Added functionality to output the bot's name daily, making it easier to identify which bot is running in the console.
- v1.1: Enabled to use English from the `config.py`. Also, implemented `/setmaxplayers`, `/setdirectly` and `/searchproperty` command.
- v1.0.7: Updated README and revised comments
- v1.0.6: Moved simple settings to `config.py`
- v1.0.5: Updated README and separated the English version
- v1.0.4: Updated README
- v1.0.3: Updated README
- v1.0.2: Implemented `/logout` command
- v1.0.1: Slightly changed message when starting server
- v1.0.0