import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
import plotly.express as px
import pandas as pd

import plotly.graph_objects as go

from os.path import join
from functools import reduce


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

def get_grp_data(df, method='TSNE', company_name='EBAY INC', grp='GICS_SECTOR'):
    company_row = df[df['Name'] == company_name]
    grp_value = company_row[grp].values[0]
    return df[df[grp] == grp_value]

def get_neighbor_data(df, neighbors=['EBAY INC']):
    return df[df['Name'] in neighbors]


def generate_vis(df, dist_matrix=None, year=2013, dim=3, method='TSNE', vis_type='OVERALL', grp='GICS_SECTOR', company='EBAY INC', num_neighbors=200, size=5, opacity=0.8, x_title='X', y_title='Y', z_title='Z', just_name=False, fig_width=800, fig_height=800, diff_grp=None, companies=[]):
    temp_grp = grp if diff_grp == None else diff_grp
    if temp_grp in {'GICS_SECTOR', 'ML_sector'}:
        gics_grp = 'Sector'
        gics_grp_str = 'GICS_SECTOR'
    if temp_grp in {'GICS_INDUSTRY', 'ML_industry'}:
        gics_grp = 'Industry'
        gics_grp_str = 'GICS_INDUSTRY'
    if temp_grp in {'GICS_SUB_INDUSTRY', 'ML_subindustry'}:
        gics_grp = 'Sub-Industry'
        gics_grp_str = 'GICS_SUB_INDUSTRY'
    
    if dim == 2:
        if vis_type == 'OVERALL':
            fig = go.Figure(data=go.Scatter(x=df['X' + '2' + method], 
                                            y=df['Y' + '2' + method],
                                            mode='markers',
                                            marker = {
                                                'size': size,
                                                'opacity': opacity,
                                                'color': df[grp + '_Color']
                                            },
                                            hovertext = df['Name'] + ' (GICS ' + gics_grp + ': ' + df['Proper_' + gics_grp_str].astype(str) + ')',
                                            text=df['Name'],
                                            hovertemplate = '%{hovertext}' + '<extra></extra>',
                                            hoverinfo='text'
                                            )
                            )
            
            """
            ####
            # Overall 2020 Industry Annotations for GM, Ford, Visa, Dell, and Microsoft
            ####
            
            # GM
            fig.add_annotation(
                x=5.1619873,
                y=-14.178176,
                xref="x",
                yref="y",
                text="General Motors",
                showarrow=True,
                font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#ffffff"
                    ),
                align="center",
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#636363",
                ax=20,
                ay=-30,
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=1
            )

            # Ford
            fig.add_annotation(
                x=5.2789135,
                y=-14.094484,
                xref="x",
                yref="y",
                text="Ford Motor",
                showarrow=True,
                font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#ffffff"
                    ),
                align="center",
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#636363",
                ax=20,
                ay=30,
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=1
            )

            # Visa
            fig.add_annotation(
                x=-11.341368,
                y=3.0591452,
                xref="x",
                yref="y",
                text="Visa",
                showarrow=True,
                font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#ffffff"
                    ),
                align="center",
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#636363",
                ax=20,
                ay=20,
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=1
            )

            # Dell
            fig.add_annotation(
                x=-14.460399,
                y=0.6034735,
                xref="x",
                yref="y",
                text="Dell Technologies",
                showarrow=True,
                font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#ffffff"
                    ),
                align="center",
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#636363",
                ax=20,
                ay=30,
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=1
            )

            # Microsoft
            fig.add_annotation(
                x=-12.391454,
                y=3.1743627,
                xref="x",
                yref="y",
                text="Microsoft",
                showarrow=True,
                font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#ffffff"
                    ),
                align="center",
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#636363",
                ax=20,
                ay=-30,
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=1
            )
            """

        elif vis_type == 'KERNEL':
            grp_data = get_grp_data(df=df, method=method, company_name=company, grp=grp)
            company_row = df[df['Name'] == company]
            norm_x, norm_y = company_row[['X'+str(dim)+method, 'Y'+str(dim)+method]].values[0]
            company_index = company_row.index.values[0]
            grp_data.loc[company_index, grp + '_Color'] = '#000000'
            fig = go.Figure(data=go.Scatter(x=grp_data['X' + '2' + method] - norm_x, 
                                            y=grp_data['Y' + '2' + method] - norm_y,
                                            mode='markers',
                                            marker = {
                                                'size': size,
                                                'opacity': opacity,
                                                'color': grp_data[grp + '_Color']
                                            },
                                            hovertext = grp_data['Name'] + ' (GICS ' + gics_grp + ': ' + grp_data['Proper_' + gics_grp_str].astype(str) + ')',
                                            hovertemplate = '%{hovertext}' + '<extra></extra>'
                                            )
                          )
        
        elif vis_type == 'MULTI-KERNEL':
            assert len(companies) >= 1
            frames = []
            #grp_data = pd.DataFrame()
            for c in companies:
                grp_data = get_grp_data(df=df, method=method, company_name=c, grp=grp)
                frames.append(grp_data)
            grp_data = pd.concat(frames)
            """
            if year == 2019 and companies[0] == 'S&P GLOBAL INC':
                for i, row in grp_data.iterrows():
                    grp_data.loc[i, grp + '_Color'] = '#013349'
            """
            for c in companies:
                company_row = df[df['Name'] == c]
                company_index = company_row.index.values[0]
                grp_data.loc[company_index, grp + '_Color'] = '#000000'
            fig = go.Figure(data=go.Scatter(x=grp_data['X' + '2' + method], 
                                              y=grp_data['Y' + '2' + method],
                                              mode='markers',
                                              marker = {
                                                  'size': size,
                                                  'opacity': opacity,
                                                  'color': grp_data[grp + '_Color']
                                              },
                                              hovertext = grp_data['Name'] + ' (GICS ' + gics_grp + ': ' + grp_data['Proper_' + gics_grp_str].astype(str) + ')',
                                              hovertemplate = '%{hovertext}' + '<extra></extra>'
                                             )
                          )
            """
            if year == 2019 and companies[0] == 'S&P GLOBAL INC':
                font_size = 16
                fig.add_annotation(
                            x=-9.194597,
                            y=0.990914,
                            xref="x",
                            yref="y",
                            text='S&P Global',
                            showarrow=True,
                            font=dict(
                                family="Courier New, monospace",
                                size=font_size,
                                color="#ffffff"
                                ),
                            align="center",
                            arrowhead=2,
                            arrowsize=1,
                            arrowwidth=2,
                            arrowcolor="#636363",
                            ax=-20,
                            ay=30,
                            bordercolor="#c7c7c7",
                            borderwidth=2,
                            borderpad=4,
                            bgcolor="#ff7f0e",
                            opacity=1
                    )
                
                fig.add_annotation(
                            x=16.371483,
                            y=0.11571513,
                            xref="x",
                            yref="y",
                            text='NASDAQ',
                            showarrow=True,
                            font=dict(
                                family="Courier New, monospace",
                                size=font_size,
                                color="#ffffff"
                                ),
                            align="center",
                            arrowhead=2,
                            arrowsize=1,
                            arrowwidth=2,
                            arrowcolor="#636363",
                            ax=-20,
                            ay=-30,
                            bordercolor="#c7c7c7",
                            borderwidth=2,
                            borderpad=4,
                            bgcolor="#ff7f0e",
                            opacity=1
                    )

                fig.add_annotation(
                            x=-9.041113,
                            y=0.78305656,
                            xref="x",
                            yref="y",
                            text="Moody's",
                            showarrow=True,
                            font=dict(
                                family="Courier New, monospace",
                                size=font_size,
                                color="#ffffff"
                                ),
                            align="center",
                            arrowhead=2,
                            arrowsize=1,
                            arrowwidth=2,
                            arrowcolor="#636363",
                            ax=-20,
                            ay=30,
                            bordercolor="#c7c7c7",
                            borderwidth=2,
                            borderpad=4,
                            bgcolor="#ff7f0e",
                            opacity=1
                    )

                fig.add_annotation(
                            x=3.0832522,
                            y=2.2406511,
                            xref="x",
                            yref="y",
                            text="Cohen & Steers",
                            showarrow=True,
                            font=dict(
                                family="Courier New, monospace",
                                size=font_size,
                                color="#ffffff"
                                ),
                            align="center",
                            arrowhead=2,
                            arrowsize=1,
                            arrowwidth=2,
                            arrowcolor="#636363",
                            ax=-20,
                            ay=40,
                            bordercolor="#c7c7c7",
                            borderwidth=2,
                            borderpad=4,
                            bgcolor="#ff7f0e",
                            opacity=1
                    )
            """
                
            
        elif vis_type == 'NEAREST NEIGHBORS':
            
            neighbors_df = yr_dm_dict[str(year)]
            neighbors_list = neighbors_df[neighbors_df['Company'] == companies]["NearestNeighborsORDERED"].item()
            neighbors_list = neighbors_list[1:len(neighbors_list) - 1]
            neighbors_list = neighbors_list.split(", ")
            
            temp_list = []
            for elt in neighbors_list:
                temp_list.append(elt[1:len(elt) - 1])
            
            neighbors_list = temp_list[:num_neighbors + 1]

            df = df[df['Name'].isin(neighbors_list)]

            company_row = df[df['Name'] == companies]
            company_index = company_row.index.values[0]
            df.loc[company_index, grp + '_Color'] = '#000000'

            fig = go.Figure(data=go.Scatter(x=df['X' + '2' + method], 
                                              y=df['Y' + '2' + method],
                                              mode='markers',
                                              marker = {
                                                  'size': size,
                                                  'opacity': opacity,
                                                  'color': df[grp + '_Color']
                                              },
                                              hovertext = df['Name'] + ' (GICS ' + gics_grp + ': ' + df['Proper_' + gics_grp_str].astype(str) + ')',
                                              hovertemplate = '%{hovertext}' + '<extra></extra>'
                                             )
                          )
            
            ####
            # Overall 2020 NN Annotations for Fedex: HB Fuller, CSX Corp, Norfolk Southern Corp, United Parcel Service, Expeditors International of Washington, XPO Logistics, Forward Air, Landstar System, Ryder System, Werner Enterprises 
            ####
            """
            if year == 2019:
                comps_to_label = ['FEDEX CORP', 'HB FULLER CO', 'CSX CORP', 'NORFOLK SOUTHERN CORP', 'UNITED PARCEL SERVICE INC', 'EXPEDITORS INTERN OF WASHINGTON INC']
                font_size = 16
                block_w = 2
                block_pad = 4 
                fig.add_annotation(
                        x=5.8953223,
                        y=-7.83815,
                        xref="x",
                        yref="y",
                        text='Fedex',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=-20,
                        ay=30,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )

                fig.add_annotation(
                        x=-3.451251,
                        y=-13.001972,
                        xref="x",
                        yref="y",
                        text='HB Fuller',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=20,
                        ay=-30,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )

                fig.add_annotation(
                        x=5.5018287,
                        y=-5.593997,
                        xref="x",
                        yref="y",
                        text='CSX Corp',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=20,
                        ay=-30,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )

                
                fig.add_annotation(
                        x=5.5200057,
                        y=-5.599181,
                        xref="x",
                        yref="y",
                        text='NORFOLK SOUTHERN CORP',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=20,
                        ay=30,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )
                

                fig.add_annotation(
                        x=5.764789,
                        y=-7.709774,
                        xref="x",
                        yref="y",
                        text='United Parcel Service',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=-150,
                        ay=-20,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )

                
                fig.add_annotation(
                        x=-7.4716988,
                        y=-28.032024,
                        xref="x",
                        yref="y",
                        text='EXPEDITORS INTERNATIONAL',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=40,
                        ay=-30,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )
                

                
                fig.add_annotation(
                        x=6.338511,
                        y=-7.6690702,
                        xref="x",
                        yref="y",
                        text='XPO LOGISTICS',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=-20,
                        ay=0,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )
                
                
                fig.add_annotation(
                        x=7.539125,
                        y=-7.9430842,
                        xref="x",
                        yref="y",
                        text='Ryder System',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=-20,
                        ay=0,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )
                

                
                fig.add_annotation(
                        x=6.490533,
                        y=-6.936752,
                        xref="x",
                        yref="y",
                        text='FORWARD AIR CORP',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=0,
                        ay=-20,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )
                
                
                fig.add_annotation(
                        x=6.9869075,
                        y=-7.027576,
                        xref="x",
                        yref="y",
                        text='LANDSTAR SYSTEM',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=0,
                        ay=-10,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )
                

                
                fig.add_annotation(
                        x=7.491798,
                        y=-7.049541,
                        xref="x",
                        yref="y",
                        text='WERNER ENTERPRISES',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=font_size,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=-20,
                        ay=0,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )
                

                

                
                for comp in orig_neighbors_list[:11]:
                    company_row = df[df['Name'] == comp]
                    company_index = company_row.index.values[0]
                    df.loc[company_index, grp + '_Color'] = '#000000'
                    fig.add_annotation(
                        x=df.loc[company_index, 'X3TSNE'],
                        y=df.loc[company_index, 'Y3TSNE'],
                        xref="x",
                        yref="y",
                        text=df.loc[company_index, 'Name'],
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=16,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=20,
                        ay=-30,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                    )
            """
            
            
    else:
        if vis_type == 'OVERALL':
            fig = go.Figure(data=go.Scatter3d(x=df['X' + '3' + method], 
                                              y=df['Y' + '3' + method],
                                              z=df['Z' + '3' + method],
                                              mode='markers',
                                              marker = {
                                                  'size': size,
                                                  'opacity': opacity,
                                                  'color': df[grp + '_Color']
                                              },
                                              hovertext = df['Name'] + ' (GICS ' + gics_grp + ': ' + df['Proper_' + gics_grp_str].astype(str) + ')',
                                              #text=df['Name'] + ' (GICS ' + gics_grp + ': ' + df['Proper_' + gics_grp_str].astype(str) + ')',
                                              hovertemplate = '%{hovertext}' + '<extra></extra>'
                                             )
                          )
        
        elif vis_type == 'KERNEL':
            grp_data = get_grp_data(df=df, method=method, company_name=company, grp=grp)
            company_row = df[df['Name'] == company]
            norm_x, norm_y, norm_z = company_row[['X'+str(dim)+method, 'Y'+str(dim)+method, 'Z'+str(dim)+method]].values[0]
            company_index = company_row.index.values[0]
            grp_data.loc[company_index, grp + '_Color'] = '#000000'
            fig = go.Figure(data=go.Scatter3d(x=grp_data['X' + '3' + method] - norm_x, 
                                              y=grp_data['Y' + '3' + method] - norm_y,
                                              z=grp_data['Z' + '3' + method] - norm_z,
                                              mode='markers',
                                              marker = {
                                                  'size': size,
                                                  'opacity': opacity,
                                                  'color': grp_data[grp + '_Color']
                                              },
                                              hovertext = grp_data['Name'] + ' (GICS ' + gics_grp + ': ' + grp_data['Proper_' + gics_grp_str].astype(str) + ')',
                                              hovertemplate = '%{hovertext}' + '<extra></extra>'
                                             )
                          )
            
        elif vis_type == 'MULTI-KERNEL':
            assert len(companies) >= 1
            frames = []
            #grp_data = pd.DataFrame()
            for c in companies:
                grp_data = get_grp_data(df=df, method=method, company_name=c, grp=grp)
                frames.append(grp_data)
            grp_data = pd.concat(frames)
            """
            if year == 2019 and companies[0] == 'S&P GLOBAL INC':
                for i, row in grp_data.iterrows():
                    #grp_data.loc[i, grp + '_Color'] = '#013349'
                    #grp_data.loc[i, grp + '_Color'] = '#5B4534'
                    grp_data.loc[i, grp + '_Color'] = '#5EBCD1'
            """
            for c in companies:
                company_row = df[df['Name'] == c]
                company_index = company_row.index.values[0]
                grp_data.loc[company_index, grp + '_Color'] = '#000000'
            fig = go.Figure(data=go.Scatter3d(x=grp_data['X' + '3' + method], 
                                              y=grp_data['Y' + '3' + method],
                                              z=grp_data['Z' + '3' + method],
                                              mode='markers',
                                              marker = {
                                                  'size': size,
                                                  'opacity': opacity,
                                                  'color': grp_data[grp + '_Color']
                                              },
                                              hovertext = grp_data['Name'] + ' (GICS ' + gics_grp + ': ' + grp_data['Proper_' + gics_grp_str].astype(str) + ')',
                                              hovertemplate = '%{hovertext}' + '<extra></extra>'
                                             )
                          )
        
        elif vis_type == "NEAREST NEIGHBORS":

            neighbors_df = yr_dm_dict[str(year)]
            neighbors_list = neighbors_df[neighbors_df['Company'] == companies]["NearestNeighborsORDERED"].item()
            neighbors_list = neighbors_list[1:len(neighbors_list) - 1]
            neighbors_list = neighbors_list.split(", ")
            
            temp_list = []
            for elt in neighbors_list:
                temp_list.append(elt[1:len(elt) - 1])
            
            orig_neighbors_list = temp_list
            neighbors_list = temp_list[:num_neighbors + 1]

            df = df[df['Name'].isin(neighbors_list)]

            company_row = df[df['Name'] == companies]
            company_index = company_row.index.values[0]
            df.loc[company_index, grp + '_Color'] = '#000000'

            fig = go.Figure(data=go.Scatter3d(x=df['X' + '3' + method], 
                                              y=df['Y' + '3' + method],
                                              z=df['Z' + '3' + method],
                                              mode='markers',
                                              marker = {
                                                  'size': size,
                                                  'opacity': opacity,
                                                  'color': df[grp + '_Color']
                                              },
                                              hovertext = df['Name'] + ' (GICS ' + gics_grp + ': ' + df['Proper_' + gics_grp_str].astype(str) + ')',
                                              hovertemplate = '%{hovertext}' + '<extra></extra>'
                                             )
                          )
            
            ####
            # Overall 2020 NN Annotations for Fedex: HB Fuller, CSX Corp, Norfolk Southern Corp, United Parcel Service, Expeditors International of Washington, XPO Logistics, Forward Air, Landstar System, Ryder System, Werner Enterprises 
            ####
            """
            if year == 2019:
                comps_to_label = ['FEDEX CORP', 'HB FULLER CO', 'CSX CORP', 'NORFOLK SOUTHERN CORP', 'UNITED PARCEL SERVICE INC', 'EXPEDITORS INTERN OF WASHINGTON INC']
                fig.add_annotation(
                        x=-28.034233,
                        y=-11.685763,
                        xref="x",
                        yref="y",
                        text='FEDEX CORP',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=16,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=20,
                        ay=-30,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )

                fig.add_annotation(
                        x=-16.660648,
                        y=-16.417713,
                        xref="x",
                        yref="y",
                        text='HB FULLER CO',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=16,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=20,
                        ay=-30,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )

                fig.add_annotation(
                        x=-3.4367993,
                        y=4.7843504,
                        xref="x",
                        yref="y",
                        text='CSX CORP',
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=16,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=20,
                        ay=-30,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                )
                

                
                for comp in orig_neighbors_list[:11]:
                    company_row = df[df['Name'] == comp]
                    company_index = company_row.index.values[0]
                    df.loc[company_index, grp + '_Color'] = '#000000'
                    fig.add_annotation(
                        x=df.loc[company_index, 'X3TSNE'],
                        y=df.loc[company_index, 'Y3TSNE'],
                        xref="x",
                        yref="y",
                        text=df.loc[company_index, 'Name'],
                        showarrow=True,
                        font=dict(
                            family="Courier New, monospace",
                            size=16,
                            color="#ffffff"
                            ),
                        align="center",
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=20,
                        ay=-30,
                        bordercolor="#c7c7c7",
                        borderwidth=2,
                        borderpad=4,
                        bgcolor="#ff7f0e",
                        opacity=1
                    )
            """  

            
    
    fig.update_layout(scene=dict(
                            xaxis_title=x_title,
                            yaxis_title=y_title,
                            zaxis_title=z_title
                        ),
                        width=fig_width,
                        height=fig_height,
                        margin=dict(t=30, r=0, l=20, b=10)
    )

    name = str(year) + ' ' + method + ' ' + vis_type
    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0,y=0,z=0),
        #eye = dict(x=0.1, y=0.1, z=1.5)
        eye=dict(x=1.25, y=1.25, z=1.25)
    )

    #fig.update_layout(scene_camera=camera, title=name)
    fig.update_layout(scene_camera=camera)
    return fig



