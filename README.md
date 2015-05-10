# PyPleer
This is a little script to use [pleer](pleer.com "Pleer website") in a terminal.

##Things to know
You need to create an account and register a application to use this script.
In the first use of it, you will be asked to provide your client and applications IDs.

The script store a file in your home directory called *.pleer_config*.

##Usage
###Search a track
`$python3 pleer.py -s "Ellie goulding"`
Will search for top 20 results for "Ellie goulding" with all quality.

`$python3 pleer.py -s "Hozier Church" -q "best" -r 50`
Will search for top 50 results for "Hozier Church" with best quality.

###Download a track
`$pytohn3 pleer.py -d 2`
Will download the second result obtained from the last search.

`$python3 pleer.py -d 1 24 32`
Will download the first, 24th and 32th result.

###Show last downloaded tracks
`$python3 pleer.py -H`
Will show the last downloaded tracks (up to 20). Can be combined with a research.
