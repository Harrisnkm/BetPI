from django.shortcuts import render
import requests
import json
from datetime import datetime
import pygal
from django.conf import settings

'''
General Functions
'''

'''Formats date string'''''
def formatCommenceTime(game):
    game['commence_time_formatted'] = datetime.fromtimestamp(game['commence_time'])

'''Loads JSON file from API or File'''
def loadJson(mode):

    if mode == 'file':
        #open json file
        odds = json.load(open('dashboard/json/odds.json'))

    else:
        #Set Parameters
        api_key = settings.BET_API_KEY
        sport_key = 'americanfootball_nfl'
        region_key = 'us'
        mkt_key = 'h2h'


        #JSON Request
        odds = requests.get('https://api.the-odds-api.com/v3/odds/', params={
            'api_key': api_key,
            'sport': sport_key,
            'region': region_key,
            'mkt': mkt_key
        })


    return odds.json()['data'] if mode == 'api' else odds['data']



'''
Dashboard Functions
'''

'''Root view for Dashboard'''
def dashboard(request):
    games = loadJson('api')

    games = findOdds(games)
    context = {'sports': games}
    return render(request, 'dashboard.html', context)


'''Adds an away team index in each game list'''
def addAwayTeam(game, reverse):
    #if hometeam does not equal teams[0] return teams .2
        game['away_team'] = game['teams'][0] if reverse else game['teams'][1]




#find odds
def findOdds(games):

    '''
    loop through each game
        loop through each book site

    initialize variables to none:
        home_odds = game.sites[0]
        away_odds = game.sites[0]
        home_max_value = home_odds.odds.h2h[0]
        away_max_value = game.sites[0].odds.h2h[1]

        forloop for each site
            check if the new value[0] is greater than the home_max_value
                set home_odds to current
            check if the new value[1] is greater than the away max value
                set away_odds to current

        add home_odds to game
        add away_odds to game

    '''

    for game in games:
        reverse = False
        #set reverse flag?
        #check if the home_team is not teams[0]
        if game['home_team'] != game['teams'][0]:
            reverse = True



        best_team1_odds = game['sites'][0]
        best_team2_odds = game['sites'][0]

        team1_value_max = best_team1_odds['odds']['h2h'][0]
        team2_value_max = best_team2_odds['odds']['h2h'][1]

        addAwayTeam(game, reverse)
        formatCommenceTime(game)

        for index, book in enumerate(game['sites']):

                if book['odds']['h2h'][0] > team1_value_max:
                    best_team1_odds = game['sites'][index]
                    team1_value_max = book['odds']['h2h'][0]

                if book['odds']['h2h'][1] > team2_value_max:
                    best_team2_odds = game['sites'][index]
                    team2_value_max = book['odds']['h2h'][1]

        #add items to the dictionary
        game['best_home_odds'] = best_team2_odds if not reverse else best_team1_odds
        game['best_away_odds'] = best_team2_odds if reverse else best_team1_odds


    return games

'''
Margins Functions
'''

'''Root view for margins'''
def margins(request):
    games = loadJson('api')
    createMarginsGraph(games)
    return render(request, 'margins.html', {})

'''Create the PyGal graph using games data'''
def createMarginsGraph(games):
    '''
    Creates graph to show greatest discrepancies between games
    :param games: data on the games
    :return: no return
    '''

    odds_differences = []
    new_odds = []

    bar_chart = pygal.Bar()  # Then create a bar graph object
    bar_chart.title = 'Difference in Values by Games'
    bar_chart.x_labels = [f"{game['teams'][0]} v. {game['teams'][1]}" for game in games]
    #loop through the first site and get all the site_nice and put it into a array
    all_sites = [site['site_nice'] for site in games[0]['sites']]
    #loop through site in each game and get the the difference between the 2 values


    #create list of odds for each game
    for i in range(len(bar_chart.x_labels)):
        odds_differences.append([round(max(site['odds']['h2h']) - min(site['odds']['h2h']),2) for site in games[i]['sites']])



    for vslice in zip(*odds_differences):
        new_odds.append(vslice)

    print(len(odds_differences))
    print(len(new_odds))
    print(len(all_sites))



    #loop through each list an
    for i in range(len(new_odds)):
        bar_chart.add(all_sites[i], new_odds[i])
        bar_chart.render_to_file('dashboard/static/bar_chart.svg')  # Save the svg to a file



'''
Resources Functions
'''

def resources(request):

    return render(request, 'resources.html')


