import sqlite3

import pandas as pd
from IPython.display import Markdown, display


conn = sqlite3.connect("sql-murder-mystery.db")


def lazy_avoid_typing_conn(query: str) -> pd.DataFrame:
    return pd.read_sql_query(query, conn)


lazy_avoid_typing_conn(
    """
SELECT "membership_id",
       "check_in_date",
       "check_in_time",
       "check_out_time"
FROM   "get_fit_now_check_in"
LIMIT  1000 """
)


lazy_avoid_typing_conn(
    '''SELECT "description"
FROM   "crime_scene_report"
WHERE  date = 20180115
       AND type = "murder"
       AND city = "SQL City"'''
)["description"].iloc[0]


display(Markdown("## Clue 2"))
display(
    Markdown(
        lazy_avoid_typing_conn(
            '''SELECT "description"
FROM   "crime_scene_report"
WHERE  date = 20180115
       AND type = "murder"
       AND city = "SQL City"'''
        )["description"].iloc[0]
    )
)


lazy_avoid_typing_conn(
    '''SELECT
    "id", 
    "name", 
    "license_id", 
    "address_number", 
    "address_street_name", 
    "ssn",
    MAX("address_number") AS last_house
FROM "person"
WHERE "address_street_name" = "Northwestern Dr"'''
)


lazy_avoid_typing_conn(
    '''SELECT
    "id", 
    "name", 
    "license_id", 
    "address_number", 
    "address_street_name", 
    "ssn"
FROM "person"
WHERE "address_street_name" = "Franklin Ave" AND "name" LIKE "Annabel%"'''
)


display(Markdown("## Clue 3"))
for i in range(2):
    display(
        Markdown(
            lazy_avoid_typing_conn(
                """SELECT "person_id",
           "transcript"
    FROM   "interview"
    WHERE  person_id = 14887
            OR person_id = 16371"""
            )["transcript"].iloc[i]
        )
    )
    print()


lazy_avoid_typing_conn(
    """SELECT *
FROM   get_fit_now_member
       INNER JOIN person
               ON get_fit_now_member.person_id = person.id
       INNER JOIN drivers_license
               ON person.license_id = drivers_license.id
WHERE  get_fit_now_member.membership_status = 'gold'
       AND get_fit_now_member.id LIKE '48Z%'
       AND drivers_license.plate_number LIKE '%H42W%' """
)


display(Markdown("## Clue 4"))
display(
    Markdown(
        lazy_avoid_typing_conn(
            """SELECT "transcript"
FROM   "interview"
WHERE  "person_id" = 67318;  """
        )["transcript"].iloc[0]
    )
)


lazy_avoid_typing_conn('''SELECT *
FROM 
  drivers_license
INNER JOIN person
ON drivers_license.id = person.license_id
INNER JOIN facebook_event_checkin
ON person.id = facebook_event_checkin.person_id
WHERE 
  drivers_license.height BETWEEN 65 
  AND 67 
  AND drivers_license.car_make = "Tesla" 
  AND drivers_license.hair_color = "red" 
  AND drivers_license.gender = "female"
  AND event_name = "SQL Symphony Concert"
GROUP BY person.id''')


lazy_avoid_typing_conn("SELECT * FROM person WHERE id = 99716")


get_ipython().run_cell_magic("bash", "", """sqlite3 sql-murder-mystery.db "INSERT INTO solution VALUES (1, 'Miranda Priestly');SELECT value FROM solution;"""")
