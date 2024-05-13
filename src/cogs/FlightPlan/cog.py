import nextcord
from nextcord.ext import commands
from urllib.parse import urlparse, parse_qs, urlencode
from datetime import datetime
import aiohttp
import random
# Import the icao.py file
import icao

from config import GUILD_ID, GOOGLE_API_KEY, GOOGLE_API_CONTEXT, BITLY_ACCESS_TOKEN



class FlightPlan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✈️  {self.__class__.__qualname__} STARTED")


    @nextcord.slash_command(description="Retrieve flight plan from a SimBrief URL and display the flight info.", guild_ids=[GUILD_ID])
    async def flight_plan(self, interaction: nextcord.Interaction, url: str):
        # Validate the URL
        if not url.startswith("https://dispatch.simbrief.com/"):
            await interaction.response.send_message("Invalid flight plan URL. Please provide a URL starting with 'https://dispatch.simbrief.com/'", ephemeral=True)
            return
        
        # Parse the URL
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Extract the relevant information
        airline = query_params.get('airline', ['<Not Set>'])[0]
        airline_code = airline
        fltnum = query_params.get('fltnum', ['<Not Set>'])[0]
        orig = query_params.get('orig', ['<Not Set>'])[0]
        dest = query_params.get('dest', ['<Not Set>'])[0]
        date = query_params.get('date', ['<Not Set>'])[0]
        basetype = query_params.get('basetype', ['<Not Set>'])[0]
        reg = query_params.get('reg', ['<Not Set>'])[0]
        route = query_params.get('route', ['<Not Set>'])[0]

        user = interaction.user.name

        # Function to retrieve airport and airline info from icao.py file
        def get_airport_info(code):
            airport_name = icao.airports.get(code, f"<Unknown>")
            return f"{code} ({airport_name})"

        def get_airline_info(code):
            airline_name = icao.airlines.get(code, f"<Unknown Airline>")
            return f"{airline_name} ({code})"

        # Convert date and time to Unix timestamp
        if date != '<Not Set>':
            dt_format = "%d %b %Y - %I:%M %p"
            dt = datetime.strptime(date, "%d %b %Y - %H:%M")
            unix_timestamp = int(dt.timestamp())
            date_formatted = f"<t:{unix_timestamp}:F>"
        else:
            date_formatted = date

        # Get airport and airline info
        departing_info = get_airport_info(orig)
        arriving_info = get_airport_info(dest)
        airline_info = get_airline_info(airline_code)

        # Prepend airline code to the flight number without a space
        flight_number = f"{airline_code}{fltnum}"

        # Function to shorten a URL using the Bitly API
        async def shorten_url(long_url, access_token):
            # Define the Bitly API URL
            bitly_url = "https://api-ssl.bitly.com/v4/shorten"
            
            # Define the request headers and payload
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "long_url": long_url,
                "domain": "bit.ly"  # Use the default Bitly domain for short links
            }
            
            # Make the API request to shorten the URL
            async with aiohttp.ClientSession() as session:
                async with session.post(bitly_url, json=payload, headers=headers) as response:
                    data = await response.json()
                    # Return the shortened URL
                    return data.get("link")

        # Shorten the provided URL
        shortened_url = await shorten_url(url, BITLY_ACCESS_TOKEN)
        
        # Function to search for an image URL based on the basetype
        async def google_image_search(query):
            search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={GOOGLE_API_CONTEXT}&key={GOOGLE_API_KEY}&searchType=image&num=1"
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url) as response:
                    data = await response.json()
                    if 'items' in data and len(data['items']) > 0:
                        return data['items'][0]['link']
                    return None
        
        # Get the image URL for the given basetype
        image_url = await google_image_search(f"{basetype} aircraft site:wikipedia.org")

        # Get the thumbnail URL for the airline logo
        airline_logo_query = f"{airline_code} Airline logo site:tradingview.com"
        airline_logo_url = await google_image_search(airline_logo_query)

        # Create a Discord embed
        embed = nextcord.Embed(
            title=f"Flight Plan for {flight_number}",
            url=f"{shortened_url}",
            description=f"{airline_info} now boarding flight {fltnum}. Departure <t:{unix_timestamp}:R>.",
            colour=0x00b0f4
        )

        embed.add_field(name="Airline", value=airline_info, inline=True)
        embed.add_field(name="Flight No.", value=flight_number, inline=True)
        embed.add_field(name="", value="", inline=False) # Just spacers
        embed.add_field(name="Departing", value=departing_info, inline=True)
        embed.add_field(name="Arriving", value=arriving_info, inline=True)
        embed.add_field(name="", value="", inline=False) # Just spacers
        embed.add_field(name="Date & Time", value=date_formatted, inline=False)
        embed.add_field(name="", value="", inline=False) # Just spacers
        embed.add_field(name="Aircraft", value=basetype, inline=True)
        embed.add_field(name="Registration", value=reg, inline=True)
        embed.add_field(name="", value="", inline=False) # Just spacers
        
        # Format the flight route with right arrow emojis
        if route != "<Not Set>":
            formatted_route = route.replace(" ", " ")
            embed.add_field(name="Flight Route", value=formatted_route, inline=False)
        else:
            embed.add_field(name="Flight Route", value=route, inline=False)
        
        # Set the image URL in the embed
        if image_url:
            embed.set_image(url=image_url)
        else:
            embed.set_image(url="https://cdn.discordapp.com/attachments/1215427100761129003/1228480736689127466/failed.png?ex=662c32d7&is=6619bdd7&hm=dc41bc45d73ab9d923ebf3f39280167fd6398b350dccf9370bc4331e1df87445&")
            print
        
        # Set the airline logo as the thumbnail URL in the embed
        #if airline_logo_url:
            embed.set_thumbnail(url=airline_logo_url)
        #else:
            embed.set_thumbnail(url=None)

        embed.set_footer(text="Envisioned by Joseph_fallen, coded by MxM & ChatGPT")

        # Send the embed as a response
        await interaction.response.send_message(embed=embed)


    @nextcord.slash_command(description="Modify flight plan URL by providing flight number, airline, and aircraft.", guild_ids=[GUILD_ID])
    async def modify_flight(self, interaction: nextcord.Interaction, url: str, flight_number: str, airline: str, aircraft: str):
        # Validate that the URL starts with "https://dispatch.simbrief.com/"
        if not url.startswith("https://dispatch.simbrief.com/"):
            await interaction.response.send_message("Invalid flight plan URL. Please provide a URL starting with 'https://dispatch.simbrief.com/'", ephemeral=True)
            return

        # Check if the provided airline code exists in the dictionary of existing airlines
        if airline not in icao.airlines:
            await interaction.response.send_message(f"The airline code '{airline}' does not exist. Please provide a valid airline code.", ephemeral=True)
            return

        # Check if the provided aircraft code exists in the dictionary of existing aircraft
        if aircraft not in icao.aircraft:
            await interaction.response.send_message(f"The aircraft code '{aircraft}' does not exist. Please provide a valid aircraft code.", ephemeral=True)
            return

        # Parse the given URL
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Update the 'airline', 'fltnum', and 'basetype' parameters with the new values
        query_params['airline'] = [airline]
        query_params['fltnum'] = [flight_number]
        query_params['basetype'] = [aircraft]

        # Encode the query parameters
        updated_query = urlencode(query_params, doseq=True)

        # Construct the modified URL
        modified_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{updated_query}"

        # Define your Bitly API access token
        bitly_access_token = "95d950fdc9ff888126bca9f9087463052c1dcc1d"

        # Function to shorten a URL using the Bitly API
        async def shorten_url(long_url, access_token):
            # Define the Bitly API URL
            bitly_url = "https://api-ssl.bitly.com/v4/shorten"
            
            # Define the request headers and payload
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "long_url": long_url,
                "domain": "bit.ly"  # Use the default Bitly domain for short links
            }
            
            # Make the API request to shorten the URL
            async with aiohttp.ClientSession() as session:
                async with session.post(bitly_url, json=payload, headers=headers) as response:
                    data = await response.json()
                    # Return the shortened URL
                    return data.get("link")

        # Shorten the modified URL
        shortened_url = await shorten_url(modified_url, bitly_access_token)

        # Send the modified URL as an ephemeral message
        await interaction.response.send_message(f"The modified flight plan URL is: {shortened_url}", ephemeral=True)

    
        
        
def setup(bot):
    bot.add_cog(FlightPlan(bot))