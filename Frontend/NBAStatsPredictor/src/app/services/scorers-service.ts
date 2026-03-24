import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, interval, switchMap, startWith, shareReplay } from 'rxjs';
import { environment } from '../environment';
import {ScoresResponse,LiveGame} from '../models/Nba.models';


export type { LiveGame, ScoresResponse };

const SCORES_POLL_INTERVAL_MS = 60_000;

@Injectable({ providedIn: 'root' })
export class ScoresService {
  private readonly apiUrl = `${environment.apiBaseUrl}/api/scores`;

  readonly scores$: Observable<ScoresResponse> = interval(SCORES_POLL_INTERVAL_MS).pipe(
    startWith(0),
    switchMap(() => this.http.get<ScoresResponse>(this.apiUrl)),
    shareReplay(1),
  );

  constructor(private http: HttpClient) {}
}
