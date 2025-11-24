import express from "express";
import mongoose from "mongoose";
import cors from "cors";

// ========================
// 1) إعداد السيرفر
// ========================
const app = express();
app.use(express.json());
app.use(cors());

// ========================
// 2) المتغيرات من Render
// ========================
const MONGO_URI = process.env.MONGO_URI;
const BOT_API_KEY = process.env.BOT_API_KEY;
const ADMIN_CHAT_ID = process.env.ADMIN_CHAT_ID;

// تأكيد المتغيرات
if (!MONGO_URI  !BOT_API_KEY  !ADMIN_CHAT_ID) {
    console.error("❌ ERROR: One or more environment variables are missing!");
    process.exit(1);
}

// ========================
// 3) الاتصال مع MongoDB
// ========================
mongoose.connect(MONGO_URI)
    .then(() => console.log("✅ Connected to MongoDB Atlas"))
    .catch(err => console.log("❌ MongoDB Error:", err));

// ========================
// 4) Schema الطالب
// ========================
const studentSchema = new mongoose.Schema({
    telegram_id: String,
    full_name: String,
    email: String,
    university_id: String,
    year: String,
    status: { type: String, default: "pending" }
});

const Student = mongoose.model("Student", studentSchema);

// ========================
// 5) API تسجيل طالب جديد
// ========================
app.post("/api/register", async (req, res) => {
    try {
        const { telegram_id, full_name, email, university_id, year } = req.body;

        // التحقق البسيط
        if (!telegram_id  !full_name  !email) {
            return res.status(400).json({ message: "Missing data" });
        }

        // حفظ الطالب
        const newStudent = await Student.create({
            telegram_id,
            full_name,
            email,
            university_id,
            year
        });

        console.log("📩 New student request:", newStudent);

        // إرسال إشعار للمدير عبر بوت التلغرام
        await fetch(https://api.telegram.org/bot${BOT_API_KEY}/sendMessage, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                chat_id: ADMIN_CHAT_ID,
                text: 📥 *طلب تسجيل جديد*\n\n👤 الاسم: ${full_name}\n🎓 السنة: ${year}\n🏷️ ID الجامعي: ${university_id}\n📧 Email: ${email}\n\n/approve_${newStudent._id}  |  /reject_${newStudent._id},
                parse_mode: "Markdown"
            })
        });

        res.json({ message: "Registration request sent" });

    } catch (err) {
        console.log(err);
        res.status(500).json({ message: "Server error" });
    }
});

// ========================
// 6) API موافقة المدير
// ========================
app.get("/admin/approve/:id", async (req, res) => {
    try {
        const id = req.params.id;
        await Student.findByIdAndUpdate(id, { status: "approved" });

        res.send("تم قبول الطالب ✔");
    } catch (err) {
        res.status(500).send("Error");
    }
});

// ========================
// 7) API رفض الطالب
// ========================
app.get("/admin/reject/:id", async (req, res) => {
    try {
        const id = req.params.id;
        await Student.findByIdAndUpdate(id, { status: "rejected" });

        res.send("تم رفض الطلب ❌");
    } catch (err) {
        res.status(500).send("Error");
    }
});

// ========================
// 8) تشغيل السيرفر Render
// ========================
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(🚀 Server running on port ${PORT});
});
