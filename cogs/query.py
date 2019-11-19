import os
import pandas as pd
import pickle
import sqlite3
import urllib.request

from bs4 import BeautifulSoup
from datetime import datetime as dt
from discord.ext import commands


class Query(commands.Cog):
    '''
    Any commands that directly relate to scraped Indeed
    data and related queries.
    '''

    def __init__(self, bot):
        self.bot = bot
        self.pickle_path = 'Discord-Bot/data/jobs.pickle'
        self.db_path = 'Discord-Bot/data/indeed_jobs.db'

    @commands.command(help='Input {"title/location/exp"} (entry/mid/senior)')
    # Primary command used to generate scrape query; stores results as pickle
    async def generate(self, ctx, criteria):

        if criteria.count('/') != 2:
            await ctx.send('Please ensure that your query is formatted properly (see -help).')
            return 'Improper format.'

        # Create BeautifulSoup object for scraping job data
        title, location, exp = criteria.replace(' ', '+').split('/')
        url = f'https://www.indeed.com/jobs?q={title}&l={location}&explvl={exp}_level'
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
        soup = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})

        print('Soup cooked.')

        # Appending scraped job data into list of lists and converting into pd.DataFrame
        jobs_list = []
        for posting in soup:
            job = posting.find(
                'a', attrs={'data-tn-element': 'jobTitle'}).text.strip()
            company = posting.find(
                'span', attrs={'class': 'company'}).text.strip()
            location = posting.find('span', attrs={
                'class': 'location accessible-contrast-color-location'}).text.strip()
            url = posting.find(
                'a', attrs={'class': 'turnstileLink'}).attrs['href']

            jobs_list.append([job, company, location, url])

        print('Indeed scraped.')

        if not jobs_list:
            await ctx.send('No results found; please review your query.')
            return 'No results found.'

        jobs_df = pd.DataFrame(jobs_list, columns=[
                               'Title', 'Company', 'Location', 'URL'])

        print('Dataframe generated.')

        await ctx.send(f'{jobs_df.shape[0]} jobs found that meet your critera:')
        await ctx.send('- - -')

        for i, row in jobs_df.iterrows():
            await ctx.send(f"{i+1}: {row['Title']} - {row['Company']}")

        await ctx.send('- - -')
        await ctx.send('Utilize -url or -save to view or store individual postings, respectively.')

        # Creating pickle object to save pd.DataFrame for use in other functions
        pickle_out = open(self.pickle_path, 'wb')
        pickle.dump(jobs_df, pickle_out, protocol=2)
        pickle_out.close()

    @generate.error
    async def generate_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please input query criteria using the format found in -help.')

    @commands.command(help='Deletes job query')
    async def clear(self, ctx):
        if os.path.exists(self.pickle_path):
            os.remove(self.pickle_path)
            await ctx.send('Query cleared. Use -generate to create a new query.')
        else:
            await ctx.send('No query to delete. Use -generate to create a new query.')

    @commands.command(help='Generates URL of {index} job from query')
    async def url(self, ctx, index):
        try:
            pickle_in = open(self.pickle_path, 'rb')
            jobs_df = pickle.load(pickle_in)
            job_url = jobs_df['URL'].iloc[int(index)-1]
            await ctx.send(f'https://www.indeed.com{job_url}')
        except FileNotFoundError:
            await ctx.send('Query not found; please use -generate to create a query.')
        except IndexError:
            await ctx.send('Index of desired job is out of scope of query.')

    @url.error
    async def url_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the index of the saved job.')

    @commands.command(help='Saves {index} job to database')
    async def save(self, ctx, index, date=dt.today().strftime('%m/%d/%Y')):
        try:
            pickle_in = open(self.pickle_path, 'rb')
            jobs_df = pickle.load(pickle_in)
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            title, company, location, url = jobs_df.iloc[int(index)-1]
            user = str(ctx.message.author.id)
            c.execute("INSERT INTO job_postings VALUES (?, ?, ?, ?, ?, ?)",
                      (title, company, location, url, user, date)
                      )
            conn.commit()
            conn.close()

            await ctx.send('Job posting saved in database. Use -db_refresh to see all saved postings.')

        except FileNotFoundError:
            await ctx.send('Query not found; please use -generate to create a query.')
        except IndexError:
            await ctx.send('Index of desired job is out of scope of query.')
        except sqlite3.OperationalError:
            print('Database already created and located in /data.')

    @save.error
    async def save_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the index of the saved job.')


def setup(bot):
    bot.add_cog(Query(bot))
