from tokenize import group
from flask import Flask, render_template

import pandas as pd
import json
import plotly
import plotly.express as px

import requests


app = Flask(__name__)


@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    #Tickets

    tickets = requests.get("http://192.168.10.80:5011/api/tickets")
    list_tickets_users = tickets.json()["tickets"]

    tickets_closed = 0
    for value in list_tickets_users:
        tickets_closed += value['closed']


    tickets = requests.get("http://192.168.10.80:5011/api/all_tickets")
    all_tickets = tickets.json()["tickets"]
    
    df = pd.DataFrame.from_dict(list_tickets_users)

    servers_disks = requests.get('http://192.168.10.80:5013/api/disks')
    all_server_disks = servers_disks.json()['servers']
    
    
    #print(df.head())
      
    fig_tickets = px.bar(df, x='user', y='closed', color='user', width=800, height=320)
    
    graphJSON_tickets = json.dumps(fig_tickets, cls=plotly.utils.PlotlyJSONEncoder)


    # Trafico

    trafico_ = requests.get("http://192.168.10.80:5012/api/trafico")
    trafico = trafico_.json()["result"]

    trafico_ayer_ = requests.get("http://192.168.10.80:5012/api/trafico/ayer")
    trafico_ayer = "{:,}".format(trafico_ayer_.json()["result"])

    trafico_anno_ = requests.get("http://192.168.10.80:5012/api/trafico/anno")
    trafico_anno = "{:,}".format(trafico_anno_.json()["result"])

    df = pd.DataFrame.from_dict(trafico)

    fig_traffic = px.bar(df, x='dia', y='trafico', color='semana', barmode='group', width=800, height=320)

    graphJSON_traffic = json.dumps(fig_traffic, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graphJSON_tickets=graphJSON_tickets, 
                                        graphJSON_traffic=graphJSON_traffic, 
                                        all_tickets=all_tickets, 
                                        tickets_closed=tickets_closed, 
                                        all_server_disks=all_server_disks, 
                                        trafico_ayer=trafico_ayer,
                                        trafico_anno=trafico_anno
                                        )


if __name__ == "__main__":
    app.run(debug=True, port=5001)