import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {environment} from '../environment';

export interface PredictionResponse {
  winner: string;
  winner_points: number;
  loser: string;
  loser_points: number;
}

export interface PredictRequest {
  HomeTeam: string;
  AwayTeam: string;
}

@Injectable({
  providedIn: 'root'
})
export class PredictorService {

  private apiUrl = `${environment.apiBaseUrl}/api/prediction/predict`;

  constructor(private http: HttpClient) {}

  predictGame(homeTeam: string, awayTeam: string): Observable<PredictionResponse> {
    const payload: PredictRequest = { HomeTeam: homeTeam, AwayTeam: awayTeam };
    return this.http.post<PredictionResponse>(this.apiUrl, payload);
  }
}
