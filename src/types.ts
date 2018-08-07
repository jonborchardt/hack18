export interface Entity {
  id: string;
  name?: string;
}

export interface NamedEntity {
  id: string;
  name: string;
}

export interface NoProps { }

export interface Record {
  id: string;
  author: string;
  gender: string;
  year: number;
  title: string;
  venue: string;
  inCitationsCount: number;
  outCitationsCount: number;
}