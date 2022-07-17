# -*- coding: utf-8 -*-
"""
Created on Sat May 18 20:05:51 2019

This is a web interface for a simple python program

@author: Wladimir
"""

from flask import Flask, render_template, request, flash, url_for
from blastinstructor_class import blast

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
map = {"RIGHT" : "%MXtFWDt20t$", "LEFT" : "%MXtBWDt20t$" ,\
       "UP" : "%MYtFWDt20t$", "DOWN" : "%MYtBWDt20t$" }

@app.route("/")
def index():
    
    return render_template('home.html')

@app.route("/disp", methods = ["POST", "GET"])
def disp():
    if request.method == 'POST':
        result = request.form
    set()
    spacing = 2
    g = blast(int(width), int(length), spacing, int(time))
    g.main()
    flash('Command has been sent')
    return render_template('disp.html', result=result, w = width, l = length, t = time)


@app.route("/move")
def move():
    return render_template('move.html')

@app.route("/move/request", methods = ["POST"])
def move_req():
    spacing = 2
    g = blast(int(width), int(length), spacing, int(time))
    req = request.get_json()
    print(req)
    g.que.put(map[req])
    g.main()
        
    return render_template('home.html')

def set():
    global width, length, time
    width = request.form['width']
    length = request.form['length']
    time = request.form['time']

if __name__ == '__main__':
    width = 0
    length = 0
    time = 0
    #app.run(debug=True)
    app.run(debug=True,host='192.168.178.20')