# PyPleer
This is a little script to use [pleer](http://pleer.com "Pleer website") in a terminal.

##Things to know
You need to create an account and register an application to use this script.
In the first use of it, you will be asked to provide your client and application IDs.

The script stores a file in your home directory called *.pleer_config*.

##Usage
###Search a track
`$python3 pleer.py -s "Ellie goulding"`
will search for top 20 results for "Ellie goulding" with all quality.

`$python3 pleer.py -s "Hozier Church" -q "best" -r 50`
will search for top 50 results for "Hozier Church" with best quality.

###Download a track
`$pytohn3 pleer.py -d 2`
will download the second result obtained from the last search.

`$python3 pleer.py -d 1 24 32`
will download the first, 24th and 32th result.

###Show last downloaded tracks
`$python3 pleer.py -H`
will show the last downloaded tracks (up to 20). Can be combined with a research.
