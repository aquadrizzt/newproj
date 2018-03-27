import copy 
import os 
import random 
import shutil
import sys 

# get_role_descriptions - this is called when information files are generated.
def get_role_description(role):
	return { 
		'Lover' 		: 'The person you see is 1) on your team and 2) aware that you are on their team.',
		'Socialite'		: 'You see three connections between pairs of people. Two of those connections are true, and represent actual connections between Information roles. The other connection is false.',
		'Assistant'		: 'The two people you see are both Information roles, but are on opposite teams.',
		'Informant' 	: 'You know which Good and Evil roles are present in the game, but not who has any specific role..', 
		'Detective' 	: 'You know which people have Evil roles, but not who has any specific role.',
		'Mastermind' 	: 'You know not only which Evil roles are in the game, but also who has each role.', 
		'Operative' 	: 'You are hidden from all Good Information roles.',
		'Saboteur' 		: 'You may play Reversal cards while on missions.',
		'Factotum'		: 'You have one additional Active modifier.' ,
		'Celebrity' 	: 'After you are on a mission that Fails, you may declare as the Celebrity.' ,
		'Enforcer'		: 'You must play Fail cards while on missions. If you are on a mission that Succeeds, you may declare as the Enforcer to cause it to Fail instead.',
	}.get(role,'ERROR: No role of that name.')

# get_role_information: this is called to populate information files 
# socialite is not handled here due to complexity
def get_role_information(my_player,players):
	return { 
		'Lover' 		: [player.name for player in players if player.role is 'Lover' and player.team is my_player.team and player is not my_player],
		'Socialite'		: [],
		'Assistant'		: random.sample([random.sample([player.name for player in players if player.team is 'Evil' and player.type is 'Information' and player.role is not 'Operative'],1)[0],random.sample([player.name for player in players if player.team is 'Good' and player.type is 'Information'],1)[0]],2),
		'Informant' 	: [player.role for player in players if  player is not my_player],
		'Detective' 	: [player.name for player in players if player.team is 'Evil' and player.role is not 'Operative'],
		'Mastermind' 	: [player.name for player in players if player.team is 'Evil' and player is not my_player],
		'Operative' 	: [],
		'Saboteur' 		: [],
		'Factotum'		: [],
		'Celebrity' 	: [],
		'Enforcer'		: [],
	}.get(my_player.role,[])

def get_role_type(role):
	return { 
		'Lover' 		: 'Information',
		'Socialite'		: 'Information',
		'Assistant'		: 'Information',
		'Informant' 	: 'Information',
		'Detective' 	: 'Information',
		'Mastermind' 	: 'Information',
		'Operative' 	: 'Information',
		'Saboteur' 		: 'Ability',
		'Factotum'		: 'Ability',
		'Celebrity' 	: 'Ability',
		'Enforcer'		: 'Ability',
	}.get(role,'ERROR: No role of that name.')

class Player():
	# players have the following traits
	# name: the name of the player as fed into system arguments 
	# role: the role the player possesses
	# team: whether hte player is good or evil 
	# type: information or ability 
	# seen: a list of what they will see
	# modifier: the random modifier this player has [NOT CURRENTLY UTILIZED]
	def __init__(self,name): 
		self.name = name 
		self.type = None 
		self.role = None 
		self.team = None 
		self.modifier = None 
		self.info = []

	def set_role(self, role):
		self.role = role
		self.type = get_role_type(role)

	def set_team(self, team):
		self.team = team

	def add_info(self,info):
		self.info += info

	def generate_info(self,players):
		pass

def main(): 
	if not (6 <= len(sys.argv) <= 11):
		print('ERROR: Invalid number of players.')
		exit(1)
	player_names = sys.argv[1:]
	num_players = len(player_names)
	player_names = list(set(sys.argv[1:])) # removes duplicates
	if len(player_names) != num_players:
		print('ERROR: Duplicate player names.')
		exit(1)

	# create player objects
	players = []
	for i in range(0,len(player_names)):
		player = Player(player_names[i])
		players.append(player)

	# number of good and evil roles
	if num_players < 7: 
		num_evil = 2 
	elif num_players < 9:
		num_evil = 3
	else: 
		num_evil = 4
	num_good = num_players - num_evil 

	# establish available roles
	good_roles = ['Socialite','Assistant','Lover','Lover','Saboteur','Detective','Celebrity','Informant']
	evil_roles = ['Socialite','Assistant','Lover','Lover','Saboteur','Mastermind','Enforcer','Operative']
	good_roles_in_game = random.sample(good_roles,num_good)
	evil_roles_in_game = random.sample(evil_roles,num_evil)

	# remove lone lovers
	if good_roles_in_game.count('Lover') == 1: 
		available_roles = set(good_roles)-set(good_roles_in_game)-set(['Lover','Lover']) 
		good_roles_in_game.remove('Lover') 
		good_roles_in_game.append(random.sample(set(available_roles),1)[0])

	if evil_roles_in_game.count('Lover') == 1: 
		available_roles = set(evil_roles)-set(evil_roles_in_game)-set(['Lover','Lover']) 
		evil_roles_in_game.remove('Lover') 
		evil_roles_in_game.append(random.sample(set(available_roles),1)[0])

	# roles after validation
	print(good_roles_in_game)
	print(evil_roles_in_game)

	# role assignment 
	random.shuffle(players)
	good_players = players[:num_good]
	evil_players = players[num_good:]

	for gp in good_players:
		gp.set_role(good_roles_in_game.pop())
		gp.set_team('Good')

	for ep in evil_players: 
		ep.set_role(evil_roles_in_game.pop())
		ep.set_team('Evil')

	for player in players:
		player.add_info(get_role_information(player,players))
		print(player.name,player.role,player.team,player.info)

	# handle mastermind here 

	# handle evil roles info here 

	# handling socialite after all other roles

	truths = []
	lies = []
	
	'''for player in players: 
		if player.type is 'Information':
			 for i in player.info:
			 	if i in player_names:
			 		truths.append([player.name,i])
			 	if i in good_roles or i in evil_roles:
			 		print(i)
			 		i_name = [player2.name for player2 in players if player2.role is i and player2.team is 'Evil'][0]
			 		truths.append([player.name,i_name])
	'''
	print(truths)


if __name__ == "__main__":
	main()