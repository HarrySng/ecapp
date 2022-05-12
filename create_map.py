"""
Author: Harry Singh
Date: 2022-04-13
"""
import folium
import numpy as np
import pandas as pd
from folium import plugins

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
    
    def conv_int(row, col):
        iy = int(row[col]) if not np.isnan(row[col]) else 'NA'
        return iy

    def create_popups(df):
        popups = []
        for i, row in df.iterrows():
            h1 = conv_int(row, 'hlystartyear')
            h2 = conv_int(row, 'hlyendyear')
            d1 = conv_int(row, 'dlystartyear')
            d2 = conv_int(row, 'dlyendyear')
            m1 = conv_int(row, 'mlystartyear')
            m2 = conv_int(row, 'mlyendyear')

            hly_btn_title = f'Download Hourly Data ({h1} - {h2})'
            dly_btn_title = f'Download Daily Data ({d1} - {d2})'
            mly_btn_title = f'Download Monthly Data ({m1} - {m2})'

            if h1 == 'NA' or h2 == 'NA':
                hly_btn_title = 'Hourly Data Not Available'
            
            if d1 == 'NA' or d2 == 'NA':
                dly_btn_title = 'Daily Data Not Available'
            
            if m1 == 'NA' or m2 == 'NA':
                mly_btn_title = 'Monthly Data Not Available'

            html = """<!DOCTYPE html>
                <html>
                    <style>
                    </style>
                    <body style="font-size: 12px;">
                    <h2>{name}, {prov}</h2>
                    <h3 id="climid">Climate ID: {id}</h3>
                    <br><br>
                    <button onclick="downloadHourlyFiles('{sid}','{h1}','{h2}')" style="background-color: #242943;color: #ffffff;border: solid 1.5px #242943;border-radius: 0;font-size: 1.5em;font-weight: 600;height: 2em;letter-spacing: 0.3em;padding: 0 1em;text-align: center;cursor: pointer;">{hbt}</button>
                    <br><br>
                    <button onclick="downloadDailyFiles('{sid}','{d1}','{d2}')" style="background-color: #242943;color: #ffffff;border: solid 1.5px #242943;border-radius: 0;font-size: 1.5em;font-weight: 600;height: 2em;letter-spacing: 0.3em;padding: 0 1em;text-align: center;cursor: pointer;">{dbt}</button>
                    <br><br>
                    <button onclick="downloadMonthlyFiles('{sid}','{m1}','{m2}')" style="background-color: #242943;color: #ffffff;border: solid 1.5px #242943;border-radius: 0;font-size: 1.5em;font-weight: 600;height: 2em;letter-spacing: 0.3em;padding: 0 1em;text-align: center;cursor: pointer;">{mbt}</button>
                    </body>
                </html>
            """.format(
                sid = row['stationid'],
                name=row['name'], 
                prov=row['province'],
                id=row['climateid'],
                hbt=hly_btn_title,
                dbt=dly_btn_title,
                mbt=mly_btn_title,
                h1=h1,h2=h2,d1=d1,d2=d2,m1=m1,m2=m2
            )
            ele_html = folium.Html(html, script=True)
            popup = folium.Popup(ele_html, max_width=2650)
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