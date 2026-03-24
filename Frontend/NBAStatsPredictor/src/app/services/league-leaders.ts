import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment';
import{LeadersMap} from '../models/Nba.models';

@Injectable({ providedIn: 'root' })
export class LeagueLeadersService {
  private readonly apiUrl = `${environment.apiBaseUrl}/api/leagueleaders`;

  constructor(private http: HttpClient) {}

  getLeagueLeaders(): Observable<LeadersMap> {
    return this.http.get<LeadersMap>(this.apiUrl);
  }
}
