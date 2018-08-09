to run UI

pull repo
then run these commands:
 yarn
 yarn run start





grab data from http://labs.semanticscholar.org/corpus/

for i in `seq 0 39` ; do curl "https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/corpus-2018-05-03/s2-corpus-$i.gz" --output "s2-corpus-$i.gz"; done

or
aws s3 cp --recursive s3://ai2-s2-research-public/open-corpus/ destinationPath

or
wget -i https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/manifest.txt

corpus-2018-05-03/s2-corpus-00.gz
corpus-2018-05-03/s2-corpus-01.gz
corpus-2018-05-03/s2-corpus-02.gz
corpus-2018-05-03/s2-corpus-03.gz
corpus-2018-05-03/s2-corpus-04.gz
corpus-2018-05-03/s2-corpus-05.gz
corpus-2018-05-03/s2-corpus-06.gz
corpus-2018-05-03/s2-corpus-07.gz
corpus-2018-05-03/s2-corpus-08.gz
corpus-2018-05-03/s2-corpus-09.gz
corpus-2018-05-03/s2-corpus-10.gz
corpus-2018-05-03/s2-corpus-11.gz
corpus-2018-05-03/s2-corpus-12.gz
corpus-2018-05-03/s2-corpus-13.gz
corpus-2018-05-03/s2-corpus-14.gz
corpus-2018-05-03/s2-corpus-15.gz
corpus-2018-05-03/s2-corpus-16.gz
corpus-2018-05-03/s2-corpus-17.gz
corpus-2018-05-03/s2-corpus-18.gz
corpus-2018-05-03/s2-corpus-19.gz
corpus-2018-05-03/s2-corpus-20.gz
corpus-2018-05-03/s2-corpus-21.gz
corpus-2018-05-03/s2-corpus-22.gz
corpus-2018-05-03/s2-corpus-23.gz
corpus-2018-05-03/s2-corpus-24.gz
corpus-2018-05-03/s2-corpus-25.gz
corpus-2018-05-03/s2-corpus-26.gz
corpus-2018-05-03/s2-corpus-27.gz
corpus-2018-05-03/s2-corpus-28.gz
corpus-2018-05-03/s2-corpus-29.gz
corpus-2018-05-03/s2-corpus-30.gz
corpus-2018-05-03/s2-corpus-31.gz
corpus-2018-05-03/s2-corpus-32.gz
corpus-2018-05-03/s2-corpus-33.gz
corpus-2018-05-03/s2-corpus-34.gz
corpus-2018-05-03/s2-corpus-35.gz
corpus-2018-05-03/s2-corpus-36.gz
corpus-2018-05-03/s2-corpus-37.gz
corpus-2018-05-03/s2-corpus-38.gz
corpus-2018-05-03/s2-corpus-39.gz
sample-S2-records.gz
license.txt

to unzip
gzip -d sample-s2records.gz


Example
This is a subset of the full Semantic Scholar corpus which represents papers crawled from the Web and subjected to a number of filters.

{
  "id": "4cd223df721b722b1c40689caa52932a41fcc223",
  "title": "Knowledge-rich, computer-assisted composition of Chinese couplets",
  "paperAbstract": "Recent research effort in poem composition has focused on the use of automatic language generation...",
  "entities": [
    "Conformance testing",
    "Natural language generation",
    "Natural language processing",
    "Parallel computing",
    "Stochastic grammar",
    "Web application"
  ],
  "s2Url": "https://semanticscholar.org/paper/4cd223df721b722b1c40689caa52932a41fcc223",
  "s2PdfUrl": "",
  "pdfUrls": [
    "https://doi.org/10.1093/llc/fqu052"
  ],
  "authors": [
    {
      "name": "John Lee",
      "ids": [
        "3362353"
      ]
    },
    "..."
  ],
  "inCitations": [
    "c789e333fdbb963883a0b5c96c648bf36b8cd242"
  ],
  "outCitations": [
    "abe213ed63c426a089bdf4329597137751dbb3a0",
    "..."
  ],
  "year": 2016,
  "venue": "DSH",
  "journalName": "DSH",
  "journalVolume": "31",
  "journalPages": "152-163",
  "sources": [
    "DBLP"
  ],
  "doi": "10.1093/llc/fqu052",
  "doiUrl": "https://doi.org/10.1093/llc/fqu052",
  "pmid": ""
}


Attributes:
id  string
S2 generated research paper ID.

title  string
Research paper title.

paperAbstract  string
Extracted abstract of the paper.

entities  list
S2 extracted list of relevant entities or topics.

s2Url  string
URL to S2 research paper details page.

s2PdfUrl  string
URL to PDF on S2 if available.

pdfUrls  list
URLs related to this PDF scraped from the web.

authors  list
List of authors with an S2 generated author ID and name.

inCitations  list
List of S2 paperId's which cited this paper.

outCitations  list
List of paperId's which this paper cited.

year  int
Year this paper was published as integer.

venue  string
Extracted venue published.

journalName  string
Name of the journal that published this paper.

journalVolume  string
The volume of the journal where this paper was published.

journalPages  string
The pages of the journal where this paper was published.

sources  list
Identifies papers sourced from DBLP or Medline.

doi  string
Digital Object Identifier registered at doi.org.

doiUrl  string
DOI link for registered objects.

pmid  string
Unique identifier used by PubMed.
