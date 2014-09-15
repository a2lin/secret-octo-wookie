secret-octo-wookie
==================

Built at PennApps Fall 2014, Street Symphony is an interactive, adaptive jukebox. Somewhat like an automated DJ, we mash together two songs based on similar beats, energy, tempo, etc in order to create more interesting tunes. We use Twilio as a voting engine where users can send a text to a specific number indicating whether they want the music to go faster, slower, louder, quieter, and also send in suggestions for upcoming songs. As certain songs get more votes, we will bias the system to play that soon (as a mashup with a song that our app determines will sound good with it). A good use case for a project like this is to provide music at a party or bar, where you may want the music to reflect the preferences of the current attendees. As people leave and enter the room throughout the night, and continue to send in suggestions via text, Street Symphony can produce harmonious mashups of songs that people currently want to listen to.

Team Members:
Alexander Lin - UCSD
Alexander J. Lin - MIT
Aditya Majumdar - Columbia
Jonathan Uesato - MIT

To run:

git clone

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

python -m jukebox.webapp

The above will start the application @ localhost:8888.
