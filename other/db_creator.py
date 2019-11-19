import sqlite3


def create_db():
    '''
    Creates an empty SQL database containing a table
    for Indeed job posting data.
    '''
    try:
        conn = sqlite3.connect('Discord-Bot/data/indeed_jobs.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE job_postings (
                    title text,
                    company text,
                    location text,
                    url text,
                    user text,
                    date text
                    )"""
        )

        conn.commit()
        conn.close()

    except sqlite3.OperationalError:
        print('Database already created and located in /data.')

create_db()
