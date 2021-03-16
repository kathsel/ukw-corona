from colorhash import ColorHash
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def add_traces(fig, data, lk_values, 
               modus='neu', 
               zahlenmodus='absolut', 
               columnname='MeldeTag_AnzahlFallNeu', 
               legname='Fälle', 
               grid=(1,1), 
               linetype='solid',
               showlegend=True):
    row, col = grid
    for lk in lk_values:
        y_vals = data.loc[data.Landkreis==lk, columnname]

        if modus=='neu':
            y_vals = y_vals.rolling(window=7).mean()
            if zahlenmodus=='100k':
                y_vals = y_vals*(10**5)/data.loc[data.Landkreis==lk, 'Einwohner']*7

        if modus=='summe':
            y_vals = y_vals.cumsum()

        fig.add_trace(go.Scatter(x=data.index[data.Landkreis==lk],
                                 y=y_vals, 
                                 name=lk + ', ' + legname, 
                                 showlegend=showlegend,
                                 line=dict(dash=linetype, color=ColorHash(lk).hex), legendgroup=lk), 
                                 row=row, col=col)

    return fig


def create_timeline_plot(data, data_value, lk_values, modus, zahlenmodus):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], shared_xaxes=True, vertical_spacing=0.05)

    legnames = {'MeldeTag_AnzahlFallNeu': 'Fälle', 'MeldeTag_AnzahlTodesfallNeu': 'Todesfälle', 'AnzahlGenesenNeu': 'Genesen'}
    linetypes = {'MeldeTag_AnzahlFallNeu': 'solid', 'MeldeTag_AnzahlTodesfallNeu': 'dash', 'AnzahlGenesenNeu': 'dot'}    

    for x in data_value:        
        fig = add_traces(fig, data, lk_values, modus, zahlenmodus, x, legname=legnames[x], grid=(1, 1), linetype=linetypes[x])

    # R-Wert
    fig = add_traces(fig, data, lk_values, modus='R', zahlenmodus='R', columnname='InzidenzFallNeu_7TageSumme_R', grid=(2, 1), showlegend=False)

    fig.update_layout(
        margin=dict(
            l=50,
            r=100,
            b=40,
            t=40
        )  
    )

    return fig


