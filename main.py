from discord.ext import commands
import discord
import glob
import requests
help_command = commands.DefaultHelpCommand(
    no_category = 'Bot Commands'
)
bot = commands.Bot(command_prefix='+', help_command = help_command, description = 'Make sure to add + before each command.')

@bot.event
async def on_ready():	
	guild_count = 0
	for guild in bot.guilds:		
		guild_count = guild_count + 1
	print("BOT is in " + str(guild_count) + " guilds.")

@commands.command(name="gen", 
help="remove the <> and replace 'service' with the service name.",
brief="Use this command to retrive an account."
)
@commands.guild_only()
async def gen(ctx, service):
  args = service.lower()
  stock = glob.glob("Accounts/*.txt")
  
  if str(args) in str(stock):
    try:
      with open(f"Accounts/{args}.txt", "r") as f:
        accounts = f.readlines()
        f.close()
        account = accounts[0]
        account = str(account.replace('\n', ''))
        accounts.pop(0)
        with open(f"Accounts/{args}.txt", "w") as new_f:
            for acc in accounts:        
                new_f.write(acc)
      account = discord.Embed(title="", description=f'Your **{args.capitalize()}** account:\n```{account}```',  color=0x34eb7d)
      await ctx.author.send(embed=account)
      success = discord.Embed(title="", description=f'{ctx.author.mention} success! Check you messages for your account.',  color=0x34eb7d)
      await ctx.channel.send(embed=success)
    except IndexError:
        error = discord.Embed(title="", description=f'{ctx.author.mention} error! No accounts left.',  color=0xff4053)
        await ctx.channel.send(embed=error)
    except Exception as e:
      print(e)
      e = str(e)
      e = e.split("):")[1]
      error = discord.Embed(title="", description=f'{ctx.author.mention} error! {e}',  color=0xff4053)
      await ctx.channel.send(embed=error)
  else:
    error = discord.Embed(title="", description=f'{ctx.author.mention} error! No a valid service',  color=0xff4053)
    await ctx.channel.send(embed=error)

@commands.command(name="stock",
help="Gives a list of whats available and how much.",
brief="Use this command to check services.")
@commands.guild_only()
async def stock(ctx):
  stock = glob.glob("Accounts/*.txt")
  embeds =[]
  for service in stock:
    f = open(service, "r")
    Content = f.read() 
    Counter = 0
    CoList = Content.split("\n") 
    for i in CoList: 
     if i: 
         Counter += 1
    service = str(service.replace('Accounts/', '').replace('.txt', '').capitalize())
    service = f'**{service.capitalize()}**' +": `{}`".format(str(Counter))
    embeds.append(service)
  f.close()
  brk = '\n{}\n'.format('-'*30)
  s = brk.join(embeds) 
  finalembed = discord.Embed(title='Stock', description='\n' + s , color=0x001A96)
  await ctx.channel.send(embed=finalembed)



@commands.command(name="restock",
help="Restock",
brief="Use this command to restock or add services.")
@commands.guild_only()
async def restock(ctx, service_type):
  stock_type = service_type.lower()
  if ctx.message.attachments[0].size > 0:
    attachment_url = ctx.message.attachments[0].url
    data = requests.get(attachment_url).text
    with open(f'Accounts/{stock_type}.txt','a')as c:
      c.write(str(data))
    success = discord.Embed(title="Success!", description=f'{ctx.author.mention}! {stock_type.capitalize()} has been restocked.',  color=0xff4053)
    await ctx.channel.send(embed=success)

bot.add_command(restock)
bot.add_command(gen)
bot.add_command(stock)
bot.run('ODMzNTI2MzcyMDA1NDQ1NzAy.YHzn7Q.JOVuuDTTRvZEJOu39DkMhMB6Ds0')