df_2013 = pd.read_csv('cons_data1_' + '2013' +'.csv')
df_2014 = pd.read_csv('cons_data1_' + '2014' +'.csv')
df_2015 = pd.read_csv('cons_data1_' + '2015' +'.csv')
df_2016 = pd.read_csv('cons_data1_' + '2016' +'.csv')
df_2017 = pd.read_csv('cons_data1_' + '2017' +'.csv')
df_2018 = pd.read_csv('cons_data1_' + '2018' +'.csv')
df_2019 = pd.read_csv('cons_data1_' + '2019' +'.csv')

yr_df_dict = {
    "2013": df_2013,
    "2014": df_2014,
    "2015": df_2015,
    "2016": df_2016,
    "2017": df_2017,
    "2018": df_2018,
    "2019": df_2019
}

d_matrix_2013 = pd.read_csv('d_matrix_' + '2013' +'.csv')
d_matrix_2014 = pd.read_csv('d_matrix_' + '2014' +'.csv')
d_matrix_2015 = pd.read_csv('d_matrix_' + '2015' +'.csv')
d_matrix_2016 = pd.read_csv('d_matrix_' + '2016' +'.csv')
d_matrix_2017 = pd.read_csv('d_matrix_' + '2017' +'.csv')
d_matrix_2018 = pd.read_csv('d_matrix_' + '2018' +'.csv')
d_matrix_2019 = pd.read_csv('d_matrix_' + '2019' +'.csv')

