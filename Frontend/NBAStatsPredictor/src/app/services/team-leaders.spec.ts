import { TestBed } from '@angular/core/testing';

import { TeamLeaders } from './team-leaders';

describe('TeamLeaders', () => {
  let service: TeamLeaders;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TeamLeaders);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
