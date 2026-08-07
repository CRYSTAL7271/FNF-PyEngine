# FNF-PyEngine

This game was not officially made from CrystalStudios or CRYSTAL7271 on github, it was made by ninjamuffin and others..
And the assets were took from ShadowMario's Engine (Psych Engine) and made a manual conversion tool!

All of the code in the python scripts are made by CrystalStudios, please if you consider making modifications, optimizations or add new things,
please add @crystalstudios3419 (Youtube) or CRYSTAL7271 (Github) in the credits of the project if it is public or distributed to others!

- The project is probably discontinued.

# Guide

The development made a different structure from psych and v-slice engines!
(Before adjusting this project you must have atleast knowledge about python, json, xml and probably more..)

# Guide - Conversion from psych to pyengine & chart structure

In the chart structure it's usually used json, same here, only one difference..
the arrows have a string in the array to make the game understand which character will do that arrow, the game has two options..
opponent or player.

For example:

v This is a part of the notes array v
`{"sectionBeats": 4, "sectionNotes": [[9600, "mainfnf:callNote//opponent.gf.left", 0], [10800, "mainfnf:callNote//opponent.gf.right", 0]], "typeOfSection": 0, "mustHitSection": false}`
Ignoring all the others, and checking in the sectionNotes, we have different things from a classic psych engine structure, instead of a int we have a string!
This string calls a event and it's the mainfnf event, and it gives the: [playeroropponent].[character].[arrowdirection],
this actually gives the game the explanation on how to call events. YOU can change this method, but it will be more time to lose for this!

Outside of the sectionNotes there is: `"pyengine_version"` (currently in build 1) and `"needsVoices"` (means that the song needs seperate Voices-dad and Voices-bf files ogg, if not it will just be Voices.ogg)

# Guide - Adding a song

The song must have a different structure of data and song parts, 
in this case you must have the Song data and music in one directory(Folder).

So, in this case you first convert the json from psych to pyengine (only psychtopyengine converter for now). 
If you already did, make a folder of the song's name, insert Inst.ogg and Voices.ogg (depends on the needsVoices instruction in the **Guide about conversion and json structure**.. *check it*).
Add a folder called 'data' inside the song folder and add the difficulties, simple as you need to put `songname-difficulty.json`

# Other Info

This project version is in 1 (as the version is only presented as a integer), covered by the Creative Commons Attribution license.