yr_dm_dict = {
    "2013": d_matrix_2013,
    "2014": d_matrix_2014,
    "2015": d_matrix_2015,
    "2016": d_matrix_2016,
    "2017": d_matrix_2017,
    "2018": d_matrix_2018,
    "2019": d_matrix_2019
}

num_neighbors_options = []

min_num_neighbors = 1
max_num_neighbors = 20

for i in range(1, max_num_neighbors + 1):
    num_neighbors_options.append({'label': str(i), 'value': str(i)})

app.layout = html.Div([

    html.Div([
        html.Img(src=app.get_asset_url('lfe_logo.png'))
    ]),

    html.Div([
        dcc.Dropdown(
            id='visualization_model',
            options=[
                {'label': 'Overall Cluster [Visualize all companies in a grouping]', 'value': 'OVERALL'},
                {'label': 'Kernel(s) [Pick at least one company, and see all companies that are classified in same grouping]', 'value': 'MULTI-KERNEL'},
                {'label': 'Nearest Neighbors [Pick one company, and see up to 20 companies that are very similar but not necessarily classified in same grouping]', 'value': 'NEAREST NEIGHBORS'}
            ],
            placeholder='Visualization Model'
        ),

        dcc.Dropdown(
            id='cluster_group',
            options=[
                {'label': 'ML Sector', 'value': 'ML_sector'},
                {'label': 'ML Industry', 'value': 'ML_industry'},
                {'label': 'ML Subindustry', 'value': 'ML_subindustry'},
                {'label': 'GICS Sector', 'value': 'GICS_SECTOR'},
                {'label': 'GICS Industry', 'value': 'GICS_INDUSTRY'},
                {'label': 'GICS Subindustry', 'value': 'GICS_SUB_INDUSTRY'}
            ],
            placeholder='Cluster Group'
        ),

        dcc.Dropdown(
            id='year',
            options=[
                {'label': '2014', 'value': '2013'},
                {'label': '2015', 'value': '2014'},
                {'label': '2016', 'value': '2015'},
                {'label': '2017', 'value': '2016'},
                {'label': '2018', 'value': '2017'},
                {'label': '2019', 'value': '2018'},
                {'label': '2020', 'value': '2019'}
            ],
            placeholder='Year'
        ), 

        dcc.Dropdown(
            id='companies',
            options=[],
            placeholder='Company/Companies',
            multi=True,
            disabled=True
        ),

        dcc.Dropdown(
            id='num_neighbors',
            options=num_neighbors_options,
            placeholder='Number of Neighbors (Pick [1-20])',
            multi=False,
            disabled=True,
            value="1"
        ),

        dcc.RadioItems(
            id='dimension_toggle',
            options=[
                {'label': '2D', 'value': '2'},
                {'label': '3D', 'value': '3'}
            ],
            value='2',
            labelStyle={'display': 'inline-block'},
        )
    ]),

    html.Div([
        dcc.Graph(
            id='graph',
            figure={}
        )
    ]),

    html.Div([
        html.P('© 2021 by MIT LFE. All Rights Reserved.'),
        html.P('The Global Industry Classification Standard (“GICS”) was developed by and is the exclusive property and a service mark of MSCI Inc. (“MSCI”) and S&P Global Market Intelligence (“S&P”) and is licensed for use by [Licensee]. Neither MSCI, S&P, nor any other party involved in making or compiling the GICS or any GICS classifications makes any express or implied warranties or representations with respect to such standard or classification (or the results to be obtained by the use thereof), and all such parties hereby expressly disclaim all warranties of originality, accuracy, completeness, merchantability and fitness for a particular purpose with respect to any of such standard or classification. Without limiting any of the foregoing, in no event shall MSCI, S&P, any of their affiliates or any third party involved in making or compiling the GICS or any GICS classifications have any liability for any direct, indirect, special, punitive, consequential or any other damages (including lost profits) even if notified of the possibility of such damages.'),
    ])
])



