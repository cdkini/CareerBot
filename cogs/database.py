import pandas as pd
import sqlite3

from discord.ext import commands


class Database(commands.Cog):
    '''
    Any commands that pertain to job storage within SQL database.
    '''

    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'Discord-Bot/data/indeed_jobs.db'

    @commands.command(help='Returns saved jobs from database')
    async def db_view(self, ctx):
        user = str(ctx.message.author.id)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute("SELECT title, company, location FROM job_postings WHERE user=?", (user,)
                  )
        
        await ctx.send('Saved jobs:')
        await ctx.send('---')

        for i, job in enumerate(c.fetchall()):
            await ctx.send(f'{i+1}: {job[0]} - {job[1]} - {job[2]}')
        await ctx.send('---')
        conn.commit()
        conn.close()

    @commands.command(help='View URL of {index} job from database')
    async def db_url(self, ctx, index):
        try:
            user = str(ctx.message.author.id)
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute("SELECT title, company, location FROM job_postings WHERE user=?", (user,)
                )

            jobs_list = []
            for job in c.fetchall():
                title, company, location, url, user, date = job   
                jobs_list.append([title, company, location, url, user, date])
                
            jobs_df = pd.DataFrame(jobs_list, columns=['Title','Company','Location', 'URL', 'User', 'Date'])
            print(jobs_df)
            job_url = jobs_df.iloc[int(index)-1]
            print(job_url)
            await ctx.send(f'https://www.indeed.com{job_url}')

        except IndexError:
            await ctx.send('Index of desired job is out of scope of query.')

    @commands.command(help='Export database as CSV to {email}')
    async def db_export(self, ctx, email):
        pass

    @commands.command(help='Delete {index} job from database')
    async def db_delete(self, ctx, email):
        pass

def setup(bot):
    bot.add_cog(Database(bot))
