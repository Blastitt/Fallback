# Fallback
A distributed implementation of Conway's Game of Life.

This project is intended to be run on four Raspberry Pi's, each controlling a single quadrant of a 16x16 grid of LEDs.

## Concept
One Pi acts as the server, calculating and distributing the next board state to the other three as clients. Should the server become unreachable, one of the clients assumes its role, and the other clients connect to it as the server.

## Noteworthy Features
* Initial board state defaults to a random seed, but can be specified manually via seed.conf.
* Specify which Pi controls which quadrant.

## Usage
### Requirements
* 4 RasPi's
* 1 Network Switch
* 4 8x8 LED grids
* RPi_ws281x python library (for LED control)

### Setup
1. Clone onto each Pi
2. Add the IPs and server ports (eg. 192.168.1.7:8000) of each Pi on a separate line of iplist.conf
3. Start each Pi one by one with run.py (see below)

#### run.py
> run.py [--\<quadrant>] [-r \<seed.conf>]

quadrant:

> tr => Top Right
> tl => Top Left
> br => Bottom Right
> bl => Bottom Left

## Credits
Created by Jonah Lazar, Juan Vallejo, and Nigel Armstrong at VTHacks 2016.
