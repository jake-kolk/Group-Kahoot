export interface QuestionParams {
    text: string;
    choices: string[];
    question_id: number;
    duration: number;
}

export class Question {
    text;
    choices;
    question_id;
    duration;

    constructor({text, choices, question_id, duration}: QuestionParams) {
        this.text = text;
        this.choices = choices;
        this.question_id = question_id;
        this.duration = duration;
    }
}