import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment';
import {StandingsData} from '../models/Nba.models';

@Injectable({ providedIn: 'root' })
export class StandingsService {
  private readonly apiUrl = `${environment.apiBaseUrl}/api/standings`;

  constructor(private http: HttpClient) {}

  getStandings(): Observable<StandingsData> {
    return this.http.get<StandingsData>(this.apiUrl);
  }
}
