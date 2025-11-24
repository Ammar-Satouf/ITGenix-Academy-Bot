require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ObjectId } = require('mongodb');
const TelegramBot = require('node-telegram-bot-api');
const crypto = require('crypto');
const cors = require('cors');

const BOT_TOKEN = process.env.BOT_TOKEN;
const MONGODB_URI = process.env.MONGODB_URI;
const ADMIN_ID = process.env.ADMIN_TELEGRAM_ID;
const WEBAPP_URL = process.env.WEBAPP_URL;
const PORT = process.env.PORT || 3000;

if (!BOT_TOKEN  !MONGODB_URI  !ADMIN_ID || !WEBAPP_URL) {
  console.error("Please set BOT_TOKEN, MONGODB_URI, ADMIN_TELEGRAM_ID and WEBAPP_URL in .env");
  process.exit(1);
}

const bot = new TelegramBot(BOT_TOKEN, { polling: true });
const app = express();
app.use(bodyParser.json());
app.use(cors({
  origin: true,
  credentials: true
}));

let db, studentsCollection;

async function initDb() {
  const client = new MongoClient(MONGODB_URI);
  await client.connect();
  db = client.db(); // uses DB from URI or default
  studentsCollection = db.collection('students');
  console.log("Connected to MongoDB");
}

function verifyTelegramInitData(initData, botToken) {
  // initData: string from Telegram WebApp (window.Telegram.WebApp.initData)
  // verification according to Telegram docs
  const params = {};
  initData.split('&').forEach(pair => {
    const [k, v] = pair.split('=');
    params[k] = decodeURIComponent(v || '');
  });

  const hash = params.hash;
  delete params.hash;

  // build data_check_string
  const keys = Object.keys(params).sort();
  const data_check_arr = keys.map(k => ${k}=${params[k]});
  const data_check_string = data_check_arr.join('\n');

  const secret = crypto.createHash('sha256').update(botToken).digest();
  const hmac = crypto.createHmac('sha256', secret).update(data_check_string).digest('hex');

  return hmac === hash;
}

// -------------------- Endpoint to receive signup from WebApp --------------------
app.post('/api/signup', async (req, res) => {
  try {
    const { form, initData } = req.body;
    // form: { name, year, email, universityId, phone }
    // initData: window.Telegram.WebApp.initData (string)
    if (!form || !initData) return res.status(400).json({ error: 'missing form or initData' });

    // verify initData
    const verified = verifyTelegramInitData(initData, BOT_TOKEN);
    if (!verified) {
      return res.status(403).json({ error: 'invalid initData' });
    }

    // parse initData to get telegram_id (user)
    const parts = {};
    initData.split('&').forEach(p => {
      const [k, v] = p.split('=');
      parts[k] = decodeURIComponent(v || '');
    });
    // initData might contain user info in user param as JSON or other fields depending on the WebApp usage.
    // Safer approach: Telegram provides user object inside WebApp.initDataUnsafe on client side.
    // Here we expect the frontend to also send telegram_id inside form (recommended).
    const telegram_id = form.telegram_id || parts.user ? JSON.parse(parts.user).id : null;

    // Create a student doc
    const studentDoc = {
      telegram_id: telegram_id || null,
      name: form.name || '',
      year: form.year || '',
      email: form.email || '',
      university_id: form.universityId || '',
      phone: form.phone || '',
      status: 'pending',
      created_at: new Date()
    };

    const result = await studentsCollection.insertOne(studentDoc);

    // Notify admin inside the bot with Approve/Reject inline buttons
    const studentId = result.insertedId.toString();
    const message = 🆕 طلب تسجيل جديد\n\nاسم: ${studentDoc.name}\nسنة: ${studentDoc.year}\nإيميل: ${studentDoc.email}\nرقم جامعي: ${studentDoc.university_id}\nTelegram ID: ${studentDoc.telegram_id || 'غير مرتبط'}\n\nID: ${studentId};

    const opts = {
      reply_markup: {
        inline_keyboard: [
          [{ text: '✅ قبول', callback_data: approve:${studentId} }, { text: '❌ رفض', callback_data: reject:${studentId} }]
        ]
      }
    };

    await bot.sendMessage(ADMIN_ID, message, opts);
