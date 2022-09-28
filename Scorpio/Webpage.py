import os
from flask import Flask,render_template
import System_readings

content =""


app = Flask(__name__)


path=os.path.abspath("Scorpio/system_data_readings.txt")


@app.route('/')
def Main():

    System_readings.Main()

    with open(f"{path}","r", errors="ignore") as file:
        content= file.read()
        
    return render_template('index.html', title='Home page', content=content)




if __name__ == "__main__":
    app.run()
    