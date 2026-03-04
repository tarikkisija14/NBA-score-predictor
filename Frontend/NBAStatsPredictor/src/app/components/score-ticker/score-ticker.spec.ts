import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScoreTicker } from './score-ticker';

describe('ScoreTicker', () => {
  let component: ScoreTicker;
  let fixture: ComponentFixture<ScoreTicker>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScoreTicker]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ScoreTicker);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
