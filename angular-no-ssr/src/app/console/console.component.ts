import { Component } from '@angular/core';

//TODO: add color to console messages determined by type, add diff types like warning, error, etc
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
