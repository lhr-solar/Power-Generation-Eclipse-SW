import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PortService {
  private getPortsURL = environment.getOpenCOMPortsRoute;

  constructor(private http: HttpClient) {}

  getPorts(): Observable<string[]> {
    return this.http.get<string[]>(this.getPortsURL);
  }
}