@app.callback(
    dash.dependencies.Output('companies', 'disabled'),
    dash.dependencies.Output('cluster_group', 'disabled'),
    dash.dependencies.Output('year', 'disabled'),
    dash.dependencies.Input('visualization_model', 'value'))
def update_disabled(visualization_model):
    return (visualization_model not in {'MULTI-KERNEL', 'NEAREST NEIGHBORS'}), (visualization_model not in {'MULTI-KERNEL', 'OVERALL', 'NEAREST NEIGHBORS'}), (visualization_model not in {'MULTI-KERNEL', 'OVERALL', 'NEAREST NEIGHBORS'})

@app.callback(
    dash.dependencies.Output('companies', 'placeholder'),
    dash.dependencies.Output('companies', 'multi'),
    dash.dependencies.Input('visualization_model', 'value'))
def update_companies_dropdown(vis_model):
    if vis_model != 'NEAREST NEIGHBORS':
        return "Company/Companies", True
    else:
        return "Company", False

@app.callback(
    dash.dependencies.Output('companies', 'options'),
    [dash.dependencies.Input('companies', 'disabled'),
    dash.dependencies.Input('cluster_group', 'disabled'),
    dash.dependencies.Input('year', 'disabled'),
    dash.dependencies.Input('year', 'value')])
