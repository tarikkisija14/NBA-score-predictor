import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment';
import{PredictionResponse,PredictRequest} from '../models/Nba.models';


export type { PredictionResponse };

@Injectable({ providedIn: 'root' })
export class PredictorService {
  private readonly apiUrl = `${environment.apiBaseUrl}/api/prediction/predict`;

  constructor(private http: HttpClient) {}

  predictGame(homeTeam: string, awayTeam: string): Observable<PredictionResponse> {
    const payload: PredictRequest = { HomeTeam: homeTeam, AwayTeam: awayTeam };
    return this.http.post<PredictionResponse>(this.apiUrl, payload);
  }
}
