from flask import render_template, request
from app import app

from .scripts.mapa_assign import *
from .scripts.mapa_enlinia import *

@app.route('/')
@app.route('/home')
def home():

    return render_template('home.html')

@app.route('/mapa')
def mapa():

    m = grafic('Mecànica Fonamental')
    return render_template('mapa_cpc.html', ass = 'Mecànica Fonamental', m = m, resultat ='/static/mapaMF.html')

@app.route('/mapa_cpc', methods=['GET','POST'])
def mapa_cpc():

    ass = request.form.get('ass')
    resultat = tria_mapa(ass)
    m = grafic(ass)

    if m and resultat:
        r = render_template('mapa_cpc.html', ass = ass, m = m, resultat = resultat)
    else:
        r = render_template('mapa_cpc.html', ass = '', m = None, resultat = None)
    
    return r


@app.route('/mapa_enlinia', methods=['GET','POST'])
def mapa_onair():

    llista_ass = request.form.getlist('ass')
    if llista_ass:
        mapa_enlinia(llista_ass)
        resultat = True
    else:
        resultat = False

    s= ", ".join(llista_ass)

    return render_template('mapa_enlinia.html', ass = s, resultat = resultat)
    
@app.route('/sobre_nosaltres')
def sobre_nosaltres():

    return render_template('sobre_nosaltres.html')

@app.route('/mapa_mix')
def mapa_mix():
    
    return render_template('mapa_mix.html')
