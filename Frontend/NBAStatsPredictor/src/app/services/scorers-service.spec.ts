import { TestBed } from '@angular/core/testing';

import { ScorersService } from './scorers-service';

describe('ScorersService', () => {
  let service: ScorersService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ScorersService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
