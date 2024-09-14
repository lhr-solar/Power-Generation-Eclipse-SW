import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PvCapModule } from './pv-cap/pv-cap.module';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, PvCapModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'angular-no-ssr';
}
