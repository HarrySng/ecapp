"""
Author: Harry Singh
Date: 2022-04-13
"""
import folium
import branca
import numpy as np
import pandas as pd
from folium import plugins
from folium.plugins import Search

def wrapper():
    drop_cols = [
        'WMO ID', 'TC ID', 'Latitude', 'Longitude',
        'First Year', 'Last Year'
    ]

    new_cols = [
        'name', 'province', 'climateid', 'stationid', 
        'latitude', 'longitude','elevation', 
        'hlystartyear', 'hlyendyear', 
        'dlystartyear', 'dlyendyear',
        'mlystartyear', 'mlyendyear'
    ]

    def load_stations(
        provinces,
        file = 'Station Inventory EN.csv', skip = 3,
        drop_cols=drop_cols, new_cols=new_cols,
        ):
        """Load and cleanup station inventory file
    
        Args:
            file (str, optional): 
                Path to station inventory file.
            skip (int, optional): No. of header rows to skip. Defaults to 3.
    
        Returns:
            _type_: _description_
        """
        df = pd.read_csv(file, skiprows=skip)
        
        # Remove rows that do not have coordinates
        df = df[df['Latitude (Decimal Degrees)'].notna()]
        df = df[df['Longitude (Decimal Degrees)'].notna()]
        
        # Remove redundant columns
        df = df.drop(drop_cols, axis=1)
    
        # Rename remaining columns
        df.columns = new_cols
    
        # FIlter on province
        df = df[df['province'].isin(provinces)]

        # drop if all three date range columns are null
        df = df.dropna(
            subset=['hlystartyear', 'dlystartyear', 'mlystartyear'], how='all'
        )

        # Calculate data lengths for use later
        df['hlyyears'] = df['hlyendyear'] - df['hlystartyear'] + 1
        df['dlyyears'] = df['dlyendyear'] - df['dlystartyear'] + 1
        df['mlyyears'] = df['mlyendyear'] - df['mlystartyear'] + 1
    
        return df
    
    def create_popups(df):
        popups = []
        for i, row in df.iterrows():
            html = """<!DOCTYPE html>
                <html>
                    <body style="font-size: 12px;">
                    <h1>{name}, {prov}</h1>
                    <h2>Climate ID: {id}</h2>
                    <h4>Coordinates: {lat}, {lon}</h4>
                    <table style="width: 370px; border:1px solid black;">
                        <tr>
                            <th style="border:1px solid black; text-align: center; vertical-align: middle;">Frequency</th>
                            <th style="border:1px solid black; text-align: center; vertical-align: middle;">Start Year</th>
                            <th style="border:1px solid black; text-align: center; vertical-align: middle;">End Year</th>
                            <th style="border:1px solid black; text-align: center; vertical-align: middle;">Total Years</th>
                        </tr>
                        <tr>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">Hourly Data</td>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">{h1}</td>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">{h2}</td>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">{htl}</td>
                        </tr>
                        <tr>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">Daily Data</td>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">{d1}</td>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">{d2}</td>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">{dtl}</td>
                        </tr>
                        <tr>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">Monthly Data</td>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">{m1}</td>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">{m2}</td>
                            <td style="border:1px solid black; text-align: center; vertical-align: middle;">{mtl}</td>
                        </tr>
                    </table>
                    </body>
                </html>
            """.format(
                name=row['name'], 
                prov=row['province'],
                id=row['climateid'],
                lat=row['latitude'], 
                lon=row['longitude'],
                h1=int(row['hlystartyear']) if not np.isnan(row['hlystartyear']) else 'NA',
                h2=int(row['hlyendyear']) if not np.isnan(row['hlyendyear']) else 'NA',
                htl=int(row['hlyyears']) if not np.isnan(row['hlyyears']) else 'NA',
                d1=int(row['dlystartyear']) if not np.isnan(row['dlystartyear']) else 'NA',
                d2=int(row['dlyendyear']) if not np.isnan(row['dlyendyear']) else 'NA',
                dtl=int(row['dlyyears']) if not np.isnan(row['dlyyears']) else 'NA',
                m1=int(row['mlystartyear']) if not np.isnan(row['mlystartyear']) else 'NA',
                m2=int(row['mlyendyear']) if not np.isnan(row['mlyendyear']) else 'NA',
                mtl=int(row['mlyyears']) if not np.isnan(row['mlyyears']) else 'NA'
            )
            iframe = folium.IFrame(html=html, width=400, height=400)
            popup = folium.Popup(iframe, max_width=2650)
            popups.append(popup)
        return popups
                
    # Function to add marker clusters
    def add_marker_cluster(df, m, popups):
        locs = df[["latitude", "longitude"]].to_numpy() 
        plugins.MarkerCluster(locs, popups = popups).add_to(m)
        return

    # Province filters
    prov_dict = {
        'maritimes': [
            'NEW BRUNSWICK', 'NEWFOUNDLAND', 
            'NOVA SCOTIA', 'PRINCE EDWARD ISLAND'
            ],
        'prairies': ['ALBERTA', 'MANITOBA', 'SASKATCHEWAN'],
        'north': ['YUKON', 'NUNAVUT', 'NORTHWEST TERRITORIES'],
        'ontario': ['ONTARIO'],
        'quebec': ['QUEBEC'],
        'bc': ['BRITISH COLUMBIA']
    }

    # Add markers in clusters, and assing popups
    for prov in prov_dict:
        df = load_stations(prov_dict[prov])
        m = folium.Map([60, -100], zoom_start=3)
        popups = create_popups(df)
        add_marker_cluster(df, m, popups)
        m.save('templates/' + prov + '.html')

if __name__ == '__main__':
    wrapper()