'''
	Contoh Deloyment untuk Domain Data Science (DS)
	Orbit Future Academy - AI Mastery - KM Batch 3
	Tim Deployment
	2022
'''

# =[Modules dan Packages]========================

from flask import Flask,render_template,request,jsonify
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mplcyberpunk
from sklearn.linear_model import LinearRegression
from seaborn.relational import lineplot
from joblib import load


# =[Variabel Global]=============================

app   = Flask(__name__, static_url_path='/static')
model = None
df = pd.read_csv("adm_data.csv")
df.columns = df.columns.str.replace(' ', '')
data = []
rate = df["ChanceofAdmit"].values
for x in rate:
  if (x >= 0.01 and x < 0.5):    
    data.append("low")
  elif (x >= 0.5 and x <= 0.8):
    data.append("medium")
  elif (x > 0.8 and x <= 1.0):
    data.append("high")  
df['category'] = data
# =[Routing]=====================================

# [Routing untuk Halaman Utama atau Home]	
@app.route("/")
def landing():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/beranda")
def beranda():
    return render_template('index.html')

@app.route("/beranda/aplikasi")
def aplikasi():
    return render_template('testing.html')

@app.route("/beranda/faq")
def faq():
    return render_template('faq.html')

@app.route("/beranda/teams")
def teams():
    return render_template('teams.html')

# [Routing untuk API]	
@app.route("/api/deteksi",methods=['POST'])
def apiDeteksi():
	# Nilai default untuk variabel input atau features (X) ke model
	input_gre = 319.0
	input_toefl  = 118.0
	input_rating = 5.0
	input_sop  = 5.0
	input_lor  = 5.0
	input_cgpa = 9.5
	input_research  = 1.0
	
	if request.method=='POST':
		# Set nilai untuk variabel input atau features (X) berdasarkan input dari pengguna
		input_gre = float(request.form['gre'])
		input_toefl  = float(request.form['toefl'])
		input_rating = float(request.form['rating'])
		input_sop  = float(request.form['sop'])
		input_lor  = float(request.form['lor'])
		input_cgpa = float(request.form['cgpa'])
		input_research  = float(request.form['research'])
		
		# Prediksi kelas atau spesies bunga iris berdasarkan data pengukuran yg diberikan pengguna
		

		df_test = pd.DataFrame(data={
			"GREScore" : [input_gre],
			"TOEFLScore"  : [input_toefl],
			"UniversityRating" : [input_rating],
			"SOP"  : [input_sop],
			"LOR"  : [input_lor],
			"CGPA"  : [input_cgpa],
			"Research"  : [input_research]
		})

		hasil_prediksi = model.predict(df_test[0:1])
		plt.style.use("cyberpunk")
		plt.figure(figsize = (16,8))
		sns.lineplot(data=df, x='ChanceofAdmit', y='ChanceofAdmit', hue='category', palette='light:b')
		sns.scatterplot(x=hasil_prediksi[0:1], y=hasil_prediksi[0:1], s=150, color='cyan', marker='v')
		mplcyberpunk.add_glow_effects()
		plt.axvline(x=hasil_prediksi[0:1], color='r', linestyle='--', ymax=hasil_prediksi[0:1]-0.026)
		plt.axhline(y=hasil_prediksi[0:1], color='g', linestyle='--', xmax=hasil_prediksi[0:1]-0.026)
		
		# Set Path untuk gambar hasil prediksi
		if hasil_prediksi >= 0.01 and hasil_prediksi < 0.5:
			plt.savefig('static/img/eval.png')
			gambar_prediksi = '\static/img/eval.png'
			hasil =  'Low'
			
		elif hasil_prediksi >= 0.5 and hasil_prediksi <= 0.8:
			plt.savefig('static/img/eval2.png')
			gambar_prediksi = '\static/img/eval2.png'
			hasil =  'Medium'
   			
		else:
			plt.savefig('static/img/eval3.png')
			gambar_prediksi = '\static/img/eval3.png'
			hasil =  'High'
			
		
		# Return hasil prediksi dengan format JSON
		class NpEncoder(json.JSONEncoder):
			def default(self, obj):
				if isinstance(obj, np.integer):
					return int(obj)
				if isinstance(obj, np.floating):
					return float(obj)
				if isinstance(obj, np.ndarray):
					return obj.tolist()
				return json.JSONEncoder.default(self, obj)

		hasil_prediksi = json.dumps(f"{np.round(hasil_prediksi[0] * 100,2)} %", cls=NpEncoder)
		return jsonify({
			"prediksi": hasil_prediksi,
			"kategori" : hasil,
			"gambar_prediksi" : gambar_prediksi
		})
  

# =[Main]========================================

if __name__ == '__main__':
	
	# Load model yang telah ditraining
	model = load('model_Reg.model')

	# Run Flask di localhost 
	app.run(host='0.0.0.0', port=5001, debug=True)
	
	


