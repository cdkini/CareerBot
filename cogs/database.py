import os
import pandas as pd
import pickle
import sqlite3

from discord.ext import commands


class Database(commands.Cog):
    '''
    Any commands that pertain to job storage within SQL database.
    '''

    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'Discord-Bot/data/indeed_jobs.db'
        self.pickle_path = 'Discord-Bot/data/database.pickle'

    @commands.command(help='View saved jobs; run before other db_functions')
    async def db_refresh(self, ctx):
        user = str(ctx.message.author.id)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute("SELECT * FROM job_postings WHERE user=?", (user,)
        )

        await ctx.send('Saved jobs:')
        await ctx.send('- - -')

        jobs_list = []
        for i, job in enumerate(c.fetchall()):
            title, company, location, url, user, date = job
            await ctx.send(f'{i+1}: {title} - {company} - {location}')
            jobs_list.append([title, company, location, url, user, date])

        await ctx.send('- - -')

        conn.commit()
        conn.close()

        jobs_df = pd.DataFrame(jobs_list, columns=[
                               'Title', 'Company', 'Location', 'URL', 'User', 'Date']
        )

        pickle_out = open(self.pickle_path, 'wb')
        pickle.dump(jobs_df, pickle_out, protocol=2)
        pickle_out.close()

    @commands.command(help='View URL of {index} job from database')
    async def db_url(self, ctx, index):
        try:
            pickle_in = open(self.pickle_path, 'rb')
            jobs_df = pickle.load(pickle_in)
            job_url = jobs_df['URL'].iloc[int(index)-1]
            await ctx.send(f'https://www.indeed.com{job_url}')

        except FileNotFoundError:
            await ctx.send('Please use -db_refresh before conducting any database operations.')
        except IndexError:
            await ctx.send('Index of desired job is out of scope of query.')

    @db_url.error
    async def url_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the index of the saved job.')

    @commands.command(help='Delete {index} saved job from database')
    async def db_delete(self, ctx, index):
        try:
            pickle_in = open(self.pickle_path, 'rb')
            jobs_df = pickle.load(pickle_in)
            job_url = jobs_df['URL'].iloc[int(index)-1]

            user = str(ctx.message.author.id)
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute("DELETE FROM job_postings WHERE user=? AND url=?", (user, job_url)
            )

            conn.commit()
            conn.close()

            await ctx.send('Job deleted from database.')

        except FileNotFoundError:
            await ctx.send('Please use -db_refresh before conducting any database operations.')
        except IndexError:
            await ctx.send('Index of desired job is out of scope of query.')

    @db_delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the index of the saved job.')

    @commands.command(help='Delete all saved jobs from database')
    async def db_delete_all(self, ctx):
        user = str(ctx.message.author.id)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute("DELETE from job_postings WHERE user=?", (user,)
        )

        conn.commit()
        conn.close()

        if os.path.exists(self.pickle_path):
            os.remove(self.pickle_path)

        await ctx.send('Database cleared.')


def setup(bot):
    bot.add_cog(Database(bot))
