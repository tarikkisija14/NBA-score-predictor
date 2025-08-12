import { TestBed } from '@angular/core/testing';

import { LeagueLeaders } from './league-leaders';

describe('LeagueLeaders', () => {
  let service: LeagueLeaders;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LeagueLeaders);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
