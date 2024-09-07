import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CapConfigComponent } from './cap-config.component';

describe('CapConfigComponent', () => {
  let component: CapConfigComponent;
  let fixture: ComponentFixture<CapConfigComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CapConfigComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CapConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
