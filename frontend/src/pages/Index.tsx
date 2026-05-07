import { useState, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import Cookies from "js-cookie";
import WelcomeScreen from "@/components/WelcomeScreen";
import ChatBox from "@/components/ChatBox";
import { MajorCode } from "@/types";

export default function Index() {
  const [studentId, setStudentId] = useState<string | null>(null);
  const [major, setMajor] = useState<MajorCode | null>(null);

  useEffect(() => {
    const savedId = Cookies.get("uj_student_id");
    const savedMajor = Cookies.get("uj_major") as MajorCode | undefined;

    if (savedId && savedMajor) {
      setStudentId(savedId);
      setMajor(savedMajor);
    }
  }, []);

  const handleLogin = (id: string, majorCode: MajorCode) => {
    Cookies.set("uj_student_id", id, { expires: 30 });
    Cookies.set("uj_major", majorCode, { expires: 30 });
    setStudentId(id);
    setMajor(majorCode);
  };

  const handleLogout = () => {
    setStudentId(null);
    setMajor(null);
    Cookies.remove("uj_student_id");
    Cookies.remove("uj_major");
  };

  return (
    <div className="h-screen w-screen overflow-hidden">
      <AnimatePresence mode="wait">
        {studentId && major ? (
          <motion.div
            key="chatbox"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.4, ease: "easeInOut" }}
            className="h-full"
          >
            <ChatBox studentId={studentId} major={major} onLogout={handleLogout} />
          </motion.div>
        ) : (
          <motion.div
            key="welcome"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.4, ease: "easeInOut" }}
            className="h-full"
          >
            <WelcomeScreen onSubmit={handleLogin} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
