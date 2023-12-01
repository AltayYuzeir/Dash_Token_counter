#----------- Dash infrastructure Packages -------------#
from dash import Dash, html, callback, dcc  #,dash_table,
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import dash_mantine_components as dmc # buttons with icons
from dash_iconify import DashIconify # icons for dash
import webbrowser
from threading import Timer

#----------- Additional Packages -------------#

import tiktoken

#---------- Variables ------------#
model_names = ["gpt-4", "gpt-3.5-turbo", "text-embedding-ada-002", 
               "text-davinci-002", "text-davinci-003", "davinci" ]

#--------------- App ---------------#
external_stylesheets = [dbc.themes.CERULEAN] # needed for dbc to work

app = Dash(__name__,  external_stylesheets=external_stylesheets)
app.title = "Token Counter"
#app._favicon = "sigma.ico"

#------------- UI ---------------#
app.layout = dbc.Container([
 
   html.Br(),
   dbc.Row([
       dbc.Col([
          dbc.Label("Paste text:", style = {"color":"white"}),
    dcc.Textarea(
         id='textarea-text',
         placeholder="Please paste your text here",
         style={ "width":"100%",'height': 250, "resize":"vertical"}
     )], width = {"size": 10, "offset": 1})
    
    ]),
   html.Br(),
   dbc.Row([
       dbc.Col([
           dbc.Label("Please select model:", style = {"color":"white", "text-align":"justify"}),
           ], width = {"size": 2, "offset": 5}),
       dbc.Col([
           dcc.RadioItems(id = "radioitems-model-name",options=model_names, inline = True,
                          value = model_names[0], 
                          labelStyle={"margin-right": "20px", "color":"white"},
                          style = {"text-align":"center"})
           ], width = {"size": 10, "offset": 1})
       ]),
   
   html.Hr(style = {"borderColor":"white","borderWidth":"1px", "opacity": "unset"}),
   
    dbc.Row([
        dbc.Col([
            html.Br(),
            dmc.Button('Calculate tokens', id='button-calculate', n_clicks=0,
                       style = {"background":"#99ccff", "color":"black"},
                       leftIcon=DashIconify(icon="tabler:sum")),
          
            html.Br(),
            html.Br(),
            dbc.Label("Number of tokens is:", style = {"color":"white"}),
            dcc.Loading(
            id="loading-1",
            type="circle",
            children=dbc.Input(id="output-token-number")
        )
            ], width = {"size": 2, "offset": 1}),
        dbc.Col([
    dbc.Label("Encoded tokens:", style = {"color":"white"}),
    dcc.Loading(
        id="loading-2",
        type="circle",
     children = dcc.Textarea(
          id='textarea-encoding',
          #title="Encoded text:",
          placeholder = "Encoded tokens will appear here",
          style={ "width":"100%",'height': 150, "resize":"vertical"}
      ))
     ], width = {"size": 7, "offset": 1})
     ]),
    html.Br(),
    html.Br()
       
], fluid = True, style={'backgroundColor':'#333333'})

#------------ Callbacks ------------#
@callback(
    [Output(component_id='output-token-number', component_property='value', 
           allow_duplicate=True),
     Output(component_id='textarea-encoding', component_property='value', 
            allow_duplicate=True)],
    Input("button-calculate", "n_clicks"),
    State("textarea-text", "value"),
    State("radioitems-model-name", "value"),
    prevent_initial_call = True  # important for the reset callback
    )
def calculate_tokens_and_encoding(n_clicks, text_input, model_input):
    if n_clicks > 0:
        encoding = tiktoken.encoding_for_model(model_input)
        encoding_text = encoding.encode(text_input)
        num_tokens = len(encoding_text)
        txt = ", ".join(str(i) for i in encoding_text)
        return num_tokens, txt

#-------------- Run app --------------#
# Need to close browser tab and then interrupt kernel 

port = 8050 # or simply open on the default `8050` port

def open_browser():
	webbrowser.open(url = "http://localhost:{}".format(port), 
                 new = 1)

# Run the app
if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=False, port=port, use_reloader=False)
