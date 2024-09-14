import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PvCapComponent } from './pv-cap.component';

describe('PvCapComponent', () => {
  let component: PvCapComponent;
  let fixture: ComponentFixture<PvCapComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PvCapComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PvCapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
