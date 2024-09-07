import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CapDisplayComponent } from './cap-display.component';

describe('CapDisplayComponent', () => {
  let component: CapDisplayComponent;
  let fixture: ComponentFixture<CapDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CapDisplayComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CapDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
