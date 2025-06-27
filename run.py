import os
from flask import Flask
from route import route 
def main():
    app = Flask(__name__,template_folder='templates',static_folder='static')
    
    app.config['SECRET_KEY']= 'hoymeenteroquetumamanobleviduadeunguerreroeslachorrademasfamaquepisolatreintaytresyelguerreroquemuriollenodehonornimurionifueguerreroesomeengrupistevos'
    route(app)
    app.run('0.0.0.0', 5000, debug=True) 
main()
