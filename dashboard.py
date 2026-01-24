import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pycountry


data_jobs = pd.read_csv("data_jobs.csv")


#Limpiar salario en USD
data_jobs['salary_in_usd'] = pd.to_numeric(data_jobs['salary_in_usd'], errors='coerce')
data_jobs = data_jobs.dropna(subset=['salary_in_usd'])
data_jobs = data_jobs[data_jobs['salary_in_usd'] > 0]

#Ajustar modalidad de trabajo
def remote_label(x):
    if x == 0:
        return "Presencial"
    elif x == 50:
        return "Híbrido"
    elif x == 100:
        return "Remoto"
    else:
        return "Desconocido"
data_jobs['Modalidad'] = data_jobs['remote_ratio'].apply(remote_label)

# Limpiar espacios y pasar a mayúsculas
data_jobs['experience_level'] = data_jobs['experience_level'].str.strip().str.upper()

#Limpiar experience level
exp_map_es = {
    'EN': 'Nivel inicial',
    'MI': 'Intermedio',
    'SE': 'Senior',
    'EX': 'Ejecutivo'
}
data_jobs['Nivel de experiencia'] = data_jobs['experience_level'].map(exp_map_es)

#Limpiar company size
data_jobs['Tamaño de empresa'] = data_jobs['company_size'].str.upper()
data_jobs = data_jobs.dropna(subset=['Tamaño de empresa'])


# Función para convertir código a nombre de país
def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return "Desconocido"

# Crear columnas nuevas con nombres completos
data_jobs["employee_country"] = data_jobs["employee_residence"].apply(get_country_name)
data_jobs["company_country"] = data_jobs["company_location"].apply(get_country_name)


#Crear dashboard
external_stylesheets = [dbc.themes.COSMO]  # Puedes cambiar el tema, ej: LUX, DARKLY, etc.
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Análisis de empleos en Data Science"
server = app.server

# Opciones para dropdowns
work_mode_options = [
    {'label': 'Todos', 'value': 'All'},
    {'label': 'Remoto', 'value': 'Remoto'},
    {'label': 'Presencial', 'value': 'Presencial'},
    {'label': 'Híbrido', 'value': 'Híbrido'}
]

country_options = [{'label': c, 'value': c} for c in sorted(data_jobs['employee_residence'].unique())]
country_options.insert(0, {'label': 'Todos', 'value': 'All'})

app.layout = dbc.Container([
    html.H1("Dashboard de empleos en Data Science", style={'textAlign':'center', 'marginBottom':'20px'}),

    # Filtros
    dbc.Row([
        dbc.Col([
            html.Label("Filtrar por modalidad:"),
            dcc.Dropdown(
                id='filter_work_mode',
                options=work_mode_options,
                value='All',
                clearable=False
            )
        ], width=4),
        dbc.Col([
            html.Label("Filtrar por país:"),
            dcc.Dropdown(
                id='filter_country',
                options=country_options,
                value='All',
                clearable=False
            )
        ], width=4)
    ], className="mb-4"),

    # Gráficos
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph_salary_country'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph_salary_experience'), width=12)
   ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph_salary_company_size'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph_employee_origin'), width=12)
    ])
], fluid=True)

# ----------------------------
# 3️⃣ Callback para actualizar gráficos
# ----------------------------
@app.callback(
    Output('graph_salary_country', 'figure'),
    Output('graph_salary_experience', 'figure'),
    Output('graph_salary_company_size', 'figure'),
    Output('graph_employee_origin', 'figure'),
    Input('filter_work_mode', 'value'),
    Input('filter_country', 'value')
)
def update_graphs(work_mode, country):
    df_plot = data_jobs.copy()

    # Filtrar por modalidad
    if work_mode != 'All':
        df_plot = df_plot[df_plot['Modalidad'] == work_mode]

    # Filtrar por país
    if country != 'All':
        df_plot = df_plot[df_plot['employee_residence'] == country]

    # Eliminar posibles NaN
    df_plot = df_plot.dropna(subset=['Nivel de experiencia', 'salary_in_usd', 'Tamaño de empresa', 'employee_residence', 'Modalidad'])

    # Gráfico 1: Salario promedio por país
    fig_country = px.bar(
        df_plot.groupby('employee_residence')['salary_in_usd'].mean().reset_index(),
        x='employee_residence',
        y='salary_in_usd',
        labels={'employee_residence':'País', 'salary_in_usd':'Salario promedio USD'},
        title='Salario promedio por país'
    )
 # Gráfico 2: Salario promedio por nivel de experiencia
    fig_experience = px.bar(
        df_plot.groupby('Nivel de experiencia')['salary_in_usd'].mean().reset_index(),
        x='Nivel de experiencia',
        y='salary_in_usd',
        labels={'Nivel de experiencia':'Nivel de experiencia', 'salary_in_usd':'Salario promedio USD'},
        title='Salario promedio por nivel de experiencia'
    )

    # Gráfico 3: Salario promedio por tamaño de empresa
    fig_company = px.bar(
        df_plot.groupby('Tamaño de empresa')['salary_in_usd'].mean().reset_index(),
        x='Tamaño de empresa',
        y='salary_in_usd',
        labels={'Tamaño de empresa':'Tamaño de empresa', 'salary_in_usd':'Salario promedio USD'},
        title='Salario promedio por tamaño de empresa'
    )

    # Gráfico 4: Procedencia de empleados por modalidad
    df_group = df_plot.groupby(['employee_residence', 'Modalidad']).size().reset_index(name='Cantidad')
    fig_origin = px.bar(
        df_group,
        x='employee_residence',
        y='Cantidad',
        color='Modalidad',
        title='Procedencia de los empleados según modalidad de trabajo',
        labels={'employee_residence':'País', 'Cantidad':'Número de empleados', 'Modalidad':'Modalidad'}
    )

    return fig_country, fig_experience, fig_company, fig_origin

# ----------------------------
# 4️⃣ Ejecutar la app
# ----------------------------
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)


