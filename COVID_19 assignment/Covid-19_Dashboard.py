# import libraries:
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash,html,dcc,callback,Input,Output,dash_table
import dash_bootstrap_components as dbc


#load Data:
df=pd.read_csv('covid_19_cleaned.csv')
# for pie plot
confirmed_pie=df.loc[:,['Deaths', 'Recovered', 'Active']].sum()

# q1: what is average ratio of each Death,active,recoverd for each month?
q1=df.groupby('Month-Record')[['DeathsRatio','RecoveredRatio','ActiveRatio']].mean().reset_index()

# q2: how many cases Deathed or recovered or active for each month?
q2=df.groupby('Month-Record')[['Deaths', 'Recovered', 'Active']].sum().reset_index()

# q3: how many case is recorded for each organization:
q3=df.groupby('WhoRegion')[['Deaths', 'Recovered', 'Active']].sum().reset_index()

# q4: what is average ratio of each Death,active,recoverd for each WHO?
q4=df.groupby('WhoRegion')[['DeathsRatio','RecoveredRatio','ActiveRatio']].mean().reset_index()

# create app:

app=Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])


# create layout and styling:


app.layout=dbc.Container([

    #1 title:
    dbc.Row(
        [
            html.H1('Covid-19 Dashboard ', style={'color':'green'}),
            html.Hr(),
            html.P('This Page Include Dashboard Data Anlysis for Covid-19 Dataset '),
            html.Hr()
        ] 
    ),
# -----------------------------------------------------------------------
    #2- Data Representation:
    dbc.Row([ 
            html.Div([
               html.H3('Dataset After Preprocessing:',style={'color':'green'}),
               html.H6(f'=== Dataset Has No.of Columns = {df.shape[1]} ===',style={'color':'white','tectAlign':'center'}),
               html.H6(f'=== Dataset Has No.of Rows = {df.shape[0]} ===',style={'color':'white','tectAlign':'center'}),
               dash_table.DataTable(
                                    data=df.to_dict('records'),
                                    page_size=5,
                                    style_cell={'textAlign': 'center'},  
                                    style_header={'backgroundColor': 'green', 'fontWeight': 'bold'},  
                                    style_data={'backgroundColor': '#2f2e2e', 'border': '1px solid grey'} 
                                    ),
                
            
                      ]),
            html.Hr()

                ]),
#----------------------------------------------------------------------------- 
    #3- EDA:
    # -----(histogram and boxplot)-----
    dbc.Row([ 
        # Vertical line 1:
        dbc.Col(
            html.Div(style={'border-left': '1px solid gray', 'height': '100%'}),
             width=0
             ),
        
        # 1- histogram:
        dbc.Col(
            html.Div([

            html.H4('Histogram Graph:',style={'color':'green'}),
            dcc.RadioItems(options=['Confirmed', 'Deaths', 'Recovered', 'Active','WhoRegion','Country', 'City','DeathsRatio','RecoveredRatio', 'ActiveRatio','Month-Record'],value='Recovered',id='col_selected',inline=True),
            dcc.Graph(figure={},id='histogram_graph')

            ]),width=5

               ),
        # Vertical line 2:
        dbc.Col(
            html.Div(style={'border-left': '1px solid gray', 'height': '100%'}),
             width=0
             ),
        # Vertical line 3:
        dbc.Col(
            html.Div(style={'border-right': '1px solid gray', 'height': '100%'}),
             width=0
             ),
        # 2- Box Plot:
        dbc.Col(html.Div([
            html.H4('Box-Plot :',style={'color':'green'}),
            dcc.RadioItems(options=['Confirmed', 'Deaths', 'Recovered', 'Active','WhoRegion','Country', 'City','DeathsRatio','RecoveredRatio', 'ActiveRatio','Month-Record'],value='Recovered',id='col_selected_box',inline=True),
            dcc.Graph(figure={},id='box_plot')

        ]),width=5

        ),
        dbc.Col(
            html.Div(style={'border-right': '1px solid gray', 'height': '100%'}),
             width=0
             ),
            
        html.Hr()
            
            
            ]),

    # ----ScatterMap-----
    dbc.Row([
        html.Div(html.H4('Distribution of Confirmed cases around the world :\n',style={'color':'green','textAlign':'center'})),
        dbc.Col(
            html.Div(style={'border-left': '1px solid gray', 'height': '100%'}),
             width=0
             ),
        dbc.Col(
        html.Div([
                
                dcc.Graph(
                    figure=px.scatter_map(
                                        df,
                                        lon='Long',
                                        lat='Lat',
                                        color='WhoRegion',
                                        hover_name='WhoRegion',
                                        hover_data=['Confirmed','Deaths','Recovered','Active','Country','City'],
                                        zoom=0,
                                        title='Confirmed cases Around the world '.title(),
                                        template='plotly_dark',
                                        width=761,
                                        height=500

                                    )

                        )
                    


    ]),width=6),
    dbc.Col(
            html.Div(style={'border-right': '1px solid gray', 'height': '100%'}),
             width=0
            ),
    dbc.Col(
            html.Div(style={'border-left': '1px solid gray', 'height': '100%'}),
             width=0
            ),
    dbc.Col(
        html.Div([
                dcc.Graph(
                            figure=px.sunburst(
                                    df,path=['WhoRegion','Country','City'],
                                    template='plotly_dark',
                                    values='Confirmed',
                                    hover_name='WhoRegion',
                                    title='All Countries , Cities and the WHO those Follwed ',
                                    # width=550,
                                    height=500
                                )

                        )
                    


    ]),width=5),
    dbc.Col(
            html.Div(style={'border-right': '1px solid gray', 'height': '100%'}),
             width=0
            ),
    html.Hr()
    

    
    
]),

    #----------Pie to precentage -> Deaths,Recoverd,Active--------
    dbc.Row(html.Div([       
        dbc.Col([
            html.H4('Precentage of Deaths,Recoverd, and Active Cases :\n',style={'color':'green'}),
            dcc.Graph(
                        figure=px.pie(
                            confirmed_pie,
                            names=['Deaths', 'Recovered', 'Active'],
                            values=confirmed_pie.values,
                            title='Percentage value of "Deaths, Recovered, Active" for 2020',
                            labels=['Deaths', 'Recovered', 'Active'],
                            template='plotly_dark',
                
                            height=550,
                        
                            hole=.5
                            
                        )
                    )
    ]),

        html.Hr()

    ])),
    #----------Line plot -> DeathsRatio,RecoverdRatio,ActiveRatio--------
    dbc.Row(html.Div([       
        dbc.Col([
            html.H4('Average of each DeathsRatio,RecoverdRatio and ActiveRatio Per Month :\n',style={'color':'green'}),
            dcc.Graph(
                        figure=px.line(
                                        q1,
                                        x='Month-Record',
                                        y=['DeathsRatio','RecoveredRatio','ActiveRatio'],
                                        template='plotly_dark',
                                        title='Avg of DR , RR and AC for each month for 2020'
                                    )
                    )
    ]),

        html.Hr()

    ])),

    #----------Bar plot -> to show Deaths,Active ,Recoverd cases per month--------
    dbc.Row(html.Div([       
        dbc.Col([
            html.H4('No.Of Deaths,Recoverd and Active Cases Per Month :\n',style={'color':'green'}),
            dcc.Graph(
                        figure=px.bar(
                                        q2,
                                        x='Month-Record',
                                        y=['Deaths', 'Recovered', 'Active'],
                                        template='plotly_dark',
                                        title='Total cases D,R,A for each month for 2020',
                                        barmode='group'   
                                    )
                    )
    ]),

        html.Hr()

    ])),
        #----------Bar plot -> to show Deaths,Active ,Recoverd cases per Who--------
    dbc.Row(html.Div([       
        dbc.Col([
            html.H4('No.Of Deaths,Recoverd and Active Cases Per WHO :\n',style={'color':'green'}),
            dcc.Graph(
                        figure=px.bar(
                                        q3,
                                        y='WhoRegion',
                                        x=['Deaths', 'Recovered', 'Active'],
                                        template='plotly_dark',
                                        title='Total cases D,R,A for each WHO ',
                                        barmode='group',
                                        orientation='h' ,  
                                    )
                    )
    ]),

        html.Hr()

    ])),

            #----------Bar plot -> to show Average DeathsRatio,RecoverdRatio,ActiveRatio cases per Who--------
    dbc.Row(html.Div([       
        dbc.Col([
            html.H4('Average DeathsRatio,RecoverdRatio,ActiveRatio cases per Who :\n',style={'color':'green'}),
            dcc.Graph(
                        figure=px.bar(
                                        q4,
                                        x='WhoRegion',
                                        y=['DeathsRatio','RecoveredRatio','ActiveRatio'],
                                        template='plotly_dark',
                                        title='Avg of DR,RR,AR for each WHO ',
                                        barmode='group',
                                    )
                    )
    ]),

        html.Hr()

    ])),
        
])

