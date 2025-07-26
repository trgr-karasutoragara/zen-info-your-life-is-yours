#!/usr/bin/env python3
"""
45分間隔で現在時刻をGmailで送信するプログラム
"""

import smtplib
import time
from email.mime.text import MIMEText
from datetime import datetime
import logging

# ログ設定（ローテーション付き）
from logging.handlers import RotatingFileHandler
import os

# ホームディレクトリのログファイル
log_file = os.path.expanduser('~/time_notifier.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=2),
        logging.StreamHandler()
    ]
)

# Gmail設定
GMAIL_USER = "your-email@gmail.com"  # ここを変更
GMAIL_APP_PASSWORD = "your-app-password"  # ここを変更
TO_EMAIL = "your-email@gmail.com"  # ここを変更

def send_time_notification():
    """現在時刻をメール送信"""
    try:
        current_time = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        
        # メール作成
        msg = MIMEText(f"""
現在時刻: {current_time}

このメールは45分間隔で自動送信されています。
プログラムは正常に動作中です。
        """.strip())
        
        msg['Subject'] = f'⏰ 定時通知 - {current_time}'
        msg['From'] = GMAIL_USER
        msg['To'] = TO_EMAIL
        
        # Gmail SMTP経由で送信
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        logging.info(f"メール送信成功: {current_time}")
        return True
        
    except Exception as e:
        logging.error(f"メール送信エラー: {e}")
        return False

def main():
    """メインループ"""
    logging.info("45分間隔通知プログラム開始")
    
    # 最初の送信
    send_time_notification()
    
    try:
        while True:
            # 45分待機（2700秒）
            logging.info("45分後に次回送信...")
            time.sleep(2700)
            
            # 次回送信
            send_time_notification()
            
    except KeyboardInterrupt:
        logging.info("プログラム終了（Ctrl+C）")
    except Exception as e:
        logging.error(f"予期しないエラー: {e}")

if __name__ == "__main__":
    main()
