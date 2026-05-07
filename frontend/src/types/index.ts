export type MajorCode = 'cs' | 'ai' | 'ds' | 'cy' | 'sw' | 'ce';

export interface Message {
  sender: 'user' | 'ai';
  text: string;
  timestamp: Date;
  animate?: 'thumbUp' | 'thumbDown' | null;
  response_time?: number;
  question?: string;
  question_id?: string;
  currentFeedback?: 'good' | 'bad' | null;
}

export interface Suggestion {
  text: string;
  label: string;
}

export const MAJOR_MAP: Record<MajorCode, string> = {
  cs: "علوم الحاسب",
  ai: "الذكاء الاصطناعي",
  ds: "علوم البيانات",
  cy: "الأمن السيبراني",
  sw: "هندسة البرمجيات",
  ce: "هندسة الحاسب والشبكات"
};
