import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { PvCapModule } from './pv-cap/pv-cap.module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    PvCapModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
