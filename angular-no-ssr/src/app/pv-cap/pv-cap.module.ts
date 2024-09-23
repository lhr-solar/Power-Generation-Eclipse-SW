import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from './material.module';
import { PvCapComponent } from './pv-cap.component';
import { CapConfigComponent } from './cap-config/cap-config.component';
import { ConsoleComponent } from '../console/console.component';
import { CapDisplayComponent } from './cap-display/cap-display.component';


import * as PlotlyJS from 'plotly.js-dist-min';
import { PlotlyModule } from 'angular-plotly.js';

PlotlyModule.plotlyjs = PlotlyJS;

@NgModule({
  declarations: [
    PvCapComponent,
    CapConfigComponent,
    ConsoleComponent,
    CapDisplayComponent
  ],
  imports: [
    CommonModule,
    PlotlyModule,
    MaterialModule
  ],
  exports: [
    PvCapComponent
  ],
  providers: [
    PvCapComponent
  ]
})
export class PvCapModule {
  
}
