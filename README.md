# weather-data-fastapi
Code challenge.
We take info from `https://api.open-meteo.com/v1/forecast` sending the params City, Latitude and Longitude and put it in a csv.
the csv can be found in the output folder.

Tools to be used:
    * FastAPI
    * Pandas
    * uvicorn
    * matplotlib
    * seaborn

In order to run this app first you must clone the repository
then cd in the weather-data-fastapi folder, 
- Create the virtual environment
    `python -m venv venv`
    or
    `python3 -m venv venv`
    (you can explore other options)
 then activate the venv

- Install the requirements -> `pip install -r requirements.txt`

- Then, in order to run the app we can run it with the following command

    `uvicorn app.main:app --reload`


 urls to be used

 - `http://127.0.0.1:8000/weather/plot` in order to see the 