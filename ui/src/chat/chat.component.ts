import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { ChatService } from '../services/chat-service';
import { ChatResponse } from '../models/chat-response';
import { ChatMessageComponent } from '../chat-message/chat-message.component';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, ChatMessageComponent],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {
  messages: ChatResponse[] = [];
  currentMessage: string = '';

  isLoading: boolean = false  

  constructor(private chatService: ChatService) {}

  sendMessage() {
    this.isLoading = true;

    if (this.currentMessage.trim()) {
      let msg = new ChatResponse("User", this.currentMessage.trim(), [], undefined);
      this.messages.push(msg);

      let history = this.chatService.collectAnswersFromAncestors(msg);
      this.chatService.askQuestion(this.currentMessage, history).subscribe(data => {
        data.parent = msg
        msg.children.push(data)
        this.isLoading = false;
      })
     
      this.currentMessage = '';
    }
  }
}
