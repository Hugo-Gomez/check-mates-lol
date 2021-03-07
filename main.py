import PySimpleGUI as sg
import webbrowser
import json

# TODO : tests and error handling
# TODO : add more languages
# TODO : add more search engines
# TODO : clean-up and comment

# TEST VARIABLES
FR_TEST_message = 'JakubMichalak a rejoint le salon\nLubiar a rejoint le salon\nÉ T a rejoint le salon\nTorethiel a ' \
               'rejoint le salon\nCasual Dada a rejoint le salon'

# CONSTANTS
REGIONS = ['EUNE', 'JP', 'LAN', 'NA', 'RU', 'BR', 'EUW', 'KR', 'LAS', 'OCE', 'TR']
LANGUAGES = ['FR', 'EN']
SEARCH_ENGINES = {
    'LeagueOfGraphs': 'https://www.leagueofgraphs.com/summoner/CML-REGION/CML-USERNAME',
    'op.gg': 'https://CML-REGION.op.gg/summoner/userName=CML-USERNAME'
}
LOBBY_LANGUAGE_MESSAGE = {
    'FR': ' a rejoint le salon',
    'EN': ' joined the lobby'
}


def generate_layout(store_dict):
    # PYSIMPLEGUI LAYOUT
    layout = [[sg.Text('Username'), sg.InputText(size=(20, 1), key='username', default_text=store_dict['username'])],
              [sg.Text('Region'), sg.InputOptionMenu(REGIONS, size=(7, 1), key='region', default_value=store_dict['region']),
               sg.Text('Client language'),
               sg.InputOptionMenu(LANGUAGES, size=(5, 1), key='language', default_value=store_dict['language']),
               sg.Text('Website'),
               sg.InputOptionMenu([*SEARCH_ENGINES.keys()], size=(20, 1), key='engine', default_value=store_dict['engine'])],
              [sg.Text('Lobby arrival message'),
               sg.Multiline(size=(50, 5), key='message', default_text=FR_TEST_message),
               sg.OK('Clear', key='clear')],
              [sg.OK('Check Mates', key='search'), sg.OK('Clear All', button_color=('white', 'red'), key='clear_all')]]
    return layout


def get_mates(message, username, language):
    players = message.replace('\n', '').replace(LOBBY_LANGUAGE_MESSAGE[language], '|').split('|')
    return [x for x in players if (len(x) > 0 and not x == username)]


def open_search_tab(username, region, engine):
    url = SEARCH_ENGINES[engine].replace('CML-USERNAME', username).replace('CML-REGION', region.lower())
    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    with open('storage.json', 'r') as storage_file:
        storage = json.loads(storage_file.read())
    window = sg.Window('Check Mates LoL', generate_layout(storage))
    while True:
        event, values = window.read()
        # Search mates
        if event == 'search':
            mates = get_mates(values['message'], values['username'], values['language'])
            for mate in mates:
                open_search_tab(mate, values['region'], values['engine'])
        # Clear every field
        if event == 'clear_all':
            for key in values.keys():
                window[key]('')
        # Clear lobby message
        if event == 'clear':
            window['message']('')
        if event == sg.WIN_CLOSED:
            break
        # Save infos
        with open('storage.json', 'w') as storage_file:
            json.dump(values, storage_file)
    window.close()
