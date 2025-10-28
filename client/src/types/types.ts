export interface QuestionSet {
    id: number;
    title: string;
    description: string;
    userId: number;
}

export interface Question {
    id: number;
    questionSetId: number;
    text: string;
    options: string[];
    correctOptionIndex: string;
    timeLimit: number;
}