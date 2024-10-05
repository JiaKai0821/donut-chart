import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objects as go
import pandas as pd



# 讀取 .xlsx 文件
file_path = 'Country_data.xlsx'
df = pd.read_excel(file_path)

# 查看讀取的數據
print(df.head())
print(df.iloc[0])
# 定義各國的初始能源比例
initial_country_data = {}
options = []
power = {}
pop = {}
for _, row in df.iterrows():
    country = row['country']
    values = row[2:7].tolist()
    initial_country_data[country] = values
    options.append({'label':country, 'value':country})
    power[country] = str(round(row[7],2))
    pop[country] = str(round(row[1],2))
print(pop)

#缺少一個country population,找到selected country之後，相對應country的population

#print(initial_country_data)
#print(options)

# 初始化 Dash 應用
app = dash.Dash(__name__)
server = app.server
total = 100
colors = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#33FFF3']  # 自定義顏色組合

# 應用的 layout
app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'column', 'backgroundColor': '#f2f2f2', 'padding': '20px'}, children=[
    # 上方區域：左側選擇國家和調整比例
    html.Div(style={'display': 'flex'}, children=[
        # 左側控制
        html.Div(style={'flex': '1', 'paddingRight': '40px'}, children=[
            html.H2('Country Energy Source Percentage Control', style={'textAlign': 'center', 'color': '#333', 'fontFamily': 'Arial'}),

            # 國家選單
            html.Label('Select Country:', style={'fontSize': '18px', 'marginRight': '15px', 'fontFamily': 'Arial'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=options,
                value='Argentina',  # 預設選擇第一個國家
                clearable=False,
                style={'width': '80%', 'borderRadius': '10px', 'boxShadow': '0px 3px 6px rgba(0, 0, 0, 0.16)', 'fontFamily': 'Arial'}
            ),

            # 生成 5 個滑動條
            html.Div(id='sliders', children=[
                html.Label('Natural Gas:', style={'fontSize': '18px', 'marginTop': '20px', 'fontFamily': 'Arial'}),
                dcc.Slider(id='slider-0', min=0, max=total, step=1, value=40,  # 預設為美國的比例
                           marks={i: f'{i}%' for i in range(0, total+1, 10)}, tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Label('Coal:', style={'fontSize': '18px', 'marginTop': '20px', 'fontFamily': 'Arial'}),
                dcc.Slider(id='slider-1', min=0, max=total, step=1, value=30,
                           marks={i: f'{i}%' for i in range(0, total+1, 10)}, tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Label('Renewable Sources:', style={'fontSize': '18px', 'marginTop': '20px', 'fontFamily': 'Arial'}),
                dcc.Slider(id='slider-2', min=0, max=total, step=1, value=15,
                           marks={i: f'{i}%' for i in range(0, total+1, 10)}, tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Label('Nuclear:', style={'fontSize': '18px', 'marginTop': '20px', 'fontFamily': 'Arial'}),
                dcc.Slider(id='slider-3', min=0, max=total, step=1, value=10,
                           marks={i: f'{i}%' for i in range(0, total+1, 10)}, tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Label('Oil:', style={'fontSize': '18px', 'marginTop': '20px', 'fontFamily': 'Arial'}),
                dcc.Slider(id='slider-4', min=0, max=total, step=1, value=5,
                           marks={i: f'{i}%' for i in range(0, total+1, 10)}, tooltip={"placement": "bottom", "always_visible": True}),
            ])
        ]),

        # 右側的 donut chart
        html.Div(style={'flex': '1', 'paddingLeft': '40px'}, children=[
            dcc.Graph(id='pie-chart')
        ])
    ]),
    
    # 下方區域：顯示比例的表格
    html.Div(style={'marginTop': '40px'}, children=[
        # 國家和人口的小表格
        dash_table.DataTable(
           id='country-info-table',
           columns=[
               {'name': 'Country', 'id': 'country'},
               {'name': 'Population', 'id': 'population'},
               {'name': 'Power', 'id':'power'}
           ],
           data=[],
           style_cell={'textAlign': 'center', 'fontFamily': 'Arial', 'fontSize': '16px'},
           style_header={'fontWeight': 'bold', 'backgroundColor': '#f9f9f9'},
        ),

        
        html.H3('Energy Source Calculation Table', style={'textAlign': 'center', 'color': '#333', 'fontFamily': 'Arial'}),
        dash_table.DataTable(
            id='percentage-table',
            columns=[
                {"name": 'Energy Source', "id": 'energy_source'},
                {"name": 'Percentage (%)', "id": 'percentage'},
                {"name": 'CO2 emission Per kWh', "id": 'emission' },
                {"name": 'Replaced by equivalent Wetland area(Million Hectare)', "id":'area'},
                {"name": 'Wetland Area Per Capita(Hectares)', 'id': 'wetcap'},
                {"name": 'Wetland Area Per Capita(Soccer Field)', 'id':'soceerfield'}
                
            ],
            style_cell={'textAlign': 'center', 'fontFamily': 'Arial', 'fontSize': 16},
            style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
            style_data={'backgroundColor': 'white', 'border': '1px solid black'},
        ),
        html.P(" *   :  Weighted Average", 
          style={'textAlign': 'left', 'fontSize': '18px', 'fontFamily': 'Arial', 'marginTop': '20px'})
    ])
])

# 更新 pie chart、sliders 和 table 的回調函數
@app.callback(
    [Output('slider-0', 'value'),
     Output('slider-1', 'value'),
     Output('slider-2', 'value'),
     Output('slider-3', 'value'),
     Output('slider-4', 'value'),
     Output('pie-chart', 'figure'),
     Output('percentage-table', 'data'),
     Output('country-info-table', 'data')],
    [Input('country-dropdown', 'value'),
     Input('slider-0', 'value'),
     Input('slider-1', 'value'),
     Input('slider-2', 'value'),
     Input('slider-3', 'value'),
     Input('slider-4', 'value')],
    [State('slider-0', 'value'),
     State('slider-1', 'value'),
     State('slider-2', 'value'),
     State('slider-3', 'value'),
     State('slider-4', 'value')]
)
def update_outputs(selected_country, s0, s1, s2, s3, s4, old_s0, old_s1, old_s2, old_s3, old_s4):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger == 'country-dropdown':
        # 當選擇國家時，初始化滑動條為該國家的比例
        values = initial_country_data[selected_country].copy()
    else:
        # 調整滑動條時，保持總和為 100%
        values = [s0, s1, s2, s3, s4]
        total_value = sum(values)
        
        if total_value != 100:
            changed_idx = int(trigger.split('-')[1])  # 取得被改變的 slider index
            delta = 100 - total_value  # 計算需要調整的總量
            
            # 分配 delta 到其他的 slider 上，確保總和為 100%
            adjustment_indices = [i for i in range(5) if i != changed_idx]
            total_other_values = sum(values[i] for i in adjustment_indices)
            for i in adjustment_indices:
                if total_other_values > 0:
                    values[i] = max(0, values[i] + (values[i] / total_other_values) * delta)
                else:
                    values[i] += delta / 4  # 若其他值為0，平均分配delta

    # 更新 pie chart
    labels = ['Natural Gas', 'Coal', 'Renewable Sources', 'Nuclear', 'Oil']
    fig = go.Figure(data=[go.Pie(labels=labels, values=values,
                                 marker=dict(colors=colors, line=dict(color='#FFF', width=2)), hole=0.4)])  # donut chart
    
    # 更新 pie chart 樣式
    fig.update_layout(
        title_text='Energy Source Pie Chart',
        annotations=[dict(text=f'{int(sum(values))}%', x=0.5, y=0.5, font_size=20, showarrow=False)],
        font=dict(size=14, color='#333', family='Arial'),
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
        paper_bgcolor='#f9f9f9',
        plot_bgcolor='#f9f9f9',
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"),
        margin=dict(l=50, r=50, t=50, b=100)
    )
    #CO2 emission per source
    source_emi = [450,1000, 20, 12, 450]
    wetland_area = []
    for percent,emi in zip(values, source_emi):
        result = percent/100 * emi * float(power[selected_country]) 
        result = round(result,2) /1000
        wetland_area.append(result)
    #total_list = []
    total_i = 0
    total_j = 0
    total_k = 0
    total_l = 0
    total_m = 0
    #除以人均負擔wetland面積
    wetlandPerCap = []
    soccerfieldArea = []
    
    #人均wetland_area大小
    for i in wetland_area:
        result = float(i) /float(pop[selected_country]) * 1e6
        result_soccer = result/0.714
        wetlandPerCap.append(result)
        soccerfieldArea.append(result_soccer)
    for i,j,k,l,m in zip(values, source_emi,wetland_area, wetlandPerCap,soccerfieldArea):
        total_i +=  i
        total_j +=  i/100*j
        total_k +=  k
        total_l +=  l
        total_m +=  m
        
    country_info = [{'country':selected_country, 'population':f"{str(round((float(pop[selected_country])/1e6),2)) +' Million'}", 'power':f"{power[selected_country] +'TWh'}"}]
    #country_info = [{'country':selected_country, 'population':f"{pop[selected_country]}"}]
    # 更新表格數據
    table_data = [{'energy_source': label, 'percentage': f'{round(value,2)}%', 'emission':f'{emi}', 'area':f"{round(area,2)}", 'wetcap':f"{round(wetlandCap,2)}", 'soceerfield':f'{round(soccerArea,2)}'} for label, value,emi,area,wetlandCap,soccerArea in zip(labels, values,source_emi,wetland_area,wetlandPerCap,soccerfieldArea)]
    #顯示計算的綜合數值
    
    table_data.append({'energy_source':"Total", 'percentage':f"{round(total_i,2)}%",'emission':f"{round(total_j,2)}*", 'area':f"{round(total_k,2)}", 'wetcap':f"{round(total_l,2)}", 'soceerfield':f"{round(total_m,2)}" })
    
    return values[0], values[1], values[2], values[3], values[4], fig, table_data,country_info

# 運行應用
if __name__ == '__main__':
    app.run_server(debug=True)
