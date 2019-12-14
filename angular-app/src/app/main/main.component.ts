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
  public urlSearchParams;
  private gridApi;
  private columnApi;
  private gridOptions = {
    columnDefs : [
      {headerName: 'Day', field: 'day', width : '100', filter: "agTextColumnFilter"},
      {headerName: 'Song Title', field: 'song'},
      {headerName: 'Sentiment', field: 'sentiment', width : '100'},
      {headerName: 'Lyrics', field: 'lyrics', width : '1200', filter: "agTextColumnFilter"},
      {headerName: 'Timestamp', field: 'timestamp', width : '300'},
    ],
    defaultColDef: {
      // make every column editable
      editable: false,
      // make every column use 'text' filter by default
      filter: 'agTextColumnFilter',
      resizable: true,
      suppressSizeToFit: false
  },
}

  rowData = [
  ];

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
       });
    }


  @Output() public childEvent = new EventEmitter();

  ngOnInit() {
    
    // Since access_token is coming in as a fragment - reading it from snapshot
    this.accessToken =     new URLSearchParams(this.activatedRoute.snapshot.fragment).get("access_token");
  }

  onGridReady(params) {
    this.gridApi = params.api;
    this.columnApi = params.columnApi;
    this.gridApi.sizeColumnsToFit();
    window.onresize = () => {
        this.gridApi.sizeColumnsToFit();
    }
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

    songData.history.forEach(history => {
      history.songs.forEach(song => {
        let record = {
          day : history.timestamp,
          timestamp : song.timestamp,
          song : song.song,
          sentiment : song.sentiment,
          lyrics : song.lyrics
        };
        this.rowData.push(record);
      });
        
    });
    this.rowData.push(songData.history);


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
    this.rowData = [];
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
