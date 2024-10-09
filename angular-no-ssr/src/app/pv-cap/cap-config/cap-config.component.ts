import { Component, EventEmitter, Output, viewChild } from '@angular/core';
import { NgModel } from '@angular/forms';
import { PortService } from '../../port/port.service';
import { environment } from '../../../environments/environment';

//TODO: all buttons, make sure there's a validate all params func on start test press bc some might be 0 or null



@Component({
  selector: 'cap-config',
  templateUrl: './cap-config.component.html',
  styleUrls: ['./cap-config.component.css']
})
export class CapConfigComponent {
  @Output() ConMsgFromConfig = new EventEmitter<string>();
  numIterNgModel = viewChild.required<NgModel>('numIter');
  stepSizeNgModel = viewChild.required<NgModel>('stepSize');
  settlingTimeNgModel = viewChild.required<NgModel>('settlingTime');
  
  // Dropdown options:
  pvTypeOptions = [
    { value: 1, viewValue: 'Array' },
    { value: 2, viewValue: 'Module' },
    { value: 3, viewValue: 'Cell' }
  ]
  portOptions: string[] = []

  defaults = {
    Array: {
      sampleRange: "0.3:0.45",
      numIter: 25,
      stepSize: 0.001,
      settlingTime: 2,
    },
    Module: {
      sampleRange: "0.2:0.7"
    },
    Cell: {
      sampleRange: "0.2:0.8"
    },
  }

  // Input fields:
  sampleRange: string = "0.1:0.9";
  lowerBound: number = 0.1;
  upperBound: number = 0.9;

  numIterVal: number = 1;
  stepSizeVal: number = 0.001;
  settlingTimeVal: number = 2;

  numSteps: number = 150;
  totalSamples: number = 3750;
  testDuration: number = 0;

  //Constructor:
  constructor(
    private portService: PortService,
  ) {}

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
    this.setDefaults(this.pvTypeOptions[0]);
  }


  // Event functions:
  // Triggers when PV Type dropdown changes
  pvTypeChange(event: any) {
    // TODO: swap to only printing if in dev environment
    const selectedOption = this.pvTypeOptions.find(option => option.value === event.value);
    if (selectedOption) {
      this.ConMsgFromConfig.emit("PV Type changed to " + selectedOption.viewValue);
    }
    this.numSteps++;

    this.setDefaults(selectedOption);
  }

  numIterChanged(newNumIter: number) {
    if(!environment.production)
      this.ConMsgFromConfig.emit("In num iter changed, display internal " + newNumIter + " " + this.numIterVal);
    if((newNumIter) && newNumIter != this.numIterVal) {
      this.numIterVal = Math.max(1, Math.floor(newNumIter));
      this.numIterNgModel().control.setValue(this.numIterVal);
      this.updateTestStatistics();
    }
  }

  stepSizeChanged(newStepSize: number) {
    if(!environment.production)
      this.ConMsgFromConfig.emit("In step size changed, display internal " + newStepSize + " " + this.stepSizeVal);
    if((newStepSize) && newStepSize != this.stepSizeVal) {
      this.stepSizeVal = Math.min(0.1, Math.max(0.001, Math.round(newStepSize / 0.001) * 0.001)); // Round to 3 decimal places in between .001 and .1
      this.stepSizeNgModel().control.setValue(this.stepSizeVal);
      this.updateTestStatistics();
    }
  }

  settlingTimeChanged(newSettlingTime: number) {
    if(!environment.production)
      this.ConMsgFromConfig.emit("In settling time changed, display internal " + newSettlingTime + " " + this.settlingTimeVal);
    if((newSettlingTime) && newSettlingTime != this.settlingTimeVal) {
      this.settlingTimeVal = Math.min(10, Math.max(0.1, Math.round(newSettlingTime / 0.1) * 0.1)); // Round to 1 decimal place between 0.1 and 10
      this.settlingTimeNgModel().control.setValue(this.settlingTimeVal);
      this.updateTestStatistics();
    }
  }

  // Other internal tools:
  //TODO: add the res tof the defaults
  setDefaults(selectedOption: any) {
    switch (selectedOption?.viewValue) {
      case "Array":
        this.sampleRange = this.defaults.Array.sampleRange;
        break;
      case "Module":
        this.sampleRange = this.defaults.Module.sampleRange;
        break;
      case "Cell":
        this.sampleRange = this.defaults.Cell.sampleRange;
        break;
      default:
        this.sampleRange = this.defaults.Array.sampleRange;
        break;
    }
    this.validateRange(null);
    this.updateTestStatistics();
  }

  // Called to validate the current sampling range input, also updates the lower and upper bounds
  // Call if: 
  //    want to know if current range is valid
  //    want to update lower and upper bounds
  validateRange(event: any) {
    try {
      const range = this.sampleRange.split(":");
      const lowerBound = parseFloat(range[0]);
      const upperBound = parseFloat(range[1]);
      if (lowerBound < 0 || lowerBound > 1 || upperBound < 0 || upperBound > 1 || upperBound < lowerBound) {
        throw new Error("Invalid range");
      }
      this.lowerBound = lowerBound;
      this.upperBound = upperBound;
      return true;

    } catch (error) {
      if(!environment.production) {
        this.ConMsgFromConfig.emit("Invalid range: " + this.sampleRange);
        console.warn("Invalid range: " + this.sampleRange);
      }
      return false;
    }
  }

  updateTestStatistics() {
    this.numSteps = Math.round((this.upperBound - this.lowerBound) / this.stepSizeVal);
    this.totalSamples = this.numSteps * this.numIterVal;
    this.testDuration = this.totalSamples * this.settlingTimeVal;
  }
}
