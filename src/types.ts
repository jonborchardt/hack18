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
  authors: Author[];
  year: number;
  venue: string;
  inCitationsCounts: GenderCount;
  outCitationsCounts: GenderCount;

  // augmented
  percentFemaleAuthor: number;
  firstFemalePosition: number;
  percentOutCiteFemale: number;
}

export interface Author {
  name: string;
  gender: Gender;
}

export interface GenderCount {
  female?: number,
  male?: number
}

export enum Gender {
  female = 'female',
  male = 'male'
}
