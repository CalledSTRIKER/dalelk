import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import { ThumbsUp, ThumbsDown, Copy, Check } from "lucide-react";
import { Message } from "@/types";
import { cn } from "@/lib/utils";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";
import { format } from "date-fns";
import { ar } from "date-fns/locale";

interface ChatMessageProps {
  message: Message;
  onFeedback?: (positive: boolean) => void;
  showFeedback?: boolean;
}

export default function ChatMessage({ message, onFeedback }: ChatMessageProps) {
  const isUser = message.sender === "user";
  const [copied, setCopied] = useState(false);
  const { toast } = useToast();

  const formatTime = (date: Date) => {
    return format(date, 'HH:mm', { locale: ar });
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.text);
      setCopied(true);
      toast({
        title: "تم النسخ",
        description: "تم نسخ الرسالة بنجاح",
      });
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast({
        title: "خطأ",
        description: "فشل نسخ الرسالة",
        variant: "destructive",
      });
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className={cn(
        "flex w-full mb-4",
        isUser ? "justify-start" : "justify-end"
      )}
    >
      <div
        className={cn(
          "px-4 py-3 rounded-2xl shadow-lg animate-fadeIn",
          isUser
            ? "bg-accent text-accent-foreground rounded-tr-sm max-w-[80%]"
            : "bg-white/90 text-foreground rounded-tl-sm max-w-max"
        )}
      >
        <div className="prose prose-sm max-w-none text-right leading-relaxed" dir="rtl">
          {isUser ? (
            <p className="mb-0 whitespace-pre-wrap">{message.text}</p>
          ) : (
            <ReactMarkdown
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
              }}
            >
              {message.text}
            </ReactMarkdown>
          )}
        </div>

        <div className="flex items-center justify-between mt-2">
          <span className="text-xs opacity-60">
            {formatTime(message.timestamp)}
          </span>

          {!isUser && (
            <div className="flex gap-2">
              <button
                onClick={handleCopy}
                className="p-1.5 rounded-lg transition-all hover:bg-accent/10"
                title="نسخ"
              >
                {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
              <button
                onClick={() => onFeedback?.(true)}
                className={cn(
                  "p-1.5 rounded-lg transition-all hover:bg-success/10",
                  message.currentFeedback === 'good' && "bg-success/20",
                  message.animate === "thumbUp" && "animate-thumbUp"
                )}
                title="مفيد"
              >
                <ThumbsUp className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => onFeedback?.(false)}
                className={cn(
                  "p-1.5 rounded-lg transition-all hover:bg-destructive/10",
                  message.currentFeedback === 'bad' && "bg-destructive/20",
                  message.animate === "thumbDown" && "animate-thumbDown"
                )}
                title="غير مفيد"
              >
                <ThumbsDown className="w-3.5 h-3.5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
