import pandas as pd
import numpy as np
import sys
import re
import matplotlib.pyplot as plt
import gender_guesser.detector as gender
import requests
import seaborn as sns
import pycountry
import plotly.express as px
import folium


def abrir_csv(path): 
    #para abir un csv
    return pd.read_csv(path, index_col = 0 )

def guardar_csv(df, path_name): 
    #guardar csv con el nombre y el path
    return df.to_csv(path_name)

def ver_nulos(df):
    #ver % de nulos de columnas de un dataframe con nulos
    df_nul=pd.DataFrame((df.isnull().sum() * 100) / df.shape[0])
    return df_nul[df_nul[0]>0] 

def merge_rightleft(df1, df2, df1_on, df2_on, merge_type):
    #merge dos dataframe con left_on y right_on
    df_merge=df1.merge(df2, left_on= df1_on, right_on=df2_on, how=merge_type)

def merge_df(df1, df2, on, merge_type):
    #merge dos dataframe 
    df_merge=df1.merge(df2, left_on= df1_on, right_on=df2_on, how=merge_type)
    
def str_genre(column):
    #sacar a traves de regex cuando tienes una "lista dentro" de un string ej:"['indie rock italiano', 'italian pop']" el primer string:indie rock italiano
    listi=[]
    for i in column:
        y= re.findall("[a-z]+.*\w+", str(i))
        try:
            listi.append(y[0])
        except:
            listi.append(y)
    return str(listi[0])

def asociar_genero(df_genero, list_genero):
    #asociar un genero de una lista list_genero a un genero mas especifico
    from fuzzywuzzy import process, fuzz
    maximo = 0
    genero_encontrado = None
    for genre in list_genero:
        if genre in df_genero:
            genero_encontrado = genre
        else:
            parecido = fuzz.ratio(df_genero, genre)
            if parecido > maximo:
                maximo = parecido
    if genero_encontrado is not None:
        return genero_encontrado
    elif maximo > 50:
        return genero_encontrado
    else:
        return "other"  

def info_mes(x):
        #sacar el mes de una fecha con formato %Y-%m-%d
        fecha_str = x
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
        mes = fecha_obj.strftime("%B")
        return mes

def info_año(x):
        #sacar el año de una fecha con formato %Y-%m-%d
        fecha = datetime.strptime(x, "%Y-%m-%d")
        año = fecha.strftime("%Y")
        return año

def estacion(mes):
    #definir la estacion a la que pertenece cada mes
    if mes in ["December", "January", "February"]:
        return "Winter"
    elif mes in ["March", "April", "May"]:
        return "Spring"
    elif mes in ["June", "July", "August"]:
        return "Summer"
    elif mes in ["September", "October", "November"]:
        return "Autumn"
    
def oth_gender(columna_persona,columna_genero, persona_mujer, persona_hombre):
    #modificar el genero de unas personas determinadas de una columna "genero"
    if x==persona_mujer:
        gender="female"
    elif x==persona_hombre:
        gender="male"
    else:
        gender=y
    return gender

def opciones_webscaping():
    opciones= Options()
    opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
    #para ocultarme como robot
    opciones.add_experimental_option('useAutomationExtension', False)
    opciones.add_argument('--start-maximized') #empezar maximizado
    opciones.add_argument('user.data-dir=selenium') #guarda las cookies
    opciones.add_argument('--incognito')#incognito window


def mapa(df, latitude, longitud, location):
    mapa = folium.Map()
    for index, row in df_map.iterrows():
        folium.Marker([row[latitude], row[longitud]],
                      radius=5, 
                      tooltip = row[location],
                      icon=folium.Icon(color='purple', icon='cloud')).add_to(mapa)
    return mapa

def generation_2022(edad):
    #determinar la generacion a partir de la edad
    if edad < 25:
        return "Generation Z"
    elif edad < 40:
        return "Millennial"
    elif edad < 60:
        return "Generation X"
    elif edad < 80:
        return "Baby Boomer"
    else:
        return "Silent"

def decade_song(date):
    #sacar la decada en la que se encuentra una fecha con formato: %Y-%m-%d
    try:
        fecha = date.split("-")[0]
        año = datetime.strptime(fecha, '%Y')
        decade = str(año.year // 10 * 10)+"s"
    except:
        decade= np.nan
    return decade

def display_foto(imagen, tamaño):
    #para display una imagen con el nombre del archivo de la imagen
    from IPython.display import display
    from IPython.display import Image
    return display(Image(filename=imagen, width=tamaño)) 

def guess_gender(name_list):
    #adivinar el genero segun el nombre, suele ayudar cuando con nombres en ingles
    guess = {"Gender": []}
    d = gender.Detector()
    for name in name_list:
        g=d.get_gender(name)
        guess["Gender"].append(g)
    return guess

def grafico_dispersion(column1, column2, x_label, y_label, title):
    #grafico dispersion con dos columnas
    plt.scatter(column1, column2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
    

def grafico_barras_1(df_column, xlabel, ylabel, title):
    #grafico de barras con una variable y su conteo
    df_column_count = df_column.value_counts()
    df_column_count.plot(kind='bar', color='green')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
    
def barplot_grupos(df_group, variable_x, groupo_variables, xlabel, ylabel, title):
    df_graf = pd.melt(df_group, id_vars=variable_x, value_vars=groupo_variables)
    sns.barplot(x=variable_x, y='value', hue='variable', data=df_graf)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def quesito(data, titulo):
    data.plot.pie(autopct='%1.1f%%')
    plt.title(titulo)
    plt.legend(bbox_to_anchor=(1.2, 1))
    plt.show()

def country_code(country_code):
    country_name=[]
    for code in country_code:
        country = pycountry.countries.get(alpha_2=code)
        country_name.append(country.name)
    return country_name

def mapa_calor(df, countries, conteo, titulo):
    fig = px.choropleth(df, locations=countries, locationmode='country names',
                    color=conteo, title=titulo,
                    color_continuous_scale='Viridis', range_color=[0, 500])
    fig.show()
    return fig

def barras_interactivas(df, x_data, y_data, extra_data, titulo):
    fig = px.bar(df, x=x_data, y=y_data,
    hover_data=extra_data, title=titulo, color_discrete_sequence=['red'])
    fig.show()
    return fig

