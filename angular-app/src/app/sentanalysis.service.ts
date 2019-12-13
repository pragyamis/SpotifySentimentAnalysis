import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http'
import { IUserInfo, IHistory, ISongs } from './userinfo';
import { Observable } from 'rxjs';
import { HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SentanalysisService {

  private _url : string = "http://3.15.223.174:4201/songs/";

  constructor(private http : HttpClient) { }

  public getSongHistory(accessToken) : Observable<IUserInfo>{
    return this.http.get<IUserInfo>(this._url + '?access_token=' + accessToken);
  }
}
