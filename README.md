# DiscordLaunchMC
MinecraftサーバーをDiscordから起動するツールです。<br>
If you need an English version: https://github.com/insane-catt/DiscordLaunchMC-en
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
図2：Minecraftサーバーに直接コマンドを打つことが可能なコンソール画面。
seedコマンドとかも普通に使える。
PaperLaunchBotというのが、今回自作したbot。

- **screen**：Minecraftサーバーをバックグラウンドで動作させ、またそれに自由に接続・切断することを可能にするソフト。以下のコマンドをターミナルで実行し、インストールできる。
```shell
sudo apt install screen -y
```
## 使い方
**PaperでのMinecraftサーバーは既に構築された状態を想定しています。** まずそれだけやって、それから以下のようにしてください。
1. 画面右のRelasesよりパッケージをダウンロードする。
1. パッケージ内のDiscordLaunchMC.pyとconfig.pyをサーバーの実行ファイルのあるディレクトリに移動し、config.pyをエディタで開く。
1. 設定欄を任意で書き換えるか、ディレクトリ構成を「/home/pi/minecraft/java/paper」にし、そのpaperディレクトリをサーバーの実行ファイルのあるフォルダにする。
1. https://discord.com/developers/applications にアクセスし、ログインし、New Applicationボタンをクリック。名前を付け、チェックを入れ、Createする。
1. 画面左にBotと出るので、クリックし、Reset Tokenボタンを押し、Yes, do it!をクリック、その後Copyボタンを押して**トークンをconfig.py内の「TOKEN」と置き換える。**
1. Privileged Gateway Intentsのところの切り替えスイッチを全部オンにし、下に出てきたSave changesボタンをクリック。
1. 画面左のOAuth2→URL Generatorとクリックし、大量のチェックボックスの中からbot、applications.commandsにチェックを入れる。その後、下にまた出てきた大量のチェックボックスの中から、もうめんどくさいのでAdministrator（管理者って意味）をクリック。（セキュリティー的に怖かったらいちいち設定する必要があるけど攻撃されるかもとか思わなければ管理者でいいと思う、自分のbotだしトークンを人に教えたり流出しなければいい。）
1. 一番下に出たGENERATED URLをコピーしてブラウザで開き、botをDiscordサーバーに招待する。
1. 以下のコマンドで実行する。
```shell
python3 DiscordLaunchMC.py
```

## 使えるコマンド一覧
### いつでも使えるコマンド
- /hello：Hello, 【コマンドを実行したユーザー】!と返してくれる。誰でも使えるコマンド。botの動作確認などに使用できる。
### サーバー停止中にDiscordサーバー管理者のみ使えるコマンド
- **/start**：サーバーを起動するコマンド。
- /changeworld：遊ぶワールドを変更する。引数として、ワールド名を入力する必要がある。存在しないワールド名を入力することで、新しいワールドが生成される。
- /setseed：シード値を指定する。引数を指定しなかった場合、ランダムなシード値にする。
- /setdifficulty：ゲーム難易度を引数で変更する。
- /setpvp：PVPのオンオフを引数で指定する。
- /logout：Botを停止させる。

その他、ゲームモード（サバイバルとかクリエイティブとか）だったりはサーバー起動中にSRVとかのコンソールとかに入力してください。**気が向いたり要望があれば機能追加します。コメントください。**

## 上手くいかない場合の連絡先
Twitter（X笑）
https://twitter.com/insane_catt

DMまでどうぞ

## バージョン履歴
- v1.0.7：README更新とコメントの修正
- v1.0.6：簡単な設定をconfig.pyに移動
- v1.0.5：READMEの更新、ENバージョンの分離
- v1.0.4：READMEの更新
- v1.0.3：READMEの更新
- v1.0.2：/logoutコマンドの実装
- v1.0.1：サーバーを起動する際のメッセージ若干変更
- v1.0.0