@callback(
    Output(component_id='histogram_graph',component_property='figure'),
    Input(component_id='col_selected',component_property='value')
)

def update_histogram(col_selected):
    num_cols=['Confirmed', 'Deaths', 'Recovered', 'Active','DeathsRatio','RecoveredRatio', 'ActiveRatio','Month-Record']
    top10_country=df.Country.value_counts().nlargest(10).index
    top10_country_df=df[df.Country.isin(top10_country)]
    top10_city=df.City.value_counts().nlargest(10).index 
    top10_city_df=df[df.City.isin(top10_city)]               
    if col_selected in num_cols :
        fig=px.histogram(
            df,
            x=col_selected,
            color_discrete_sequence=['green'],
            nbins=30,
            template='plotly_dark',
            title='Distribution of '+col_selected
        )
        
    if col_selected =='Country':
        fig=px.histogram(
            top10_country_df,
            x='Country',
            color='Country',
            template='plotly_dark',
            title='Top_10 '+col_selected+' Distribution'
        )
    if col_selected =='WhoRegion':
        fig=px.histogram(
            df,
            x='WhoRegion',
            color='WhoRegion',
            template='plotly_dark',
            title='WHO Distribution'
        )
    if col_selected =='City':
        fig=px.histogram(
            top10_city_df,
            x='City',
            color='City',
            template='plotly_dark',
            title='Top_10 '+col_selected+' Distribution'
        )
    return fig
        
