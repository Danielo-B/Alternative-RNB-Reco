# Alternative R&B For Me: A Song Recommendation System for Alternative R&B Songs

This project is a recommendation system for alternative R&B songs. The recommendation system can suggest songs based on lyrical similarities in songs in the genre or by similar audio signals between songs.

## Files
Below you can find the purpose for each notebook in this repo:

### Presentation-Alternative RNB for Me.pptx
Formal project slide deck. Please use the pdf to view in browser at the cost of video and audio functionality.

### Song_lyric_scrape.py
Used this file to query the Genius.com API to get the lyrics of songs in the genre. Each document is stored in a MongoDB. Steps include:
* Importing unique API token
* Query API to gather lyrics for each artist using a created list of artists
* Store input data into MongoDB

### Lyrics export.ipynb
Main Notebook: Steps below:
* Query data from MongoDB to put into a dataframe
* Remove artists/ songs that for various reasons
*  

## Extras
### Flask App: Coming Soon!
### Blog Post: Coming Soon!
