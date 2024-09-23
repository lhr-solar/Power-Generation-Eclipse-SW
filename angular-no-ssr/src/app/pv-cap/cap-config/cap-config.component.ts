import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'cap-config',
  templateUrl: './cap-config.component.html',
  styleUrls: ['./cap-config.component.css']
})
export class CapConfigComponent {
  @Output() pvTypeChanged = new EventEmitter<string>();
  
  pvTypeOptions = [
    { value: 1, viewValue: 'Array' },
    { value: 2, viewValue: 'Module' },
    { value: 3, viewValue: 'Cell' }
  ]

  onPvTypeChange(event: any) {
    console.log(event);
    this.pvTypeChanged.emit("PV Type changed to " + event.value);
  }
}