@callback(
    Output(component_id='box_plot',component_property='figure'),
    Input(component_id='col_selected_box',component_property='value')
)

def update_box(col_selected):
    num_cols=['Confirmed', 'Deaths', 'Recovered', 'Active','DeathsRatio','RecoveredRatio', 'ActiveRatio','Month-Record']
    top10_country=df.Country.value_counts().nlargest(10).index
    top10_country_df=df[df.Country.isin(top10_country)]
    top10_city=df.City.value_counts().nlargest(10).index 
    top10_city_df=df[df.City.isin(top10_city)]               
    if col_selected in num_cols :
        fig=px.box(
            df,
            y=col_selected,
            color_discrete_sequence=['green'],
            template='plotly_dark',
            title='Box-Plot of '+col_selected
        )
        
    if col_selected =='Country':
        fig=px.box(
            top10_country_df,
            x='Country',
            y='Confirmed',
            color='Country',
            template='plotly_dark',
            title='Top_10 '+col_selected+' Boxplot'
        )
    if col_selected =='WhoRegion':
        fig=px.box(
            df,
            x='WhoRegion',
            y='Confirmed',
            color='WhoRegion',
            template='plotly_dark',
            title='WHO Box-Plot'
        )
    if col_selected =='City':
        fig=px.box(
            top10_city_df,
            x='City',
            y='Confirmed',
            color='City',
            template='plotly_dark',
            title='Top_10 '+col_selected+' Boxplot'
        )
    return fig

# Run app:
if __name__=='__main__':
    app.run_server(debug=True)










