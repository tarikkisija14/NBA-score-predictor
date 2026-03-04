import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment';

@Injectable({
  providedIn: 'root'
})
export class Standings {
  private apiUrl = `${environment.apiBaseUrl}/api/standings`;

  constructor(private http: HttpClient) { }

  getStandings(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}
