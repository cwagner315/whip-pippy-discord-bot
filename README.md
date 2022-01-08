# whip-pippy-discord-bot
Discord bot for server management. 


1. Installation instrucitons.. 
	
	pip install -U discord.py
	pip install -U python-dotenv

	OR
	 
	pip3 install -U discord.py
	pip3 install -U python-dotenv
	
2. Edit the .env file to change the server(guild) and the authorization token.

 ## commands
 
 ### !lap [target]

Initiates a one minute timed vote for (3/5) of the target members current *voice channel non-self-defeaned members* to 
cast a vote by typing ** !lap ** if the mute is successful it will server mute the target user for a random amount of 
seconds between 15-120.

Command use: !lap Optional[target] to start a vote.

ex:
	!lap @pipe_down
	!lap # Defaults: @pipe_down