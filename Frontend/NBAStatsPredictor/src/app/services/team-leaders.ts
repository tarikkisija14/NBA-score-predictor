import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TeamLeaders {
  private apiUrl = 'https://localhost:7042/api/teamleaders';

  constructor(private http: HttpClient) { }

  getTeamLeaders():Observable<any>{
    return this.http.get<any>(this.apiUrl)
  }

}
