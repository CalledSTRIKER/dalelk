import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, LogOut } from "lucide-react";
import logo from "@/assets/uj-logo.jpg";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import ChatMessage from "./ChatMessage";
import { MAJOR_MAP, MajorCode, Message, Suggestion } from "@/types";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/use-toast";

interface ChatBoxProps {
  studentId: string;
  major: MajorCode;
  onLogout: () => void;
}
const suggestionsByMajor: Record<MajorCode, Suggestion[]> = {
cs: [
{ text: "ما هو المتطلب السابق لمقرر نظم التشغيل ؟", label: "📘 متطلب مقرر نظم التشغيل " },
{ text: "هل يوجد شهادات احترافية لتخصص الأمن السيبراني؟", label: "📜 الشهادات الإحترافية" },
{ text: "ما الفرق بين التدريب الصيفي والتعاوني؟", label: "💬 استفسار عام" }
],
ai: [
{ text: "ما هو رمز مقرر أساسيات الذكاء الإصطناعي؟", label: "📘 رمز مقرر أساسيات الذكاء الإصطناعي" },
{ text: "ما هي الشهادات المطلوبة في مجال الذكاء الاصطناعي؟", label: "📜 الشهادات الإحترافية" },
{ text: "ما هي مدة التدريب الصيفي؟", label: "💬 استفسار عام" }
],
ds: [
{ text: "ما هو رمز مقرر مستودعات البيانات", label: "📘 رمز مقرر مستودعات البيانات" },
{ text: "ما هي الشهادات المطلوبة في علوم البيانات؟", label: "📜 الشهادات الإحترافية" },
{ text: "كيف أتعلم تحليل البيانات؟", label: "💬 استفسار عام" }
],
cy: [
{ text: "ما هو رمز مقرر أساسيات الامن السيبراني", label: "📘 رمز مقرر أساسيات الأمن السيبراني" },
{ text: "ما هي الشهادات المهمة في الأمن السيبراني؟", label: "📜 الشهادات الإحترافية" },
{ text: "كيف أبدأ في مجال الاختراق الأخلاقي؟", label: "💬 استفسار عام" }
],
sw: [
{ text: "كم عدد عدد ساعات مقرر تفاعل الانسان و الحاسب", label: "📘 عدد ساعات مقرر تفاعل الانسان و الحاسب" },
{ text: "ما هي الشهادات المطلوبة في هندسة البرمجيات؟", label: "📜 الشهادات الإحترافية" },
{ text: "كيف أتعلم تطوير التطبيقات؟", label: "💬 استفسار عام" }
],
ce: [
{ text: "ما هي مواد المستوى العاشر لهندسة الحاسب؟", label: "📘 مواد المستوى العاشر" },
{ text: "ما هي أهم شهادات الشبكات؟", label: "📜 الشهادات الإحترافية" },
{ text: "كيف أتعلم هندسة الشبكات؟", label: "💬 استفسار عام" }
]
};

