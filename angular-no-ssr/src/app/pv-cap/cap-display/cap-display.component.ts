import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'cap-display',
  templateUrl: './cap-display.component.html',
  styleUrls: ['./cap-display.component.css'],
})
export class CapDisplayComponent implements OnInit {
  public graph = {
    data: [
      {
        x: [/* Voltage data */],
        y: [/* Current data */],
        type: 'scatter',
        mode: 'lines+points',
        name: 'I-V Curve',
        yaxis: 'y1'
      },
      {
        x: [/* Voltage data */],
        y: [/* Power data */],
        type: 'scatter',
        mode: 'lines+points',
        name: 'P-V Curve',
        yaxis: 'y2'
      }
    ],
    layout: {
      autosize: true,
      margin: { l: 0, r: 0, b: 0, t: 0 },
      // height: 800,
      // width: null,
      title: 'PV Characteristics',
      xaxis: { title: 'Voltage (V)' },
      yaxis: { title: 'Current (A)', side: 'left' },
      yaxis2: {
        title: 'Power (W)',
        overlaying: 'y',
        side: 'right'
      }
    }
  };

  public vOc: number = 0; // Open-circuit voltage
  public iSc: number = 0; // Short-circuit current
  public vMpp: number = 0; // Voltage at maximum power point
  public iMpp: number = 0; // Current at maximum power point
  public pMpp: number = 0; // Power at maximum power point
  public ff: number = 0; // Fill factor

  constructor() {}

  ngOnInit(): void {
    // Initialize your data here
  }
}
