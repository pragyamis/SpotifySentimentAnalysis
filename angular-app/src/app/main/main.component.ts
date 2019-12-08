import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { SentanalysisService } from '../sentanalysis.service';
import { IUserInfo, IHistory, ISongs, ISongSentimentData } from '../userinfo';
import * as c3 from 'c3';
import { isUndefined } from 'util';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  @Input('parentData') public parentName;
  public username = "Unknown";
  public isVisible = true;
  public songData: IUserInfo;

  constructor(private _analysisService: SentanalysisService) { }

  @Output() public childEvent = new EventEmitter();

  ngOnInit() {
  }

  ngAfterViewInit() {
    this._analysisService.getSongHistory().subscribe(data => this.processHistoryData(data));

  }

  fireEvent() {
    this.childEvent.emit('Hey Parent App. How are you doing?');
  }

  countElement(name: string, historyElement: IHistory): number {
    return historyElement.songs.filter(function (element) {
      return element.sentiment == name;
    }).length;
  }

  processSongData(name: string, songData: IUserInfo) {
    let sentArray = new Array<any>();
    this.username = songData.username;

    sentArray.push(this.formElement('sad', songData.history));
    sentArray.push(this.formElement('happy', songData.history));

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