export default function ChatBox({ studentId, major, onLogout }: ChatBoxProps) {
  const chatEndRef = useRef<HTMLDivElement>(null);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const { toast } = useToast();
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: "ai",
      text:`مرحبًا، أنا مرشدك الأكاديمي الذكي، ويسعدني دعم مسيرتك في تخصص **${MAJOR_MAP[major]}**.`,
      timestamp: new Date(),
      animate: null,
      currentFeedback: null
    }
  ]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const hostname = window.location.hostname;
  const [blockedMessage, setBlockedMessage] = useState<string | null>(null);

  const handleSend = async (text?: string) => {
    const messageText = text || input.trim();
    if (!messageText) return;

    setShowSuggestions(false);
    const userMessage: Message = { sender: "user", text: messageText, timestamp: new Date() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await fetch(`http://${hostname}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ question: messageText }),
      });
      const data = await response.json();
      let aiMessage: Message = {} as Message

      
    
      if (!response.ok) {
        if (response.status == 429)
        {

            aiMessage = {
                sender: "ai",
                text: data.detail,
                timestamp: new Date(),
                animate: null,
                response_time: data.response_time,
                question: messageText,
                question_id: data.question_id,
                currentFeedback: null
              };

        }

        else if(response.status == 403){
            setBlockedMessage(data.detail);
            setIsTyping(false);
            return;

        }

        else
          {
        throw new Error('فشل الحصول على الرد');
        }
      }

      else{

          aiMessage = {
            sender: "ai",
            text: data.answer || "عذراً، حدث خطأ في الحصول على الرد.",
            timestamp: new Date(),
            animate: null,
            response_time: data.response_time,
            question: messageText,
            question_id: data.question_id,
            currentFeedback: null
          };

    }
      
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      toast({
        title: "خطأ",
        description: "فشل الاتصال بالخادم",
        variant: "destructive",
      });
      
      const errorMessage: Message = {
        sender: "ai",
        text: "عذراً، حدث خطأ في الاتصال. يرجى المحاولة مرة أخرى.",
        timestamp: new Date(),
        animate: null,
        currentFeedback: null
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleFeedback = async (messageIndex: number, positive: boolean) => {
    const message = messages[messageIndex];
    const newFeedback = positive ? 'good' : 'bad';
    
    setMessages((prev) =>
      prev.map((msg, idx) =>
        idx === messageIndex
          ? { ...msg, currentFeedback: newFeedback, animate: positive ? "thumbUp" : "thumbDown" }
          : msg
      )
    );

    try {
      const response = await fetch(`http://${hostname}/api/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          question: message.question,
          answer: message.text,
          feedback: newFeedback,
          response_time: message.response_time,
          question_id: message.question_id
        }),
      });

      if (!response.ok) {

        if(response.status == 403){
            const data = await response.json();

            setBlockedMessage(data.detail);
            setIsTyping(false);
            return;

        }
        throw new Error('فشل إرسال التقييم');
      }

      toast({
        title: "شكراً لك",
        description: "تم إرسال تقييمك بنجاح",
      });
    } catch (error) {
      toast({
        title: "خطأ",
        description: "فشل إرسال التقييم",
        variant: "destructive",
      });
      setMessages((prev) =>
        prev.map((msg, idx) =>
          idx === messageIndex ? { ...msg, currentFeedback: null, animate: null } : msg
        )
      );
    }

    setTimeout(() => {
      setMessages((prev) =>
        prev.map((msg, idx) =>
          idx === messageIndex ? { ...msg, animate: null } : msg
        )
      );
    }, 400);
  };

  if (blockedMessage) {
  return (
    <div className="h-screen w-screen flex items-center justify-center bg-white text-black" dir="ltr">
      {blockedMessage}
    </div>
  );
}

  

  return (
    <div className="flex flex-col h-screen gradient-bg">
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between p-3 sm:p-5 glass-card border-b border-white/20"
      >
        <Button
          onClick={onLogout}
          variant="destructive"
          size="sm"
          className="gap-2 shadow-md"
        >
          <LogOut className="w-4 h-4" />
          تسجيل خروج
        </Button>
        
        <div className="flex items-center gap-2 sm:gap-3">
          <div className="text-right">
            <h2 className="text-lg sm:text-xl font-bold text-white">
              المرشد الأكاديمي الذكي
            </h2>
            <p className="text-xs sm:text-sm text-white/70">
              {MAJOR_MAP[major]} • {studentId}
            </p>
          </div>
          <img 
            src={logo} 
            alt="University of Jeddah Logo" 
            className="w-16 h-12 sm:w-20 sm:h-14 rounded-lg border-2 border-white/30 shadow-md"
          />
        </div>
      </motion.header>

      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
        <AnimatePresence>
          {messages.map((msg, idx) => (
            <ChatMessage
              key={idx}
              message={msg}
              onFeedback={(positive) => handleFeedback(idx, positive)}
            />
          ))}
        </AnimatePresence>

        {isTyping && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2 text-white/70 text-sm px-5"
          >
            <div className="flex gap-1">
              <motion.div
                className="w-2 h-2 bg-white/50 rounded-full"
                animate={{ scale: [1, 1.5, 1] }}
                transition={{ duration: 1, repeat: Infinity, delay: 0 }}
              />
              <motion.div
                className="w-2 h-2 bg-white/50 rounded-full"
                animate={{ scale: [1, 1.5, 1] }}
                transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
              />
              <motion.div
                className="w-2 h-2 bg-white/50 rounded-full"
                animate={{ scale: [1, 1.5, 1] }}
                transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
              />
            </div>
            <span>المرشد يكتب...</span>
          </motion.div>
        )}

        {showSuggestions && messages.length === 1 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="space-y-3 mt-6"
          >
            <p className="text-white/80 text-sm text-center mb-4">جرب إحدى هذه الأسئلة:</p>
            {suggestionsByMajor[major].map((suggestion, idx) => (
              <motion.button
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 + idx * 0.1 }}
                onClick={() => handleSend(suggestion.text)}
                className="w-full p-4 text-right glass-card hover:bg-white/20 transition-all duration-300 rounded-xl shadow-md hover:shadow-lg hover:scale-[1.02] text-white"
              >
                {suggestion.label}
              </motion.button>
            ))}
          </motion.div>
        )}

        <div ref={chatEndRef} />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="p-4 glass-card border-t border-white/20"
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex gap-3"
        >
          <Button
            type="submit"
            size="lg"
            disabled={!input.trim() || isTyping}
            className="bg-accent hover:bg-accent/90 shadow-lg hover:shadow-xl transition-all duration-300"
          >
            <Send className="w-5 h-5" />
          </Button>
          
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="اكتب سؤالك هنا..."
            disabled={isTyping}
            className="flex-1 glass-input text-white placeholder:text-white/60 text-base sm:text-lg h-12 sm:h-14 text-right border-white/30 focus:border-white/50"
          />
        </form>
      </motion.div>
    </div>
  );
}
