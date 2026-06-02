// LaserWeld Pro - 通知转发 API
// Vercel Serverless Function
// 用途：月度订阅 / 打样需求 → 邮件通知 Louis

const SMTP_HOST = 'smtp.qq.com';
const SMTP_PORT = 587;
const EMAIL_USER = process.env.EMAIL_USER || '43288781@qq.com';
const EMAIL_PASS = process.env.EMAIL_PASS;
const NOTIFY_EMAIL = process.env.NOTIFY_EMAIL || '43288781@qq.com';

export default async function handler(req, res) {
  // CORS
  const origin = req.headers.origin || '';
  const allowedOrigins = [
    'https://laserweld-pro-rkmikgiv.edgeone.cool',
    'https://laserweld-pro.vercel.app',
    'http://localhost:8080',
    'http://localhost:3000',
  ];
  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { type, data } = req.body;
  if (!type || !data) {
    return res.status(400).json({ error: 'Missing type or data' });
  }

  // Validate email credentials
  if (!EMAIL_PASS) {
    console.error('EMAIL_PASS not set in environment variables');
    return res.status(500).json({ error: 'Email service not configured' });
  }

  try {
    let subject, text;

    if (type === 'subscribe') {
      subject = `🔔 LaserWeld Pro - 新月度订阅通知`;
      text = `【激光焊接参数查询软件】月度订阅通知
━━━━━━━━━━━━━━━━━━
订阅时间：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
订阅方案：月度订阅 ¥38/月
━━━━━━━━━━━━━━━━━━
联系方式：
  姓名：${data.name || '未填写'}
  电话：${data.phone || '未填写'}
  公司：${data.company || '未填写'}
  备注：${data.note || '无'}
━━━━━━━━━━━━━━━━━━
请安排人员对接线下打样服务。`;
    } else if (type === 'contact') {
      subject = `📝 LaserWeld Pro - 打样需求留言`;
      text = `【激光焊接参数查询软件】打样需求提交
━━━━━━━━━━━━━━━━━━
提交时间：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
━━━━━━━━━━━━━━━━━━
  姓名：${data.name || '未填写'}
  电话：${data.phone || '未填写'}
  公司：${data.company || '未填写'}
  需求描述：${data.note || '无'}
━━━━━━━━━━━━━━━━━━
请尽快联系客户确认打样细节。`;
    } else {
      return res.status(400).json({ error: 'Invalid type' });
    }

    // Send email via nodemailer or direct SMTP
    const nodemailer = await import('nodemailer');
    const transporter = nodemailer.default.createTransport({
      host: SMTP_HOST,
      port: SMTP_PORT,
      secure: false,
      auth: { user: EMAIL_USER, pass: EMAIL_PASS },
    });

    await transporter.sendMail({
      from: `"LaserWeld Pro" <${EMAIL_USER}>`,
      to: NOTIFY_EMAIL,
      subject,
      text,
    });

    console.log(`Email sent: ${type}`);
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Email send error:', err);
    return res.status(500).json({ error: 'Failed to send notification' });
  }
}
