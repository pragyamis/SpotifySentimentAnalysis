import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http'
import { IUserInfo, IHistory, ISongs } from './userinfo';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SentanalysisService {

  private _url : string = "http://localhost:8089/sentimentanalysis/v1/";
  constructor(private http : HttpClient) { }

  public getSongHistory() : Observable<IUserInfo>{
    return this.http.get<IUserInfo>(this._url);
  }
}
