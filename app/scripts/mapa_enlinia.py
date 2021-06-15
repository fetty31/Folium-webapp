import folium as f
import branca
import pandas as pd
import json
from folium.plugins import MousePosition, Fullscreen, Search
from .mapa_assign import *
import time 

def mapa_enlinia(llista_ass):
    start = time.time()
    
    def style_function(feature):
        nota = notes_series.get(str(feature['properties']['COD_POSTAL']), None)
        return {"fillOpacity": 0.7,"lineOpacity":0.8,"weight": 1,"color":'black',"fillColor": "black" if nota is None else colorscale(nota)}
    
    llista_df = []
    for ass in llista_ass:
        fitxer = tradueix(ass)
        if fitxer:
            with open(fitxer,'r') as f_csv:
                df = pd.read_csv(f_csv,dtype={'CPC':str})
                llista_df.append(df)
    
    df2 = pd.concat(llista_df)
    df2 = df2.groupby(['CPC'],as_index=False).mean()
    df2 = df2.drop(['ASS','std','min','max'],axis=1)
    df2 = df2.rename(columns={"CPC": "COD_POSTAL",'mean':'MITJANA','count':'ALUMNES'})

    m = f.Map(location=[41.71,1.84], tiles=None, zoom_start=8, overlay=False)
        

    colorscale = branca.colormap.LinearColormap(colors=['#f03b20', '#fec44f','#31a354'],vmin=0,vmax=10)#funció per donar color segons la nota
    notes_series = df2.set_index("COD_POSTAL")["MITJANA"] #pandas.series cp-notes per style_function

    df_taula = df2.rename(columns={'COD_POSTAL':'CODI POSTAL'})

    cp_style = "font-size: 15px; font-weight: bold" #estil de lletra GeoJsonPopup

    Tooltip = f.features.GeoJsonTooltip(['COD_POSTAL'],style=cp_style,labels=False,sticky=True)

    with open('app/scripts/CATALUNYA.geojson','r') as data:
        data1 = data.read()
        geojson = f.GeoJson(data=data1,
                                control=False,
                                name='Catalunya',
                                style_function=style_function,
                                tooltip=Tooltip,
                                highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                                zoom_on_click = True).add_to(m)
    
    with open('app/scripts/coordinates.json','r') as c:
        coordinates = json.load(c)
    
    for i in df2.index:
        cp = str(df2.iloc[i]['COD_POSTAL'])
        nota = notes_series.get(cp, None)
        try:
            data2 = {"type": "FeatureCollection",
                        "features": [{ "type": "Feature", "properties": {"COD_POSTAL": cp}, "geometry": {"type": "Polygon",
                                        "coordinates": coordinates[cp]} 
                                        }] }
            Tooltip = f.features.GeoJsonTooltip(['COD_POSTAL'],style=cp_style,labels=False,sticky=True)
            gjson = f.GeoJson(data=data2,
                            control=False,
                            style_function= lambda x:{'fillOpacity':0,
                                                        'weight':0,
                                                        'fillcolor':colorscale(nota),
                                                        'color': 'black'},
                            highlight_function=lambda x:{'weight':3,'fillColor':'grey'},
                            zoom_on_click = False,
                            tooltip = Tooltip
                                                )

            #taules html
            tau=df_taula[df_taula['CODI POSTAL']==cp]
            classes="table table-striped table-hover table-condensed table-responsive"
            pop = tau.to_html(buf=None, columns=None, col_space=100, header=True, index=False, na_rep='0', formatters=None,classes=classes, float_format=None, sparsify=None, index_names=True, justify='center', bold_rows=True, escape=True, max_rows=None, max_cols=None, show_dimensions=False, notebook=False, decimal='.', border=3, table_id=None)
            popup = f.Popup(pop)
                

            gjson.add_child(popup)
            gjson.add_to(geojson)
            
        except KeyError as e:
            pass

    colormap = branca.colormap.LinearColormap(colors=['#f03b20', '#fec44f','#31a354']).scale( 0,10 ).to_step(n=10)
    colormap.caption = 'Notes per codi postal'
    colormap.add_to(m) #afegir una llegenda al mapa amb els colors de l'escala YlOrRd

    f.TileLayer('cartodbpositron',overlay=False,name="mapa clar").add_to(m)
    f.TileLayer('OpenStreetMap',overlay=False,name='mapa a color').add_to(m)
    f.TileLayer('cartodbdark_matter',overlay=False,name="mapa fosc").add_to(m) #3 estils de mapa

    f.LayerControl(collapsed=False).add_to(m) #afegir layer control (llegenda interactiva)

    fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    MousePosition(separator=' | ',lat_formatter=fmtr, lng_formatter=fmtr,position='bottomleft').add_to(m) #poder veure les coordenades del cursor en el mapa

    Fullscreen(position='topleft', title='Pantalla completa', title_cancel='Sortir de la pantalla completa').add_to(m)

    Search(geojson, search_label='COD_POSTAL', geom_type='Polygon', position='topleft', placeholder='Buscar Codi Postal',collapsed=True).add_to(m)
    #barra de busqueda de CPs

    stop = time.time()

    print('time: {}'.format(stop-start))

    m.save('app/templates/mapa_mix.html')
    
    
    
    