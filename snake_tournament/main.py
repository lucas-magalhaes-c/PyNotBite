import numpy as np

class Snake:

    def __init__(self, color):
        self.color = color
        self.animal_class = "Reptilia"
        self.base_damage = 4
        self.bites = {
            "min": 0,
            "max": 3
        }
        self.life = 100

    def attack(self,snake):
        if isinstance(snake,Snake): # checks if the snake parameter is of type Snake
            number_of_bites = self.number_of_bites()
            total_damage = self.base_damage * number_of_bites

            snake.take_damage(total_damage)
            
            return total_damage, snake
        else:
            print("Failed. You can only attack a snake object")
            return None, snake
    
    
    def number_of_bites(self):
        return np.random.randint(self.bites["min"], self.bites["max"] + 1)
    
    def take_damage(self,total_damage):
        self.life = self.life - total_damage

        if self.life < 0:
            self.life = 0


class Battle:
    def __init__(self, players):

        if len(players) != 2:
            print("The number of players must be 2!")
            exit()

        self.players = players
        self.battle_round = 0
        self.winner = None
        self.logs = []

    def run(self):

        coin_flip = lambda : np.random.randint(0,2) # rand 0 or 1

        while self.players[0].life > 0 and self.players[1].life > 0:
            self.battle_round += 1

            # flip coin. if 0 the players[0] attacks first and 1 the players[1]
            attacking = coin_flip()
            defending = 0 if attacking == 1 else 1

            # the attacking snake performs the attack
            total_damage, self.players[defending] = self.players[attacking].attack(self.players[defending])
            
            self.logs.append("> {} snake attacked the {} snake (remaining life {}). Total damage: {}"
                .format(self.players[attacking].color, self.players[defending].color, 
                self.players[defending].life, total_damage))

            # if the defending snake survives, it attacks
            if self.players[defending].life > 0:
                total_damage, self.players[attacking] = self.players[defending].attack(self.players[attacking])
                
                self.logs.append("> {} snake attacked the {} snake (remaining life {}). Total damage: {}"
                    .format(self.players[defending].color, self.players[attacking].color, 
                    self.players[attacking].life, total_damage))

        self.winner = 0 if self.players[0].life > 0 else 1

    def show_result(self):
        if self.winner != None:
            print("{} wins! Remaining life: {}. Total rounds: {}"
                .format(self.players[self.winner].color, self.players[self.winner].life, self.battle_round))
        else:
            print("Battle not started")
    
    def show_logs(self):
        for log in self.logs:
            print(log)

class Tournament:
    def __init__(self, players):
        self.valid_number_of_players = [2,4,8,16]
        self.classified_players = []
        self.tournament_winner = None
        self.battle_count = 0
        self.tournament_logs = []

        if len(players) not in self.valid_number_of_players:
            print("The number of players must be 2, 4, 8 or 16!")
            exit()
        
        self.players = players
    
    def run(self):
        snakes_color_list = lambda snakes_list : list(map(lambda x: x.color + " snake",snakes_list))

        print("Starting players:", snakes_color_list(self.players))
        self.classified_players = self.players

        while len(self.classified_players) != 1:
            players_to_battle = self.classified_players 
            self.classified_players = []

            players = []
            for player in players_to_battle:
                players.append(player)

                if len(players) == 2:
                    self.battle_count += 1
                    battle = Battle(players)
                    battle.run()

                    self.classified_players.append(players[battle.winner])
                    self.tournament_logs.append("Battle {}: {} snake vs. {} snake. Winner: {}"
                        .format(self.battle_count,players[0].color,players[1].color,players[battle.winner].color))
                    players = []
            
            print("Classified players:", snakes_color_list(self.classified_players))
        
        print("The winner is the {} snake".format(self.classified_players[0].color))
                

    def show_logs(self):
        for log in self.tournament_logs:
            print(log)


players = [Snake("Purple"),Snake("Blue"),Snake("Green"),Snake("Yellow"),
            Snake("Brown"),Snake("Orange"),Snake("Gray"),Snake("White")]

tournament = Tournament(players)
tournament.run()
tournament.show_logs()