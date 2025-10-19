export interface QuestionParams {
    text: string;
    choices: string[];
    question_id: number;
    duration_ms: number;
}

export class Question {
    text;
    choices;
    id;
    duration;

    constructor({text, choices, question_id, duration_ms}: QuestionParams) {
        this.text = text;
        this.choices = choices;
        this.id = question_id;
        this.duration = duration_ms;
    }
}