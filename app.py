from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response, jsonify
import os
import json
import ast
import traceback

app = Flask(__name__)

#def createReport(jsonFileContainingData):


@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route("/report/<reportNum>", methods=["GET", "POST"])
def goToReport(reportNum):
	if request.method == 'POST':
		with open('{}.json'.format(reportNum), 'w') as outfile:
		    json.dump(request.data, outfile)
	else:
		try:
			dictionaryFile = json.load(open("{}.json".format(reportNum)))
			try:
				e = json.loads(str(dictionaryFile))
				dictionaryFile = e
			except:
				pass
			print dictionaryFile
			levensh = dictionaryFile["Levenshtein"]
			print levensh
			#return jsonify(dictionaryFile)
			if levensh > 75:
				Diagnosis = "General Fluency/Vocal Disorder"
			elif dictionaryFile["Stutter"] > 5:
				Diagnosis = "Stuttering Speech Disorder"
			elif dictionaryFile["Partial"] > 5:
				Diagnosis = "Tangential Speech Disorder"
			else:
				Diagnosis = "No Speech Developmental Challenges Detected"
			return render_template("report.html", Diagnosis=Diagnosis, levRange=range(1,len(dictionaryFile["AllLev"])+1), allSent=dictionaryFile["AllSentences"], LEVData=dictionaryFile["AllLev"], reportNum=reportNum, Data=dictionaryFile, levMax=1000-dictionaryFile['Levenshtein'])
		except Exception as exp:
			print traceback.print_exc()
			return "<h1>Report for {} not generated</h1>".format(reportNum)


@app.route("/", methods=["POST"])
def getReport():
	print("Working")
	print str(request.form.items())
	for key, quant in request.form.items():
		print("{} = {}".format(key, quant))
	return redirect(url_for('goToReport', reportNum=quant))



if __name__ == "__main__":
	app.run()
