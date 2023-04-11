import pandas
import requests
import re
from geopy.distance import geodesic
from bs4 import BeautifulSoup

def geofence(achnor:tuple, point2:tuple, dist:int):
    #* Takes in 2 points (Latitude,Longitude)
    #* ex: achnor=(43.40886,-89.73611) point2=(43.42098,-89.73728) a distance in ft dist=528
    return geodesic(achnor, point2).ft < dist

def get_webpage(url:str):
    r = requests.get(url)
    print(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_votes_from_html(soup):
    #* Gets Votes from the MP webpage
    votes = soup.find(id="route-star-avg").text
    votes = votes.replace(" ", "").replace("\n","").replace("from","vote")
    total_votes = votes.split("vote")[-2]
    return(total_votes)

def get_views_total_from_html(soup):
    #* Gets Views Total from the MP webpage
    views = str(soup.body.find(text=re.compile('/month\n')))
    views = views.replace("\n","").replace(" ","").replace(",","").replace("·","").replace("/","").replace("month","").split("total")
    total_views = int(views[0])
    return(total_views)

def get_views_month_from_html(soup):
    #* Gets Views per month from the MP webpage
    views = str(soup.body.find(text=re.compile('/month\n')))
    views = views.replace("\n","").replace(" ","").replace(",","").replace("·","").replace("/","").replace("month","").split("total")
    per_month_views = int(views[1])
    return(per_month_views)

def get_date_from_html(soup):
    #* Gets Views from the MP webpage
    table=soup.find("table",{"class":"description-details"})
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if "Shared By:" in cells[0]:
            data = cells[1].text
            data = data.replace(" ","").split("\n")
            date = data[2].replace("on","")
    return date

def add_html_to_df(df:pandas.DataFrame, new_csv:str):
    df['raw_html'] = df['URL'].map(get_webpage)
    df.to_csv(new_csv)

def add_data_to_csv(df:pandas.DataFrame, new_csv:str):
    df['votes'] = df['raw_html'].map(get_votes_from_html)
    df['view'] = df['raw_html'].map(get_views_total_from_html)
    df['view_month'] = df['raw_html'].map(get_views_month_from_html)
    df['date'] = df['raw_html'].map(get_date_from_html)
    df = df.drop(['raw_html'], axis=1)
    df.to_csv(new_csv)

def write_to_html(df:pandas.DataFrame, name:str, web_template_file:str, output_html_filename:str):
    #* Takes in dataframe and name, then creates the html from it for the webpage
    data = ""
    for index, row in df.iterrows():
        data = data + '<tr>' + '<td class="lalign" id="filter_col1" data-column="0">' + row["Route"]+ '</td>' + "\n"
        data = data + '<td class="lalign" id="filter_col2" data-column="1">' + str(row["Rating"]) + '</td>' + "\n"
        data = data + '<td class="lalign" id="filter_col3" data-column="2">' + str(row["Avg Stars"]) + '</td>' + "\n"
        data = data + '<td class="lalign" id="filter_col3" data-column="3">' + str(row["votes"]) + '</td>' + "\n"
        data = data + '<td class="lalign" id="filter_col3" data-column="3">' + str(row["view"]) + '</td>' + "\n"
        data = data + '<td class="lalign" id="filter_col3" data-column="3">' + str(row["view_month"]) + '</td>' + "\n"
        data = data + '<td class="lalign" id="filter_col3" data-column="3">' + str(row["boulders_in_geofence"]) + '</td>' + "\n"
        data = data + '<td class="lalign" id="filter_col3" data-column="3">' + str(row["date"]) + '</td>' + "\n"
        data = data + '<td class="lalign" id="filter_col3" data-column="3" ><a href="' + row["URL"] +'">link</td>' + "\n"
        data = data + '<td class="lalign" id="filter_col3" data-column="3">' + row["Location"] + '</td>'+'</tr>' + "\n"
        data = data + "\n"
    file_template = open(web_template_file, "r")
    html = file_template.read()
    file_template.close()
    html = html.replace("{{data}}", data)
    html = html.replace("{{Name}}", name)
    new_file = open(output_html_filename, "w")
    new_file.write(html)
    new_file.close()


def rebuild_df_cache(routes_downloaded_from_mp:str, new_csv:str):
    #* Add Votes and Views to CSV, Its slow so use this like a cache
    #* It needs to do a web call to each route, so its very slow.
    raw_csv_df = pandas.read_csv(routes_downloaded_from_mp)
    add_html_to_df(raw_csv_df, new_csv)
    add_data_to_csv(raw_csv_df, new_csv)
    

def main():
    #? VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE 
    #? VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE 
    #? VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE 
    #? VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE 

    rebuild_cache = False
    location = "DL Boulders"
    grade_regex = ".*" #'.[0-7]' # "# '.
    votes_more_than = 0
    views_total_more_than = 0
    views_month_more_than = 0
    stars_more_than = 0.0
    distance_in_ft  = 528 #0.1 of a mile is 528
    orginal_mp_csv_download = 'route-finder-all-dl.csv'
    combined_local_csv_name = 'routes_cache.csv'
    output_html_filename = "index.html"

    # Testing on small Sample
    # orginal_mp_csv_download = 'route-finder copy.csv'
    # combined_local_csv_name = 'routes_csv.csv'

    #? VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE 
    #? VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE 
    #? VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE 
    #? VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE #* VARS TO CHANGE 

    #* Adds votes to MP route downloaded csv. Needs this on first run for a location
    if rebuild_cache:
        rebuild_df_cache(orginal_mp_csv_download, combined_local_csv_name)
        
    #* Locations to zoom on, Not needed unless used for write_to_html_distance(*) is being used
    # south_ghost = (43.40886,-89.73611)
    # west_middle = (43.42098,-89.73728) 
    # east_bigbud = (43.42737,-89.72676)
    # south_reserve = (43.40436,-89.72961)
    # dl_lake_center = (43.41808001721097, -89.73159990417643)

    #* Reads in the Routes, and then uses regex to filer the grades, then makes the webpage with that DF and filters on the distance based on the given anchor
    #? CSV Keys : Route,Location,URL,Avg Stars,Your Stars,Route Type,Rating,Pitches,Length,Area Latitude,Area Longitude,votes
    df = pandas.read_csv(combined_local_csv_name)

    df = df.loc[df['Rating'].str.contains(grade_regex, regex=True)] 
    df = df.loc[df['votes'] > votes_more_than]
    df = df.loc[df['view'] > views_total_more_than]
    df = df.loc[df['view_month'] > views_month_more_than]
    df = df.loc[df['Avg Stars'] > stars_more_than]

    # df loc messes up the index numbers, it doesnt set them to 0,1,2,3 it just removes the filtered ones. So 0,4,5,10,14
    df = df.reset_index()
 
    # Adding GeoFence counts into df
    df["boulders_in_geofence"] = 0
    for index, row in df.iterrows():
        anchor = (row["Area Latitude"], row["Area Longitude"])
        for index2, row2 in df.iterrows():
            point = (row2["Area Latitude"], row2["Area Longitude"])
            if df['Route'][index] != df['Route'][index2]:
                if geofence(anchor, point, distance_in_ft):
                    df.iat[index,-1] = df['boulders_in_geofence'][index] + 1

    total_climbs = len(df.index)
    name = (location + "\n in range v" + str(grade_regex) .replace('.',"").replace(']',"").replace('[',"") + "\n with more than " + str(stars_more_than) +" stars, "+ str(views_total_more_than) +"/"+ str(views_month_more_than) +  "\n page views total/per month and " + str(votes_more_than) +  "\n votes in " +str(distance_in_ft) + "ft" + "\n Total Climbs:" + str(total_climbs))
    write_to_html(df=df, name=name, web_template_file="index_template_b.html", output_html_filename=output_html_filename)

if __name__ == '__main__':
    main()
