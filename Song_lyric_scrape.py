#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:26:56 2019

@author: danielobennett
"""


import lyricsgenius
from Dans_Genius_API import my_api_token #personal token, go to Genius.com to get your own!

#webscraping
import time
from pymongo import MongoClient


rnb_artists = [
"11:11", "Abra", "Active Child", "Alessia Cara", "Alex Clare", "Allan Kingdom", "Aloe Blacc", "AlunaGeorge",
"Always Never", "Amber Coffman", "Anders", "Anderson Paak", "Anna Wise", "Ari Lennox", "Arlissa", "Autre Ne Veut",
"Banks", "Black Atlass", "Blackbear", "Blood Orange", "Boots", "Bryson Tiller", "Chet Faker", "Childish Gambino",
"Clarence Clarity", "Cocaine 80s", "D'Angelo", "Daley", "Daniel Caesar", "Danny!", "Dawn Richard", "Dean",
"Dvsn", "Elijah Blake", "Erykah Badu", "Estelle", "FKA twigs", "Francis and the Lights", "Frank Ocean",
"Gallant", "GoldLink", "Grimes", "Groove Theory", "H.E.R.", "Hiatus Kaiyote", "How To Dress Well", "Ibeyi",
"Illangelo", "ILoveMakonnen", "Inc.", "Jack Garratt", "Jai Paul", "James Fauntleroy", "Jamie Woon", "Jamila Woods",
"Janelle Monáe", "Jesse Boykins III", "Jessy Lanza", "Jhené Aiko", "JMSN", "Jon Bellion", "Jorja Smith", "Kacy Hill",
"Kali Uchis", "Kaytranada", "Kehlani", "Kelela", "Kelis", "Kenna", "Kevin Abstract", "Khalid", "Kiana Ledé",
"Kid Cudi", "Kiiara", "Kilo Kish", "Kimbra", "King", "Lance Skiiiwalker", "Lapalux", "Låpsley", "Lauv",
"Lion Babe", "Little Dragon", "Lykke Li", "M.I.A.", "Mabel", "Mac Ayres", "Maejor", "Mahalia", "Majid Jordan",
"Malay", "Marian Hill", "Mateo", "Matt Martians", "Maxwell", "Miguel", "Mila J", "Mr Hudson", "Nao",
"Nick Murphy", "NxWorries", "Oh Wonder", "PARTYNEXTDOOR", "Pell", "Perfume Genius", "Quadron","R.LUM.R",
"Rainy Milo", "Raleigh Ritchie", "Raury", "Reggie Sears", "Rhye", "River Tiber", "Ro James", "Rosie Lowe",
"Roy Woods", "Sabrina Claudio", "Samantha Urbani", "Sampha", "Seinabo Sey", "Sevdaliza", "Sevyn Streeter",
"Shura", "Shy Girls", "Sia Furler", "Sinéad Harnett", "Snakehips", "SOHN", "Solange", "Spooky Black",
"Steve Lacy", "Syd tha Kid", "SZA", "Tei Shi", "The Internet", "The Neighbourhood", "The Weeknd", "Thee Satisfaction",
"THEY.", "Thundercat", "Tinashe", "Toro y Moi", "Tory Lanez", "Travis Scott", "Wet", "William Singe",
"Willow Smith", "Yummy Bingham", "Yuna", "Zayn",
]


#connect to mongoDB , need  to run brew services start mongodb then mongo to work
#must also have created a database and collection to store data in
client = MongoClient()
db = client.sep_19_songs #collection name

genius = lyricsgenius.Genius(my_api_token) #
for each_artist in rnb_artists:
    time.sleep(2) 
    artist = genius.search_artist(each_artist,
                              sort="title", 
                              allow_name_change=True,
                              get_full_info=False) 
#allow_name_change = fuzzy match artist name if it doesnt find exact match
    song_num = 0 #track song number for each artist
    for song in artist.songs:
        song_num += 1
        temp_dict = {}
        temp_dict['Artist_name'] = artist.name
        temp_dict['Song'] = song.title
        temp_lyrics = song.lyrics         #make sure listed as strings 
        temp_dict['Lyrics'] = temp_lyrics
        temp_dict['Artist_Song_Count'] = song_num #track song number for each artist
        db.sep_19_songs.insert_one(temp_dict)    #insert into mongo db
    print("Done with", each_artist)

print("Done overall!!")