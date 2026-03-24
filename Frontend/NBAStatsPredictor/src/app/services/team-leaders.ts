import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment';
import { LeadersMap } from '../models/Nba.models';

@Injectable({ providedIn: 'root' })
export class TeamLeadersService {
  private readonly apiUrl = `${environment.apiBaseUrl}/api/teamleaders`;

  constructor(private http: HttpClient) {}

  getTeamLeaders(): Observable<LeadersMap> {
    return this.http.get<LeadersMap>(this.apiUrl);
  }
}
