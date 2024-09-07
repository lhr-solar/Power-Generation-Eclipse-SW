import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { ConsoleComponent } from '../console/console.component';

@Component({
  selector: 'pv-cap',
  templateUrl: './pv-cap.component.html',
  styleUrls: ['./pv-cap.component.css']
})
export class PvCapComponent implements AfterViewInit{
  @ViewChild(ConsoleComponent) consoleComponent!: ConsoleComponent;

  ngAfterViewInit() {
    this.consoleComponent.addConsoleMessage("PV Capture Page Started")
  }
}
