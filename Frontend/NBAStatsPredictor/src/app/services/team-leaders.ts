import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment';

@Injectable({
  providedIn: 'root'
})
export class TeamLeaders {
  private apiUrl = `${environment.apiBaseUrl}/api/teamleaders`;

  constructor(private http: HttpClient) { }

  getTeamLeaders(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}
