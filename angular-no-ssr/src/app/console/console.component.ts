import { Component } from '@angular/core';

@Component({
  selector: 'console',
  templateUrl: './console.component.html',
  styleUrls: ['./console.component.css'],
})
export class ConsoleComponent {
  messages: string[] = [];  
 
  addConsoleMessage(message: string) {
    this.messages.push(message);
  }
}
