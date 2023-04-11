# MP Route Sorter

### Description
Mountain project sucks at sorting routes. This adds more columns to be able to sort. Coloumns include:
- Total Views (new)
- Views By Month (new)
- Added Date (new)
- Grade
- Votes
- Stars
- Area
- URL
- Boulders Close (new) - Shows other Boulders that are within x yards and in the filter

### Running

*Vars*
```    
    rebuild_cache = True
    location = "DL Boulders"
    grade_regex = ".*" # selects all boulders
    votes_more_than = 0
    views_total_more_than = 0
    views_month_more_than = 0
    stars_more_than = 0.0
    distance_in_ft  = 528 #0.1 of a mile is 528
    orginal_mp_csv_download = 'route-finder-all-dl.csv'
    combined_local_csv_name = 'routes_csv.csv'
    output_html_filename = "index.html"
```

Steps:
1. Download csv from mountain project using: https://www.mountainproject.com/route-finder
2. Save CSV in main directory, this name is used in var -> **orginal_mp_csv_download**
3. The code will scan every URL  from this csv. This takes a while, so it will build a cache so it can be ran mutiple times at after storing the info it needs. The var that controls this is **rebuild_cache**. The first time the code is ran, set **rebuild_cache** to *True* so it can create new columns in the cache csv. Then you can set **rebuild_cache** to *False* and it will used the cached version stored in the **combined_local_csv_name** var.
4. Once ran it will build a webpage with the name passed in the **output_html_filename**
5. Once this is running, feel free to experiment with different settings on the filters vars:

```
    grade_regex = ".*" # selects all boulders
    votes_more_than = 0
    views_total_more_than = 0
    views_month_more_than = 0
    stars_more_than = 0.0
    distance_in_ft  = 528 #0.1 of a mile is 528
```

## Picture of webpage

![page](https://github.com/ky-nolan/mp/blob/master/static/screenshot.png)