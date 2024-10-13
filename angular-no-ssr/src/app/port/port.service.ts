import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PortService {
  private getPortsURL = environment.backendURL + environment.getOpenCOMPortsRoute;

  constructor(private http: HttpClient) {}

  getPorts(): Observable<string[]> {
    let ret_val = this.http.get<string[]>(this.getPortsURL);
    if(!environment.production) 
      console.log(ret_val);
    return ret_val;
  }
}
