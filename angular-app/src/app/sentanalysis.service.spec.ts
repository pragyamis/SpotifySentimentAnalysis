import { TestBed } from '@angular/core/testing';

import { SentanalysisService } from './sentanalysis.service';

describe('SentanalysisService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SentanalysisService = TestBed.get(SentanalysisService);
    expect(service).toBeTruthy();
  });
});
