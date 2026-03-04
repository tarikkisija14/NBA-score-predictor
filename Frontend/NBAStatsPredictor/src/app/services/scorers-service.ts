import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, interval, switchMap, startWith, shareReplay } from 'rxjs';
import { environment } from '../environment';

export interface LiveGame {
  game_id: string;
  status: string;
  period: number;
  home_team: string;
  home_tricode: string;
  home_score: number;
  home_logo: string;
  away_team: string;
  away_tricode: string;
  away_score: number;
  away_logo: string;
}

export interface ScoresResponse {
  games: LiveGame[];
  count: number;
  error?: string;
}

@Injectable({ providedIn: 'root' })
export class ScoresService {
  private apiUrl = `${environment.apiBaseUrl}/api/scores`;


  scores$: Observable<ScoresResponse> = interval(60_000).pipe(
    startWith(0),
    switchMap(() => this.http.get<ScoresResponse>(this.apiUrl)),
    shareReplay(1)
  );

  constructor(private http: HttpClient) {}
}
