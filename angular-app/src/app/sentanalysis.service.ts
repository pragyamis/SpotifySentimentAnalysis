import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http'
import { IUserInfo, IHistory, ISongs } from './userinfo';
import { Observable } from 'rxjs';
import { HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SentanalysisService {

  private _url : string = "http://3.15.223.174:4201/songs";
  // private _url : string = "http://localhost:8089/sentimentanalysis/v1/";

  private cached_data = undefined;
  public accessToken = undefined;

  constructor(private http : HttpClient) { }

  public getSongHistory(accessToken) : Observable<IUserInfo>{
    console.log("accessToken = " + accessToken + ", this.accessToken = " + this.accessToken);
    if(accessToken != undefined){
      this.accessToken = accessToken;
      console.log("sectting token");
    }

    if(this.cached_data == undefined){
      this.cached_data = this.http.get<IUserInfo>(this._url + '?access_token=' + accessToken);
    }
    return this.cached_data;
  }



}
