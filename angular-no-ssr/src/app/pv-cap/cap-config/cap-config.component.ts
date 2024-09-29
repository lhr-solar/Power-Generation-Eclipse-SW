import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { PortService } from '../../port/port.service';

@Component({
  selector: 'cap-config',
  templateUrl: './cap-config.component.html',
  styleUrls: ['./cap-config.component.css']
})
export class CapConfigComponent {
  @Output() pvTypeChanged = new EventEmitter<string>();
  
  // Dropdown options:
  pvTypeOptions = [
    { value: 1, viewValue: 'Array' },
    { value: 2, viewValue: 'Module' },
    { value: 3, viewValue: 'Cell' }
  ]
  portOptions: string[] = []

  // Input fields:
  numSteps: number = 150;
  stepSize: number = 0.001;
  settlingTime: number = 2;
  totalSamples: number = 3750;
  testDuration: number = 0;

  //Constructor:
  constructor(private portService: PortService) {}

  ngOnInit() {
    this.portService.getPorts().subscribe( {
      next: (ports) => {
        this.portOptions = ports;
      },
      error: (err) => {
        this.portOptions = [];
        console.error(err);
      }
    });
  }



  // Event functions:
  onPvTypeChange(event: any) {
    // TODO: swap to only printing if in dev environment
    const selectedOption = this.pvTypeOptions.find(option => option.value === event.value);
    if (selectedOption) {
      this.pvTypeChanged.emit("PV Type changed to " + selectedOption.viewValue);
    }

    // TODO: swap each cap config value to defaults for each pvtype on a pvtype swap
  }
}
