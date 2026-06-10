#!/usr/bin/env python3
"""LaserWeld Pro - Email relay server.
Runs locally, exposed via localhost.run for the live website.
Accepts POST /api/notify, sends email via QQ SMTP.
"""

import json
import smtplib
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from email.mime.text import MIMEText
from email.header import Header

SMTP_HOST = 'smtp.qq.com'
SMTP_PORT = 587
EMAIL_USER = '43288781@qq.com'
EMAIL_PASS = 'rxzacshznprecajg'
NOTIFY_EMAIL = '43288781@qq.com'

class NotifyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
        except:
            self._send_json(400, {'error': 'Invalid JSON'})
            return

        type_ = data.get('type')
        info = data.get('data', {})

        if type_ == 'subscribe':
            subject = '🔔 LaserWeld Pro - 新月度订阅通知'
            text = f'''【激光焊接参数查询软件】月度订阅通知
━━━━━━━━━━━━━━━━━━
订阅时间：{self._now()}
订阅方案：月度订阅 ¥38/月
━━━━━━━━━━━━━━━━━━
联系方式：
  姓名：{info.get('name', '未填写')}
  电话：{info.get('phone', '未填写')}
  公司：{info.get('company', '未填写')}
  备注：{info.get('note', '无')}
━━━━━━━━━━━━━━━━━━
请安排人员对接线下打样服务。'''
        elif type_ == 'contact':
            subject = '📝 LaserWeld Pro - 打样需求留言'
            text = f'''【激光焊接参数查询软件】打样需求提交
━━━━━━━━━━━━━━━━━━
提交时间：{self._now()}
━━━━━━━━━━━━━━━━━━
  姓名：{info.get('name', '未填写')}
  电话：{info.get('phone', '未填写')}
  公司：{info.get('company', '未填写')}
  需求描述：{info.get('note', '无')}
━━━━━━━━━━━━━━━━━━
请尽快联系客户确认打样细节。'''
        else:
            subject = '🔔 LaserWeld Pro - 通知'
            text = f'未知通知类型: {type_}\n数据: {json.dumps(info, ensure_ascii=False)}'

        try:
            msg = MIMEText(text, 'plain', 'utf-8')
            msg['From'] = f'"LaserWeld Pro" <{EMAIL_USER}>'
            msg['To'] = NOTIFY_EMAIL
            msg['Subject'] = Header(subject, 'utf-8')

            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            server.quit()

            print(f'✅ Email sent: {type_}', flush=True)
            self._send_json(200, {'ok': True})
        except Exception as e:
            print(f'❌ Email failed: {e}', flush=True)
            self._send_json(500, {'error': str(e)})

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'LaserWeld Pro Email Relay running.')

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def _now(self):
        from datetime import datetime, timezone, timedelta
        tz = timezone(timedelta(hours=8))
        return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    def log_message(self, format, *args):
        print(f'[{self._now()}] {args[0]} {args[1]} {args[2]}', flush=True)

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
    server = HTTPServer(('0.0.0.0', port), NotifyHandler)
    print(f'🚀 Email relay listening on port {port}', flush=True)
    print(f'    POST /api/notify  →  sends email via QQ SMTP', flush=True)
    print(f'    Expose via: ssh -R 80:localhost:{port} nokey@localhost.run', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down...', flush=True)
        server.server_close()

if __name__ == '__main__':
    main()
