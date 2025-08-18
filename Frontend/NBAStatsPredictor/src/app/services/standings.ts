import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Standings {
  private apiUrl= 'https://localhost:7042/api/standings';// backend endpoint

  constructor(private http: HttpClient) { }
  //fetch staingds  from backend and return as observable
  getStandings():Observable<any>{
    return this.http.get<any>(this.apiUrl)
  }
}
