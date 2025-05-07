import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { ChatResponse } from '../models/chat-response';

@Injectable({
    providedIn: 'root',
})
export class ChatService {
    private apiUrl = '/api/chat';

    constructor(private http: HttpClient) {}    

    askQuestion(question: string, history: string[]) {
        const body = { question, history };
        return this.http.post<ChatResponse>(`${this.apiUrl}`, body);
    }

    collectAnswersFromAncestors(node: ChatResponse): string[] {
        const answers: string[] = [];
        this.walkUp(node, answers);
        return answers;
      }
      
      walkUp(current: ChatResponse | undefined, answers: string[]) {
        if (!current) return;
        this.walkUp(current.parent, answers);  // Recursively go to the top
        answers.push(`${current.role}:${current.content}`);     // Then push the answer when we come back down
      }

}