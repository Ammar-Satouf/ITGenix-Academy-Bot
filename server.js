const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const TelegramBot = require('node-telegram-bot-api');

const app = express();
app.use(cors());
app.use(express.json());

// ⚙️ المتغيرات من Render Environment
const MONGO_URI = process.env.MONGO_URI;
const BOT_TOKEN = process.env.BOT_TOKEN;
const ADMIN_CHAT_ID = process.env.ADMIN_CHAT_ID;

// 🔗 ربط MongoDB
mongoose.connect(MONGO_URI)
  .then(() => console.log('✅ Connected to MongoDB'))
  .catch(err => console.error('❌ MongoDB connection error:', err));

// 🎓 نموذج الطالب
const studentSchema = new mongoose.Schema({
  telegram_id: { type: String, required: true },
  full_name: { type: String, required: true },
  email: { type: String, required: true },
  university_id: { type: String, required: true },
  year: { type: String, required: true },
  status: { type: String, default: 'pending' },
  registered_at: { type: Date, default: Date.now }
});

const Student = mongoose.model('Student', studentSchema);

// 🤖 تهيئة البوت
const bot = new TelegramBot(BOT_TOKEN, { polling: false });

// 📍 مسار تسجيل الطالب
app.post('/api/register', async (req, res) => {
  try {
    const { telegram_id, full_name, email, university_id, year } = req.body;

    // التحقق من البيانات
    if (!telegram_id || !full_name || !email || !university_id || !year) {
      return res.status(400).json({ error: 'جميع الحقول مطلوبة' });
    }

    // حفظ الطالب في قاعدة البيانات
    const newStudent = new Student({
      telegram_id,
      full_name,
      email,
      university_id,
      year,
      status: 'pending'
    });

    await newStudent.save();

    // 📨 إرسال إشعار للمدير
    const message = `
🎓 **طلب تسجيل جديد**

👤 الاسم: ${full_name}
📧 البريد: ${email}
🎯 الرقم الجامعي: ${university_id}
📅 السنة: ${year}

✅ /approve_${newStudent._id}
❌ /reject_${newStudent._id}
    `;

    await bot.sendMessage(ADMIN_CHAT_ID, message, { parse_mode: 'Markdown' });

    res.json({ 
      success: true, 
      message: 'تم تسجيل طلبك بنجاح، سيتم المراجعة قريباً',
      student_id: newStudent._id 
    });

  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'حدث خطأ أثناء التسجيل' });
  }
});

// ✅ مسار الموافقة على الطالب
app.get('/admin/approve/:id', async (req, res) => {
  try {
    const studentId = req.params.id;
    
    const student = await Student.findByIdAndUpdate(
      studentId,
      { status: 'approved' },
      { new: true }
    );

    if (!student) {
      return res.status(404).json({ error: 'الطالب غير موجود' });
    }

    // إرسال رسالة تأكيد للمدير
    await bot.sendMessage(
      ADMIN_CHAT_ID, 
      `✅ تم الموافقة على طلب ${student.full_name}`
    );

    res.json({ 
      success: true, 
      message: `تم الموافقة على ${student.full_name}` 
    });

  } catch (error) {
    res.status(500).json({ error: 'حدث خطأ أثناء الموافقة' });
  }
});

// ❌ مسار رفض الطالب
app.get('/admin/reject/:id', async (req, res) => {
  try {
    const studentId = req.params.id;
    
    const student = await Student.findByIdAndUpdate(
      studentId,
      { status: 'rejected' },
      { new: true }
    );

    if (!student) {
      return res.status(404).json({ error: 'الطالب غير موجود' });
    }

    await bot.sendMessage(
      ADMIN_CHAT_ID, 
      `❌ تم رفض طلب ${student.full_name}`
    );

    res.json({ 
      success: true, 
      message: `تم رفض طلب ${student.full_name}` 
    });

  } catch (error) {
    res.status(500).json({ error: 'حدث خطأ أثناء الرفض' });
  }
});

// 📊 مسار الحصول على حالة الطالب
app.get('/api/status/:telegram_id', async (req, res) => {
  try {
    const student = await Student.findOne({ 
      telegram_id: req.params.telegram_id 
    });

    if (!student) {
      return res.status(404).json({ error: 'لم يتم العثور على سجل لك' });
    }

    res.json({
      full_name: student.full_name,
      status: student.status,
      registered_at: student.registered_at
    });

  } catch (error) {
    res.status(500).json({ error: 'حدث خطأ أثناء جلب البيانات' });
  }
});

// 🏠 مسار الأساس
app.get('/', (req, res) => {
  res.json({ 
    message: 'Student Registration API is running!',
    version: '1.0.0'
  });
});

// 🚀 تشغيل السيرفر
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
