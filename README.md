# soccer_stats

Sports statistics is something that really facinates me.  I thought it would be fun to gather soccer statistics in one location so I could easily see how players from different leagues compare without having to go to all of the league sites individually.

This project uses the following features to extract soccer statistics and display them in an easy-to-use web interface

* Consumes a series of public APIs to retrieve player data.  Uses requests library to post to the webservice.
* Navigates to the various league websites to retrieve player photo urls.  This involved APIs and webscraping.  Uses requests (API consumption), BeautifulSoup (webscraping), and jsonpath_ng.ext (parsing json using wildcards).
* Uses psycopg2 and psycopg2.extras to create the underlying PostgreSQL database, tables, and to insert the data.
* Uses pandas to create the raw DataFrames for data cleaning and databse inserts.
* Uses flask to build API endpoints used by the web frontend to populate dropdowns, the datagrid, and player photo and biographical information.
* Uses d3 to retrieve json data as well as html elements for data visualization.
* Uses grid.js to bind the json data for visualization.

