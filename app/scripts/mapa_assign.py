
def tria_mapa(ass):
    dic_ass_mapa = {'Mecànica Fonamental':'mapaMF','Àlgebra Lineal':'mapaAL',"Fonaments d'Informàtica":'mapaFI','Química 1':'mapaQ1','Càlcul 1':'mapaC1',
        'Expressió Gràfica':'mapaEG','Termodinàmica Fonamental':'mapaTF','Química 2':'mapaQ2','Càlcul 2':'mapaC2','Geometria':'mapaG'}

    if ass in dic_ass_mapa:
        return f'/static/{dic_ass_mapa[ass]}.html'
    else:
        return False

def tradueix(ass):
    dic_ass_codi = {'Àlgebra Lineal':'240011','Mecànica Fonamental':'240013',"Fonaments d'Informàtica":'240015','Química 1':'240014','Càlcul 1':'240012',
        'Expressió Gràfica':'240025','Termodinàmica Fonamental':'240023','Química 2':'240024','Càlcul 2':'240022','Geometria':'240021'}
    
    if ass in dic_ass_codi:
        return f'app/scripts/CPCass/{dic_ass_codi[ass]}CPC.csv'
    else:
        return None

def grafic(ass):
    l=['/static/grafiques/Ch*BCN Ciutat.html','/static/grafiques/Ch*BCN Sud.html','/static/grafiques/Ch*BCN Nord.html','/static/grafiques/Ch*Lleida.html','/static/grafiques/Ch*Tarragona.html','/static/grafiques/Ch*Girona.html']
    dic_ch = {'Mecànica Fonamental':'MF','Àlgebra Lineal':'ÀL',"Fonaments d'Informàtica":'FI','Química 1':'Q1','Càlcul 1':'C1',
        'Expressió Gràfica':'EG','Termodinàmica Fonamental':' TF','Química 2':'Q2','Càlcul 2':'C2','Geometria':'G'}
    l2=[]
    if ass in dic_ch:
        for e in l:
            a,b = e.split('*')
            sp = dic_ch[ass]
            cc = a + sp + b
            l2.append(cc)   
        return l2
    else:
        return None
       