import { TestBed } from '@angular/core/testing';

import { Predictor } from './predictor';

describe('Predictor', () => {
  let service: Predictor;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Predictor);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