def get_companies(comps_disabled, cluster_grp_disabled, yr_disabled, yr):
    new_options = []
    if not comps_disabled and not cluster_grp_disabled and not yr_disabled and not (yr is None):
        check_df = yr_df_dict[yr]
        for comp in sorted(check_df.Name):
            new_options.append({'label': comp, 'value': comp})
    return new_options

@app.callback(
    dash.dependencies.Output('num_neighbors', 'options'),
    dash.dependencies.Input('visualization_model', 'value'))
def get_num_neighbors(vis_model):
    return [] if vis_model != 'NEAREST NEIGHBORS' else num_neighbors_options

@app.callback(
    dash.dependencies.Output('num_neighbors', 'disabled'),
    dash.dependencies.Input('visualization_model', 'value'),
    dash.dependencies.Input('companies', 'value'))
def get_num_neighbors(vis_model, comp_selected):
    return vis_model != "NEAREST NEIGHBORS" 

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    dash.dependencies.Input('visualization_model', 'value'),
    dash.dependencies.Input('cluster_group', 'value'),
    dash.dependencies.Input('year', 'value'),
    dash.dependencies.Input('companies', 'value'),
    dash.dependencies.Input('dimension_toggle', 'value'),
    dash.dependencies.Input('num_neighbors', 'value'))
def update_graph(vis_model, cluster_group, yr, comps_selected, dims, n_neighbors):
    df = yr_df_dict[yr]
    return generate_vis(df, year=int(yr), dim=int(dims), vis_type=vis_model, grp=cluster_group, num_neighbors=int(n_neighbors), companies=comps_selected, size=8)


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
