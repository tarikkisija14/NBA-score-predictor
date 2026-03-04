import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment';

@Injectable({
  providedIn: 'root'
})
export class LeagueLeaders {
  private apiUrl = `${environment.apiBaseUrl}/api/leagueleaders`;

  constructor(private http: HttpClient) { }

  getLeagueLeaders(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}
