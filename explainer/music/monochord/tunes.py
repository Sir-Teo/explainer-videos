"""A small corpus of traditional and long-out-of-copyright tunes, for Part 14 (*Melody*) and after.

Each tune is written in scale degrees, as a singer would sol-fa it, so that the key does not matter:

    1 2 3 4 5 6 7      the degrees of the major scale (in a tune marked ``minor``: of the natural minor scale)
    5,   1'            the same degree an octave lower, an octave higher
    #4   b7            raised or lowered by a semitone
    3*2  5*.5          twice as long as a beat, half as long (no mark: one beat)
    /                  the end of a phrase

They were written out from memory for this series, in the versions most often sung; they are not a scholarly
edition, the rhythms of some are simplified, and a few stop after their first strain.  Statistics computed from
them are compared in the film with published counts from far larger collections (the Essen folksong collection).
Checked in ``tests/music/test_melody.py``: every tune parses, stays within two octaves, and ends on its tonic or a
note of its tonic triad.
"""

from __future__ import annotations

TUNES: dict[str, dict] = {
    "Ah! vous dirai-je, maman (the Tune)": {"origin": "France", "notes":
        "1 1 5 5 6 6 5*2 / 4 4 3 3 2 2 1*2 / 5 5 4 4 3 3 2*2 / 5 5 4 4 3 3 2*2 / 1 1 5 5 6 6 5*2 / 4 4 3 3 2 2 1*2 /"},
    "Frère Jacques": {"origin": "France", "notes":
        "1 2 3 1 / 1 2 3 1 / 3 4 5*2 / 3 4 5*2 / 5*.5 6*.5 5*.5 4*.5 3 1 / 5*.5 6*.5 5*.5 4*.5 3 1 / 1 5, 1*2 / 1 5, 1*2 /"},
    "Mary Had a Little Lamb": {"origin": "United States", "notes":
        "3 2 1 2 3 3 3*2 / 2 2 2*2 3 5 5*2 / 3 2 1 2 3 3 3 3 / 2 2 3 2 1*4 /"},
    "London Bridge": {"origin": "England", "notes":
        "5*1.5 6*.5 5 4 3 4 5*2 / 2 3 4*2 3 4 5*2 / 5*1.5 6*.5 5 4 3 4 5*2 / 2*2 5*2 3 1*3 /"},
    "Ode to Joy": {"origin": "Beethoven, 1824", "notes":
        "3 3 4 5 5 4 3 2 / 1 1 2 3 3*1.5 2*.5 2*2 / 3 3 4 5 5 4 3 2 / 1 1 2 3 2*1.5 1*.5 1*2 /"},
    "Happy Birthday to You": {"origin": "United States", "notes":
        "5,*.75 5,*.25 6, 5, 1 7,*2 / 5,*.75 5,*.25 6, 5, 2 1*2 / 5,*.75 5,*.25 5 3 1 7, 6, / 4*.75 4*.25 3 1 2 1*2 /"},
    "Amazing Grace": {"origin": "United States", "notes":
        "5, 1*2 3*.5 1*.5 3*2 2 1*2 6, 5,*2 / 5, 1*2 3*.5 1*.5 3*2 2*.5 3*.5 5*3 / 3*.5 5*.5 5*2 3*.5 1*.5 3*2 2 1*2 6, 5,*2 / 5, 1*2 3*.5 1*.5 3*2 2 1*3 /"},
    "Auld Lang Syne": {"origin": "Scotland", "notes":
        "5, 1*1.5 1*.5 1 3 2*1.5 1*.5 2 3 / 1*1.5 1*.5 3 5 6*3 / 6 5*1.5 3*.5 3 1 2*1.5 1*.5 2 3 / 1*1.5 6,*.5 6, 5, 1*3 /"},
    "Greensleeves": {"origin": "England", "mode": "minor", "notes":
        "1 3*2 4 5*1.5 #6*.5 5 4*2 2 7,*1.5 1*.5 2 / 3*2 1 1*1.5 #7,*.5 1 2*2 #7, 5,*2 / 1 3*2 4 5*1.5 #6*.5 5 4*2 2 7,*1.5 1*.5 2 / 3*1.5 2*.5 1 #7,*1.5 #6,*.5 #7, 1*3 /"},
    "Oh! Susanna": {"origin": "Stephen Foster, 1848", "notes":
        "1*.5 2*.5 3 5 5*1.5 6*.5 5 3 1*1.5 2*.5 / 3 3 2 1 2*3 / 1*.5 2*.5 3 5 5*1.5 6*.5 5 3 1*1.5 2*.5 / 3 3 2 2 1*3 /"},
    "Yankee Doodle": {"origin": "United States", "notes":
        "1 1 2 3 1 3 2 5, / 1 1 2 3 1*2 7,*2 / 1 1 2 3 4 3 2 1 / 7, 5, 6, 7, 1*2 1*2 /"},
    "Row, Row, Row Your Boat": {"origin": "United States", "notes":
        "1 1 1*.67 2*.33 3 / 3*.67 2*.33 3*.67 4*.33 5*2 / 1'*.33 1'*.33 1'*.33 5*.33 5*.33 5*.33 3*.33 3*.33 3*.33 1*.33 1*.33 1*.33 / 5*.67 4*.33 3*.67 2*.33 1*2 /"},
    "Three Blind Mice": {"origin": "England", "notes":
        "3 2 1*2 / 3 2 1*2 / 5 4*.5 4*.5 3*2 / 5 4*.5 4*.5 3*2 / 5*.5 1'*.5 1'*.5 7*.5 6*.5 7*.5 1'*.5 5*.5 5 / 5*.5 1'*.5 1'*.5 7*.5 6*.5 7*.5 1'*.5 5*.5 5 / 5*.5 4*.5 3 2 1*2 /"},
    "Old MacDonald": {"origin": "United States", "notes":
        "1 1 1 5, 6, 6, 5,*2 / 3 3 2 2 1*3 / 5, 1 1 1 5, 6, 6, 5,*2 / 3 3 2 2 1*4 /"},
    "Jingle Bells (chorus)": {"origin": "James Pierpont, 1857", "notes":
        "3 3 3*2 3 3 3*2 / 3 5 1*1.5 2*.5 3*4 / 4 4 4*1.5 4*.5 4 3 3 3*.5 3*.5 / 3 2 2 3 2*2 5*2 / 3 3 3*2 3 3 3*2 / 3 5 1*1.5 2*.5 3*4 / 4 4 4*1.5 4*.5 4 3 3 3*.5 3*.5 / 5 5 4 2 1*4 /"},
    "Silent Night": {"origin": "Franz Gruber, 1818", "notes":
        "5*1.5 6*.5 5 3*3 / 5*1.5 6*.5 5 3*3 / 2'*2 2' 7*3 / 1'*2 1' 5*3 / 6*2 6 1'*1.5 7*.5 6 5*1.5 6*.5 5 3*3 / 6*2 6 1'*1.5 7*.5 6 5*1.5 6*.5 5 3*3 / 2'*2 2' 4'*1.5 2'*.5 7 1'*3 3'*3 / 1' 5 3 5*1.5 4*.5 2 1*3 /"},
    "Joy to the World": {"origin": "Lowell Mason, 1839", "notes":
        "1'*2 7*1.5 6*.5 5*3 4 3*2 2*2 1*3 / 5 6*3 6 7*3 7 1'*3 / 1' 1' 7 6 5 5*1.5 4*.5 3 / 1' 1' 7 6 5 5*1.5 4*.5 3 / 3 3 3 3 3*.5 4*.5 5*3 / 4*.5 3*.5 2 2 2 2*.5 3*.5 4*3 / 3*.5 2*.5 1 1'*2 6 5*1.5 4*.5 3 4 3*2 2*2 1*4 /"},
    "Hot Cross Buns": {"origin": "England", "notes":
        "3 2 1*2 / 3 2 1*2 / 1*.5 1*.5 1*.5 1*.5 2*.5 2*.5 2*.5 2*.5 / 3 2 1*2 /"},
    "Au clair de la lune": {"origin": "France", "notes":
        "1 1 1 2 3*2 2*2 / 1 3 2 2 1*4 / 1 1 1 2 3*2 2*2 / 1 3 2 2 1*4 / 2 2 2 2 6,*2 6,*2 / 2 1 7, 6, 5,*4 / 1 1 1 2 3*2 2*2 / 1 3 2 2 1*4 /"},
    "Sur le pont d'Avignon": {"origin": "France", "notes":
        "1 1 1*2 2 2 2*2 / 3 4 5 1 7, 1 2 5, / 1 1 1*2 2 2 2*2 / 3 4 5 1 2 7, 1*2 /"},
    "Alouette": {"origin": "Canada", "notes":
        "1*1.5 2*.5 3 3 2*.5 1*.5 2*.5 3*.5 1 5, / 1*1.5 2*.5 3 3 2*.5 1*.5 2*.5 3*.5 1*2 /"},
    "Lightly Row (Hänschen klein)": {"origin": "Germany", "notes":
        "5 3 3*2 4 2 2*2 / 1 2 3 4 5 5 5*2 / 5 3 3*2 4 2 2*2 / 1 3 5 5 3*4 / 2 2 2 2 2 3 4*2 / 3 3 3 3 3 4 5*2 / 5 3 3*2 4 2 2*2 / 1 3 5 5 1*4 /"},
    "Go Tell Aunt Rhody": {"origin": "United States", "notes":
        "3*2 3 2 1*2 1*2 / 2*2 2 4 3 2 1*2 / 5*2 5 4 3*2 3*2 / 2 1 2 3 1*4 /"},
    "Good King Wenceslas": {"origin": "Piae Cantiones, 1582", "notes":
        "1 1 1 2 1 1 5,*2 / 6, 5, 6, 7, 1*2 1*2 / 1 1 1 2 1 1 5,*2 / 6, 5, 6, 7, 1*2 1*2 / 5 4 3 2 3 2 1*2 / 6, 5, 6, 7, 1*2 1*2 / 5, 5, 6, 7, 1 1 2*2 / 5 4 3 2 1*2 4*2 1*4 /"},
    "Deck the Halls": {"origin": "Wales", "notes":
        "5*1.5 4*.5 3 2 1 2 3 1 / 2*.5 3*.5 4*.5 2*.5 3*1.5 2*.5 1 7, 1*2 / 5*1.5 4*.5 3 2 1 2 3 1 / 2*.5 3*.5 4*.5 2*.5 3*1.5 2*.5 1 7, 1*2 / 2*1.5 3*.5 4 2 3*1.5 4*.5 5 2 / 3*.5 #4*.5 5 6*.5 7*.5 1' 7 6 5*2 / 5*1.5 4*.5 3 2 1 2 3 1 / 6*.5 6*.5 6*.5 6*.5 5*1.5 4*.5 3 2 1*2 /"},
    "The First Noel": {"origin": "England", "notes":
        "3*.5 2*.5 1*1.5 2*.5 3*.5 4*.5 5*2 / 6*.5 7*.5 1' 7 6 5*2 / 6*.5 7*.5 1' 7 6 5 6 7 1' 5 4 3*2 / 3*.5 2*.5 1*1.5 2*.5 3*.5 4*.5 5*2 / 1'*.5 7*.5 6*2 6 5*3 / 1' 7 6 5 6 7 1' 5 4 3*2 /"},
    "We Wish You a Merry Christmas": {"origin": "England", "notes":
        "5, 1 1*.5 2*.5 1*.5 7,*.5 6, 6, / 6, 2 2*.5 3*.5 2*.5 1*.5 7, 5, / 5, 3 3*.5 4*.5 3*.5 2*.5 1 6, / 5,*.5 5,*.5 6, 2 7, 1*2 /"},
    "Brahms's Lullaby": {"origin": "Brahms, 1868", "notes":
        "3*.5 3*.5 5*1.5 3*.5 3 5*2 / 3*.5 5*.5 1' 7*1.5 6*.5 6 5 / 2*.5 3*.5 4 2 2*.5 3*.5 4*2 / 2*.5 4*.5 7*.5 6*.5 5 7 1'*2 / 1*.5 1*.5 1'*2 6*.5 4*.5 5*2 / 3*.5 1*.5 4 5 6 5*2 / 1*.5 1*.5 1'*2 6*.5 4*.5 5*2 / 3*.5 1*.5 4 3 2 1*2 /"},
    "Simple Gifts": {"origin": "Joseph Brackett, 1848", "notes":
        "5,*.5 5,*.5 1 1*.5 2*.5 3*.5 1*.5 3*.5 4*.5 5 5*.5 4*.5 3 / 2*.5 1*.5 2 2 2 2*.5 1*.5 2*.5 3*.5 2*.5 7,*.5 5, / 5,*.5 5,*.5 1 1*.5 2*.5 3*.5 1*.5 3*.5 4*.5 5 5*.5 4*.5 3 / 2*.5 1*.5 2 2*.5 3*.5 2 1*.5 7,*.5 1 1 1*2 /"},
    "When the Saints Go Marching In": {"origin": "United States", "notes":
        "1 3 4 5*5 / 1 3 4 5*5 / 1 3 4 5*2 3*2 1*2 3*2 2*4 / 3 3 2 1*3 1 3*2 5*2 5 4*3 / 3 4 5*2 3*2 1*2 2*2 1*4 /"},
    "My Bonnie Lies over the Ocean": {"origin": "Scotland", "notes":
        "5, 3 2 1 2 1 6, 5,*2 3,*3 / 5, 3 2 1 1 7, 1 2*5 / 5, 3 2 1 2 1 6, 5,*2 3,*3 / 5, 6, 2 1 7, 6, 7, 1*5 /"},
    "Oh My Darling, Clementine": {"origin": "United States", "notes":
        "1*.75 1*.25 1 5, 3*.75 3*.25 3 1 / 1*.75 3*.25 5*1.5 5*.5 4*.75 3*.25 2*2 / 2*.75 3*.25 4 4 3*.75 2*.25 3 1 / 1*.75 3*.25 2 5, 7,*.75 2*.25 1*2 /"},
    "She'll Be Coming Round the Mountain": {"origin": "United States", "notes":
        "5,*.5 6,*.5 1 1 1 1 6, 5, 3, 5, 1*3 / 1*.5 2*.5 3 3 3 3 5 3 2 1 2*3 / 5*.5 4*.5 3 3 3 3 2 1 1 1 6,*2 / 6, 2 1 7, 6, 5, 7, 2 1*3 /"},
    "Camptown Races": {"origin": "Stephen Foster, 1850", "notes":
        "5 5 3 5 6 5 3*2 / 3 2*3 3 2*3 / 5 5 3 5 6 5 3*2 / 2 2*.5 3*.5 2 1*3 /"},
    "Pop Goes the Weasel": {"origin": "England", "notes":
        "1 1 2 2 3 5 3 1 / 1 1 2 2 3*2 1*2 / 1 1 2 2 3 5 3 1 / 6*2 2 4 3*2 1*2 /"},
    "The Farmer in the Dell": {"origin": "Germany and the United States", "notes":
        "5, 1 1 1 1 1*2 / 2 3 3 3 3 3*2 / 5 5 6 5 3 1 / 2 3 3 2 2 1*2 /"},
    "The Itsy Bitsy Spider": {"origin": "United States", "notes":
        "5, 1 1 1 2 3 3 / 3 2 1 2 3 1*2 / 3 3 4 5 5 4 3 4 5 3*2 / 1 1 2 3 3 2 1 2 3 1*2 / 5, 5, 1 1 1 2 3 3 / 3 2 1 2 3 1*2 /"},
    "This Old Man": {"origin": "England", "notes":
        "5 3 5*2 5 3 5*2 / 6 5 4 3 2 3 4*2 / 3*.5 4*.5 5 1 1*.5 1*.5 1 1*.5 2*.5 3*.5 4*.5 5*2 / 5 2 2 4 3 2 1*2 /"},
    "Jasmine Flower (Mo Li Hua)": {"origin": "China", "notes":
        "3 3*.5 5*.5 6*.5 1'*.5 1'*.5 6*.5 5 5*.5 6*.5 5*2 / 3 3*.5 5*.5 6*.5 1'*.5 1'*.5 6*.5 5 5*.5 6*.5 5*2 / 5 5 5 3*.5 5*.5 6 6 5*2 / 3 2*.5 3*.5 5 3*.5 2*.5 1 1*.5 2*.5 1*2 /"},
    "Drunken Sailor": {"origin": "sea shanty", "mode": "minor", "notes":
        "5 5*.5 5*.5 5 5*.5 5*.5 5 1 3 5 / 4 4*.5 4*.5 4 4*.5 4*.5 4 7, 2 4 / 5 5*.5 5*.5 5 5*.5 5*.5 5 #6 7 1' / 7 5 4 2 1*2 1*2 /"},
    "Kumbaya": {"origin": "United States", "notes":
        "1 3 5*1.5 5*.5 5 6 6 5*3 / 1 3 5*1.5 5*.5 5 4 3 2*3 / 1 3 5*1.5 5*.5 5 6 6 5*3 / 4 3 1 2 2 1*4 /"},
    "Michael, Row the Boat Ashore": {"origin": "United States", "notes":
        "1 3 5*1.5 3*.5 5 6 5*2 / 3 5 6*2 5*2 / 3 5 5*1.5 3*.5 4 3 2*2 / 1 2 3 2 1*2 /"},
    "Skip to My Lou": {"origin": "United States", "notes":
        "3 3 1 1 3 3 5*2 / 2 2 7, 7, 2 2 4*2 / 3 3 1 1 3 3 5*2 / 2 3 4 3 2 1 1*2 /"},
    "La Cucaracha": {"origin": "Mexico", "notes":
        "5,*.5 5,*.5 5,*.5 1*1.5 3 / 5,*.5 5,*.5 5,*.5 1*1.5 3 / 1 1 7, 7, 6, 6, 5,*2 / 5,*.5 5,*.5 5,*.5 7,*1.5 2 / 5,*.5 5,*.5 5,*.5 7,*1.5 2 / 5 6 5 4 3 2 1*2 /"},
    "Aura Lee": {"origin": "George Poulton, 1861", "notes":
        "5, 1 7, 1 2 6, 2*2 / 1 7, 6, 7, 1*4 / 5, 1 7, 1 2 6, 2*2 / 1 7, 6, 7, 1*4 / 3 3 3*2 3 3 3*2 / 3 2 1 2 3*4 / 3 3 4 3 2 6, 2*2 / 1 7, 6, 7, 1*4 /"},
    "O Tannenbaum": {"origin": "Germany", "notes":
        "5, 1*.75 1*.25 1*1.5 2*.5 3*.75 3*.25 3*1.5 / 3*.5 2*.5 3*.5 4 7, 2 1 / 5, 1*.75 1*.25 1*1.5 2*.5 3*.75 3*.25 3*1.5 / 3*.5 2*.5 3*.5 4 7, 2 1 / 5*.5 5*.5 3*.5 6*1.5 5*.5 5*.5 4*.5 4*1.5 / 4*.5 4*.5 2*.5 5*1.5 4*.5 4*.5 3*.5 3 / 5, 1*.75 1*.25 1*1.5 2*.5 3*.75 3*.25 3*1.5 / 3*.5 2*.5 3*.5 4 7, 2 1 /"},
    "Hark! The Herald Angels Sing": {"origin": "Mendelssohn, 1840", "notes":
        "5, 1 1*1.5 7,*.5 1 3 3 2 / 5 5 5*1.5 4*.5 3 2 3*2 / 5, 1 1*1.5 7,*.5 1 3 3 2 / 5 2 2*1.5 7,*.5 7, 6, 5,*2 /"},
    "God Save the King": {"origin": "Britain", "notes":
        "1 1 2 7,*1.5 1*.5 2 / 3 3 4 3*1.5 2*.5 1 / 2 1 7, 1*3 / 5 5 5 5*1.5 4*.5 3 / 4 4 4 4*1.5 3*.5 2 / 3 4*.5 3*.5 2*.5 1*.5 3*1.5 4*.5 5 / 6*.5 4*.5 3 2 1*3 /"},
    "The Star-Spangled Banner": {"origin": "John Stafford Smith, about 1775", "notes":
        "5*.75 3*.25 1 3 5 1'*2 / 3'*.75 2'*.25 1' 3 #4 5*2 / 5*.5 5*.5 3'*1.5 2'*.5 1' 7*2 / 6*.5 7*.5 1' 1' 5 3 1 /"},
    "Alle meine Entchen": {"origin": "Germany", "notes":
        "1 2 3 4 5*2 5*2 / 6 6 6 6 5*4 / 6 6 6 6 5*4 / 4 4 4 4 3*2 3*2 / 2 2 2 2 1*4 /"},
    "Kuckuck, Kuckuck": {"origin": "Germany", "notes":
        "5 3*2 5 3*2 / 2 1 2 1*3 / 2 2 3 4*2 2 / 3 3 4 5*2 3 / 5 3*2 5 3*2 / 4 3 2 1*3 /"},
    "Ach, du lieber Augustin": {"origin": "Austria", "notes":
        "5*1.5 6*.5 5 4 3 1 1 / 2 5, 5, 3 1 1 / 5*1.5 6*.5 5 4 3 1 1 / 2 5, 5, 1*3 /"},
    "Korobeiniki": {"origin": "Russia", "mode": "minor", "notes":
        "5 2*.5 3*.5 4 3*.5 2*.5 1 1*.5 3*.5 5 4*.5 3*.5 / 2*1.5 3*.5 4 5 3 1 1*2 / 4*1.5 6*.5 1' 7*.5 6*.5 5*1.5 3*.5 5 4*.5 3*.5 / 2 2*.5 3*.5 4 5 3 1 1*2 /"},
    "Away in a Manger": {"origin": "James Murray, 1887", "notes":
        "5 5*1.5 4*.5 3 3 2 1 1 7, 6, 5,*2 / 5, 5,*1.5 6,*.5 5, 5, 2 7, 6, 5, 1 3*2 / 5 5*1.5 4*.5 3 3 2 1 1 7, 6, 5,*2 / 5, 4*1.5 3*.5 2 3 2 1 2 6, 7, 1*2 /"},
}
