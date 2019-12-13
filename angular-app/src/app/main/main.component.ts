import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { SentanalysisService } from '../sentanalysis.service';
import { IUserInfo, IHistory, ISongs, ISongSentimentData } from '../userinfo';
import * as c3 from 'c3';
import { isUndefined } from 'util';
import { ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  @Input('parentData') public parentName;
  routeParams: Params;
  // Query parameters found in the URL: /example-params/one/two?query1=one&query2=two
  queryParams: Params;
  public username = "User";
  public isVisible = true;
  public songData: IUserInfo;
  public accessToken;

  constructor(private _analysisService: SentanalysisService,  private activatedRoute: ActivatedRoute) {
    this.getRouteParams();
   }

  getRouteParams() {
        // Route parameters
        this.activatedRoute.params.subscribe( params => {
            this.routeParams = params;
        });

        // URL query parameters
        this.activatedRoute.queryParams.subscribe( params => {
            this.queryParams = params;
            // TODO - fix this logic
            // this.accessToken = params.access_token;
            this.accessToken = "BQCPMHMZUWvjU-EINDyX_pYKBBhCnN3ekPgfZmStWGegntfVSYPn2zWFzO7lw_EIe7RXlhKs1utiHwKqcaHM0YaJF5ZSwxzRDG_ffo8Hj2-RYTuN7jLNCX2jFzjk5G3s3a2z1mysa_Wq7yOAY-Hx0Hpa1xu66sHl51S0zTYYzEFQ6lhRmi-dZBhEzOKgpcHfxMNEDXvZS2zdJeYFEgiWfmzJnaIkaH_TRWfaX9xJTWZYk1GTZBcHqw";
        });
    }


  @Output() public childEvent = new EventEmitter();

  ngOnInit() {
  }

  ngAfterViewInit() {
    this._analysisService.getSongHistory(this.accessToken).subscribe(data => this.processHistoryData(data));
  }

  countElement(name: string, historyElement: IHistory): number {
    return historyElement.songs.filter(function (element) {
      return element.sentiment == name;
    }).length;
  }

  processSongData(name: string, songData: IUserInfo) {
    let sentArray = new Array<any>();
    this.username = songData.username;

    sentArray.push(this.formElement('sadness', songData.history));
    sentArray.push(this.formElement('happiness', songData.history));
    sentArray.push(this.formElement('anger', songData.history));
    sentArray.push(this.formElement('neutral', songData.history));

    return sentArray;
  }

  formElement(name: string, historyList: Array<IHistory>) {
    let dataList = new Array<any>();
    dataList.push(name);
    for (let index = 0; index < historyList.length; index++) {
      dataList.push(this.countElement(name, historyList[index]));
    }
    return dataList;
  }

  processHistoryData(rawData) {
    this.songData = rawData;
    let sentArray = this.processSongData("Vijay", this.songData);

    let chart = c3.generate({
      bindto: '#chart',
      data: {
        columns: sentArray
      },
      axis: {
        y: {
          label: { // ADD
            text: 'Song Count',
            position: 'outer-middle'
          }
        },
        y2: {
          show: true,
          label: { // ADD
            text: 'Song Count',
            position: 'outer-middle'
          }
        }
      }
    });

  }
}
