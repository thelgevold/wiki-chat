import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ChatResponse } from '../models/chat-response'; 
import { ChatService } from '../services/chat-service';

@Component({
  selector: 'app-chat-message',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-message.component.html',
  styleUrls: ['./chat-message.component.css']
})
export class ChatMessageComponent {
  @Input() msg!: ChatResponse;
  @Input() depth = 0;

  replying = false;
  replyText = '';
  isLoading = false;

  constructor(private chatService: ChatService) {}

  toggleReply() {
    this.replying = !this.replying;
  }

  sendReply() {
    if (!this.replyText.trim()) return;

    const reply = new ChatResponse(
      'User', 
      this.replyText, 
      [], 
      [],
      this.msg
    );
    this.msg.children = this.msg.children || [];
    this.msg.children.push(reply);

    let history = this.chatService.collectAnswersFromAncestors(reply);
    this.isLoading = true;

    this.chatService.askQuestion(this.replyText, history).subscribe(data => {
      data.parent = this.msg;
      reply.children.push(data);
      
      this.isLoading = false;
      
      console.log(this.msg)

      // Reset state
      this.replyText = '';
      this.replying = false;
    });

    
  }

}