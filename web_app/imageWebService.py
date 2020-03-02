import requests
import json
from mongoengine import *
from PIL import Image
from io import BytesIO
from flask import Flask,  request
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)
# Es el endpoint que se encarga de consultar la salud de la DB
@app.route('/health',methods=['GET'])
def health_check():
  from pymongo import MongoClient
  try:
    mongoDataBaseName=config['db_settings']['mongoDataBaseName']
    mongoDataBaseConnectString=config['db_settings']['mongoDataBaseConnectString']
    client = MongoClient(mongoDataBaseConnectString,connectTimeoutMS=5000,serverSelectionTimeoutMS=5000)

    db = client.health

    status = db.command("whatsmyuri")
  except:
    status="Connection error"
    return(status)
  return(status)

# Es el endpoint que se encarga de subir las imagenes
@app.route('/push',methods=['POST'])
def push_image():
  if (request.method == 'POST'):

    # Leo parametros de configuracion general de la app 
    cropSize=config['image_settings']['cropSize']
    outputFormat=config['image_settings']['outputFormat']
    mongoDataBaseName=config['db_settings']['mongoDataBaseName']
    mongoDataBaseConnectString=config['db_settings']['mongoDataBaseConnectString']

    # Tomo la url de la imagen a subir (JSON)
    obj = request.get_json()
    imageURL=obj["URL"]

    # Hago el request de la imagen
    r = requests.get(imageURL)

    # Leo la imagen y la re-escalo
    ingestFile = BytesIO(r.content)
    i = Image.open(ingestFile)

    #Bug a arreglar, no puedo usar el valor del config file, espero arreglar esto antes de entregarlo XD
    cs=(600,600)
    i.thumbnail(cs)
    #i.thumbnail(cropSize)

    #Grabo la imagen tratada en memoria y la convierto a JPEG
    tmp=BytesIO()
    jpegConvert=i.convert('RGB')
    jpegConvert.save(tmp,outputFormat)


  #Me conecto a la DB para persistir el registro
  connect(
    db=mongoDataBaseName,
    host=mongoDataBaseConnectString
  )

  #Defino un schema para guardar el documento
  class doc(Document):
    url = StringField(required=True)
    image = ImageField(max_length=50)

  d=doc(url=imageURL)
  d.image.replace(tmp,filename=imageURL)
  d.save()

  return(imageURL)
