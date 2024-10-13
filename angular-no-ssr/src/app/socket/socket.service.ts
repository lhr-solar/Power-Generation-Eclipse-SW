import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { environment } from '../../environments/environment';

@Injectable()
export class SocketService {
  private socketURL;
  private socket$!: WebSocketSubject<any>; // $! mean the var is an observable/stream and not null respectively
  public cellDataList: any[] = [];
  
  constructor(url: string) {
    this.socketURL = url;
  }

  connect(): void {
    if(!this.socket$ || this.socket$.closed) {
      this.socket$ = webSocket(this.socketURL);

      this.socket$.subscribe({
        next: (data) => this.cellDataList.push(data),
        error: (err) => console.error(err),
        complete: () => console.log('Socket connection closed')
      });

      this.socket$.next('Start');
    }
  }

  close() { 
    this.socket$.complete();
  }
}
