# 45分ごとにメールで時刻をお知らせする仕組み

メールだと、返信することでログ（その時、してることなど）を記録できるので。メールで一元管理したい方向け。

<br>

## 使い方

Pythonスクリプトをsystemdで常駐させます。

<br>

## 設定

`sudo nano /etc/systemd/system/time-notifier.service`

<br>

```
[Unit]
Description=Time Notifier Service
After=network.target

[Service]
Type=simple
User=YOUR-USER-NAME
WorkingDirectory=/home/YOUR-USER-NAME
ExecStart=/usr/bin/python3 /home/YOUR-USER-NAME/time_notifier.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

<br>

## 適用と正常動作確認

### サービス再読み込み
`sudo systemctl daemon-reload`

### 開始
`sudo systemctl start time-notifier`

### 確認
`sudo systemctl status time-notifier`
　
### ログ確認
`sudo journalctl -u time-notifier -f`

### ログファイル確認
`tail -f ~/time_notifier.log`

<br>

## 哲学、制作背景
没頭というか集中し過ぎることや、調べ物に時間がかかるなどするので、時間管理をしたいことと、家庭内サーバーあるのだから自動化も試したかったので。

<br>

## License

MIT License

<br>


## Repository Policy

- I develop prototypes with a focus on ethics.
- There are no plans for maintenance or support.
- The project is released under the MIT License, so feel free to modify it within the scope of the license.
- Instead of providing support, I create new prototypes to solve emerging problems.

<br>

## Author Declaration

I am an independent volunteer with no conflicts of interest.


