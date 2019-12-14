
export interface IUserInfo {
    "username" : string;
    "history" : IHistory[];
}

export interface IHistory {
    "timestamp" : string;
    "songs" : ISongs[];
}

export interface ISongs {
    "song" : string;
    "sentiment" : string;
    "lyrics" : string;
    "timestamp" : string;
 }

 export class ISongSentimentData {
    date : Date;
    pct25 : number;
    pct50 : number;
    pct05 : number;
    pct75 : number;
    pct95 : number;
}