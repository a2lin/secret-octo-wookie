#!/bin/bash
# run with ./youtube2wav.sh https://www.youtube.com/watch?v=hT_nvWreIhg
# where the parameter is the youtube url you want the sound of
# it'll create a .wav of that titled like OneRepublic - Counting Stars.wav
# A very simple Bash script to download a YouTube video 
# and extract the music file from it. 
address=$1 
regex='v=(.*)' 
	if [[ $address =~ $regex ]]; then 
	video_id=${BASH_REMATCH[1]}
	video_id=$(echo $video_id | cut -d'&' -f1) 
	video_title="$(youtube-dl --get-title $address)" 
	youtube-dl $address 
	ext="mp4" 
	echo "$video_title"
	echo "$video_id"
	full_title="$video_title-$video_id"
	echo $full_title
	ffmpeg -i "$full_title".$ext "$video_title".wav 
	#lame "$video_title".wav "$video_title".mp3 
	#rm $video_id.$ext "$video_title".wav 
else 
	echo "Sorry but the system encountered a problem." 
fi