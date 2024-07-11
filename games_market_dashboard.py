import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


# Load and clean data
df = pd.read_csv('G:/My Drive/Test_tasks/Valiotti_test_sql_Py_dash/test_games_data.csv') 

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Game Industry Dashboard"),
    html.P("This dashboard provides insights into the game industry. Use the filters to explore the data."),
    
    html.Div([
        html.Div([
            html.Label("Platform Filter"),
            dcc.Dropdown(
                id='platform-filter',
                options=[{'label': platform, 'value': platform} for platform in df['platform'].unique()],
                multi=True
            ),
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Genre Filter"),
            dcc.Dropdown(
                id='genre-filter',
                options=[{'label': genre, 'value': genre} for genre in df['genre'].unique()],
                multi=True
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin-left': '2%'}),

        html.Div([
            html.Label("Year of Release"),
            dcc.RangeSlider(
                id='year-slider',
                min=2000,
                max=2022,
                marks={year: str(year) for year in range(2000, 2023)},
                step=1,
                value=[2000, 2022]
            ),
        ], style={'width': '35%', 'display': 'inline-block', 'margin-left': '2%'}),
    ], style={'margin-bottom': '20px'}),
    
    html.Div([
        html.Div(id='total-games', style={'width': '33%', 'display': 'inline-block', 'text-align': 'center'}),
        html.Div(id='average-user-score', style={'width': '33%', 'display': 'inline-block', 'text-align': 'center'}),
        html.Div(id='average-critic-score', style={'width': '33%', 'display': 'inline-block', 'text-align': 'center'})
    ], style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px'}),
    
    dcc.Graph(id='stacked-area-plot'),
    dcc.Graph(id='scatter-plot'),
    dcc.Graph(id='bar-line-chart')
])

@app.callback(
    [
        Output('total-games', 'children'),
        Output('average-user-score', 'children'),
        Output('average-critic-score', 'children'),
        Output('stacked-area-plot', 'figure'),
        Output('scatter-plot', 'figure'),
        Output('bar-line-chart', 'figure')
    ],
    [
        Input('platform-filter', 'value'),
        Input('genre-filter', 'value'),
        Input('year-slider', 'value')
    ]
)
def update_dashboard(selected_platforms, selected_genres, selected_years):
    filtered_df = df[
        (df['platform'].isin(selected_platforms) if selected_platforms else True) &
        (df['genre'].isin(selected_genres) if selected_genres else True) &
        (df['year_of_release'] >= selected_years[0]) &
        (df['year_of_release'] <= selected_years[1])
    ]
    
    total_games = len(filtered_df)
    avg_user_score = filtered_df['user_score'].mean()
    avg_critic_score = filtered_df['critic_score'].mean()

    total_games_text = f"Total number of games: {total_games}"
    avg_user_score_text = f"Average user score: {avg_user_score:.2f}"
    avg_critic_score_text = f"Average critic score: {avg_critic_score:.2f}"

    # Stacked Area Plot
    area_plot_df = filtered_df.groupby(['year_of_release', 'platform']).size().reset_index(name='Count')
    area_plot = px.area(area_plot_df, x='year_of_release', y='Count', color='platform', title='Game Releases by Year and Platform')
    area_plot.update_layout(title={'text': 'Game Releases by Year and Platform', 'x': 0.5})

    # Scatter Plot
    scatter_plot = px.scatter(filtered_df, x='user_score', y='critic_score', color='genre', title='User Scores vs. Critic Scores by Genre')
    scatter_plot.update_layout(title={'text': 'User Scores vs. Critic Scores by Genre', 'x': 0.5})

    # Bar/Line Chart for Age Rating
    age_rating_df = filtered_df.groupby('genre')['rating_numeric'].mean().reset_index()
    bar_line_chart = px.bar(age_rating_df, x='genre', y='rating_numeric', title='Average Age Rating by Genre')
    bar_line_chart.update_layout(title={'text': 'Average Age Rating by Genre', 'x': 0.5})

    return total_games_text, avg_user_score_text, avg_critic_score_text, area_plot, scatter_plot, bar_line_chart

if __name__ == '__main__':
    app.run_server(debug=True)
