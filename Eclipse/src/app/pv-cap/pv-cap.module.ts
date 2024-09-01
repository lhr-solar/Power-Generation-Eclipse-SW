import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PvCapComponent } from './pv-cap.component';
import { CapConfigComponent } from './cap-config/cap-config.component';
import { ConsoleComponent } from '../console/console.component';
import { CapDisplayComponent } from './cap-display/cap-display.component';

@NgModule({
  declarations: [
    PvCapComponent,
    CapConfigComponent,
    ConsoleComponent,
    CapDisplayComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    PvCapComponent
  ]
})
export class PvCapModule { }
