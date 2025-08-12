import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LeagueLeaders } from './league-leaders';

describe('LeagueLeaders', () => {
  let component: LeagueLeaders;
  let fixture: ComponentFixture<LeagueLeaders>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LeagueLeaders]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LeagueLeaders);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
