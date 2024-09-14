import { NgModule, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { PvCapComponent } from './pv-cap.component';
import { CapConfigComponent } from './cap-config/cap-config.component';
import { ConsoleComponent } from '../console/console.component';
import { CapDisplayComponent } from './cap-display/cap-display.component';
import { PlotlyModule } from 'angular-plotly.js';


@NgModule({
  declarations: [
    PvCapComponent,
    CapConfigComponent,
    ConsoleComponent,
    CapDisplayComponent
  ],
  imports: [
    CommonModule,
    PlotlyModule
  ],
  exports: [
    PvCapComponent
  ]
})
export class PvCapModule {
  constructor(@Inject(PLATFORM_ID) private platformId: Object) {
    if (isPlatformBrowser(this.platformId)) {
      import('plotly.js-dist-min').then(PlotlyJS => {
        PlotlyModule.plotlyjs = PlotlyJS.default;
      });
    }
  }
}
