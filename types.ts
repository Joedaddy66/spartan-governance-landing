
export interface VideoScripts {
  fifteenSecond: string;
  thirtySecond: string;
}

export interface PromoPack {
  videoScripts: VideoScripts;
  thumbnailIdeas: string[];
  socialMediaCaption: string;
}

export interface TranscriptionEntry {
  speaker: 'user' | 'model';
  text: string;
}