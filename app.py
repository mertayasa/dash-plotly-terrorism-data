import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

app = dash.Dash()
server = app.server

df = pd.read_csv('globalterrorismdb.csv', error_bad_lines=False, sep=';', encoding='UTF-8')


dfcase = df.groupby('iyear').size().reset_index(name = 'case')
dfkill = df.groupby(['country_txt','iyear'])['nkill'].agg('sum').reset_index(name = 'kill')
dfattack = df.groupby(['attacktype1_txt']).size().reset_index(name = 'total')
dfgname = df.drop(df.index[df['gname'] == "Unknown"], inplace = True)
dfgname = df['gname'].value_counts()[:10].sort_values(ascending=False).reset_index(name = 'total')


bar_case = px.bar(
    dfcase,
    x=dfcase['iyear'],
    y=dfcase['case'],
    labels={'iyear':"Year", "case":"Case"},
    template='plotly_dark',
    title='Case By Year ?'
)

line_kill = px.line(
    dfkill,
    x=dfkill['iyear'],
    y=dfkill['kill'],
    color=dfkill['country_txt'],
    labels={'iyear':"Year", "kill":"People Killed", "country_txt":"Country"},
    template='plotly_dark',
    title='People Killed In Every Country ?'
)

pie_chart_attack = px.pie(
        data_frame=dfattack,
        values=dfattack['total'],
        names='attacktype1_txt',
        color='attacktype1_txt',
        labels={"attacktype1_txt":"Attack Type", "total":"Case"},
        title='How Terrorist Attack ?',
        template='plotly_dark',
        )

pie_chart_group = px.pie(
        data_frame=dfgname,
        values=dfgname['total'],
        names='index',
        color='index',
        labels={"index":"Group Name", "total":"Case"},
        title='10 Most Dangerous Terrorist Group (Based on their case) ?',
        template='plotly_dark',
        )

app.layout = html.Div([
    html.H1('Global Terrorism Attack 1970 - 2017', style={"text-align": "center", "font-family":"sans-serif", "color":"white", "background-color":"black", "margin-bottom":"0", "margin-top":"0", "padding-top":"10px"}),
    dcc.Graph(figure=bar_case),
    dcc.Graph(figure=line_kill),
    dcc.Graph(figure=pie_chart_attack),
    dcc.Graph(figure=pie_chart_group)
])

if __name__ == '__main__':
    app.run_server(debug=True)
