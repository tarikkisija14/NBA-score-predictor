import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Standings {
  private apiUrl= 'https://localhost:7042/api/standings';

  constructor(private http: HttpClient) { }

  getStandings():Observable<any>{
    return this.http.get<any>(this.apiUrl)
  }
}
