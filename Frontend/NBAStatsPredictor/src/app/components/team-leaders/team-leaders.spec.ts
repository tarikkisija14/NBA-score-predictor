import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeamLeaders } from './team-leaders';

describe('TeamLeaders', () => {
  let component: TeamLeaders;
  let fixture: ComponentFixture<TeamLeaders>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeamLeaders]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TeamLeaders);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
