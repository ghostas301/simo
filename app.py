from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from pytube import YouTube
import requests
import os
import json

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/',methods=['GET', 'POST'])
def index():
	if request.method == "POST":
		link = request.form['link']
		if link == '':
			flash('Vous de devez entrez le lien du télécharement','danger')
			return redirect('/')
		ys = YouTube(link)
		titre = ys.title
		fileName = "static/audio/"+titre+".mp3"
		y = os.path.isfile(fileName)
		if y == True:
			flash('Cette chanson est déjà existante !','danger')
			return redirect('/')
		artiste = ys.author
		video = ys.streams.filter(only_audio=True).first()
		length=ys.length
		duration = str(int(length/60)) + ':' + str(int(length%60))
		with open("static/bdd.json", encoding='utf-8') as json_file:
			data = json.load(json_file)
			donnee = {"track":len(data)+1,"name":titre,"duration":duration,"file":titre}
			data.append(donnee)
			with open('static/bdd.json', 'w') as outfile:
				json.dump(data, outfile,indent=4)
		 
		downloaded_file = video.download('static/audio')
		base, ext = os.path.splitext(downloaded_file)
		new_file = base + '.mp3'
		os.rename(downloaded_file, new_file)
		flash('télécharement términé avec succée','success')
	return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)