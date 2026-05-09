import { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import logo from "@/assets/uj-logo.jpg";
import { MAJOR_MAP, MajorCode } from "@/types";

interface WelcomeScreenProps {
  onSubmit: (id: string, majorCode: MajorCode) => void;
}

export default function WelcomeScreen({ onSubmit }: WelcomeScreenProps) {
  const [id, setId] = useState("");
  const [majorCode, setMajorCode] = useState<string>("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!/^\d{7}$/.test(id)) {
      alert("الرقم الجامعي يجب أن يكون 7 أرقام فقط");
      return;
    }

    if (!Object.keys(MAJOR_MAP).includes(majorCode)) {
      alert("اختر تخصص صحيح");
      return;
    }

    onSubmit(id, majorCode as MajorCode);
  };

  return (
    <div className="relative min-h-screen overflow-hidden gradient-bg">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute top-20 right-20 w-64 h-64 bg-white/5 rounded-full blur-3xl"
          animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.5, 0.3] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute bottom-20 left-20 w-96 h-96 bg-white/5 rounded-full blur-3xl"
          animate={{ scale: [1.2, 1, 1.2], opacity: [0.2, 0.4, 0.2] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>

      {/* ── DESKTOP layout: side by side ── */}
      <div className="hidden lg:flex items-center justify-between min-h-screen px-8 xl:px-16 relative z-10">

        {/* LEFT PANEL */}
        <motion.div
          initial={{ opacity: 0, x: -40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.6, ease: "easeOut" }}
          className="flex flex-col w-[200px] xl:w-[240px] shrink-0 text-white"
        >
          <h2 className="text-2xl font-bold mb-4">عن المشروع</h2>
          <p className="text-white/80 text-base leading-relaxed text-right">
            دليلك هو مساعد أكاديمي ذكي يعتمد على تقنيات الذكاء الاصطناعي
            لمساعدة طلاب كلية علوم وهندسة الحاسب في جامعة جدة.
            يمكنه الإجابة عن الأسئلة المتعلقة بالمقررات، المتطلبات،
            التدريب الصيفي، الشهادات المهنية، والأنشطة الطلابية.
          </p>
        </motion.div>

        {/* CENTER CARD */}
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="flex-1 flex justify-center"
        >
          <div className="w-full max-w-[500px] p-10 rounded-3xl glass-card shadow-2xl">
            <motion.img
              src={logo}
              alt="University of Jeddah Logo"
              className="w-64 mx-auto mb-8 rounded-2xl shadow-lg border-2 border-white/30"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
            />
            <div className="text-center mb-8">
              <h1 className="text-2xl font-bold text-white mb-3 px-2">
                مرحباً بك في <i>دليلك</i><br />مرشدك الأكاديمي الذكي
              </h1>
              <p className="text-white/80 text-lg">فضلاً أدخل بياناتك للمتابعة</p>
            </div>
            <form onSubmit={handleSubmit} className="space-y-6">
              <Input
                type="text"
                placeholder="ادخل رقمك الجامعي (7 أرقام)"
                value={id}
                onChange={(e) => setId(e.target.value)}
                maxLength={7}
                className="glass-input text-white placeholder:text-white/60 text-lg h-14 text-right border-white/30 focus:border-white/50 transition-all"
              />
              <Select value={majorCode} onValueChange={setMajorCode}>
                <SelectTrigger className="glass-input text-white h-14 text-lg text-right border-white/30 focus:border-white/50">
                  <SelectValue placeholder="اختر تخصصك" />
                </SelectTrigger>
                <SelectContent className="bg-white/95 backdrop-blur-md">
                  {Object.entries(MAJOR_MAP).map(([code, label]) => {
                    const isAvailable = ["cs", "ai", "ds", "cy", "sw", "ce"].includes(code);
                    return (
                      <SelectItem
                        key={code}
                        value={code}
                        disabled={!isAvailable}
                        className={`text-right text-lg ${isAvailable ? "cursor-pointer hover:bg-primary/10" : "opacity-50 cursor-not-allowed"}`}
                      >
                        {label}
                      </SelectItem>
                    );
                  })}
                </SelectContent>
              </Select>
              <Button
                type="submit"
                disabled={!majorCode}
                className="w-full h-14 text-lg font-bold bg-primary hover:bg-primary-light transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                دخول
              </Button>
            </form>
          </div>
        </motion.div>

        {/* RIGHT PANEL */}
        <motion.div
          initial={{ opacity: 0, x: 40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.6, ease: "easeOut" }}
          className="flex flex-col w-[180px] xl:w-[200px] shrink-0 text-white text-right"
        >
          <h2 className="text-2xl font-bold mb-4">فريق المشروع</h2>
          <ul className="space-y-2 text-white/80 text-lg">
            <li>المشرف: عبد الله الغامدي</li>
            <li>سلطان بازهير</li>
            <li>فواز الشمري</li>
            <li>يزن الأنصاري</li>
            <li>سعد الشهري</li>
            <li>أمير الزهراني</li>
          </ul>
        </motion.div>
      </div>

      {/* ── MOBILE layout: stacked ── */}
      <div className="flex lg:hidden flex-col items-center min-h-screen px-4 py-10 gap-8 relative z-10">

        {/* CENTER CARD */}
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="w-full max-w-[500px] p-6 rounded-3xl glass-card shadow-2xl"
        >
          <motion.img
            src={logo}
            alt="University of Jeddah Logo"
            className="w-48 mx-auto mb-6 rounded-2xl shadow-lg border-2 border-white/30"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          />
          <div className="text-center mb-6">
            <h1 className="text-xl font-bold text-white mb-2 px-2">
              مرحباً بك في <i>دليلك</i><br />مرشدك الأكاديمي الذكي
            </h1>
            <p className="text-white/80 text-base">فضلاً أدخل بياناتك للمتابعة</p>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              type="text"
              placeholder="ادخل رقمك الجامعي (7 أرقام)"
              value={id}
              onChange={(e) => setId(e.target.value)}
              maxLength={7}
              className="glass-input text-white placeholder:text-white/60 text-base h-12 text-right border-white/30 focus:border-white/50 transition-all"
            />
            <Select value={majorCode} onValueChange={setMajorCode}>
              <SelectTrigger className="glass-input text-white h-12 text-base text-right border-white/30 focus:border-white/50">
                <SelectValue placeholder="اختر تخصصك" />
              </SelectTrigger>
              <SelectContent className="bg-white/95 backdrop-blur-md">
                {Object.entries(MAJOR_MAP).map(([code, label]) => {
                  const isAvailable = ["cs", "ai"].includes(code);
                  return (
                    <SelectItem
                      key={code}
                      value={code}
                      disabled={!isAvailable}
                      className={`text-right text-base ${isAvailable ? "cursor-pointer hover:bg-primary/10" : "opacity-50 cursor-not-allowed"}`}
                    >
                      {label}
                    </SelectItem>
                  );
                })}
              </SelectContent>
            </Select>
            <Button
              type="submit"
              disabled={!majorCode}
              className="w-full h-12 text-base font-bold bg-primary hover:bg-primary-light transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              دخول
            </Button>
          </form>
        </motion.div>

        {/* BOTTOM ROW: description + team side by side */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
          className="w-full max-w-[500px] flex flex-row gap-6 text-white pb-6"
        >
          {/* Description */}
          <div className="flex-1 text-right">
            <h2 className="text-lg font-bold mb-2">عن المشروع</h2>
            <p className="text-white/80 text-sm leading-relaxed">
              دليلك هو مساعد أكاديمي ذكي يعتمد على تقنيات الذكاء الاصطناعي
              لمساعدة طلاب علوم الحاسب والذكاء الاصطناعي في جامعة جدة.
            </p>
          </div>

          {/* Divider */}
          <div className="w-px bg-white/20 self-stretch" />

          {/* Team */}
          <div className="flex-1 text-right">
            <h2 className="text-lg font-bold mb-2">فريق المشروع</h2>
            <ul className="space-y-1 text-white/80 text-sm">
            <li>المشرف: عبد الله الغامدي</li>
              <li>سلطان بازهير</li>
              <li>فواز الشمري</li>
              <li>يزن الأنصاري</li>
              <li>سعد الشهري</li>
              <li>أمير الزهراني</li>
            </ul>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
