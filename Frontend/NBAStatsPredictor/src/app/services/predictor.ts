import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Predictor {
  private apiUrl = 'https://localhost:7042/api/predictor';

  constructor(private http: HttpClient) { }

  predictGame(homeTeam:string,awayTeam:string):Observable<any>{
    return this.http.post<any>(this.apiUrl,{homeTeam:homeTeam,awayTeam:awayTeam},)
  }

}
