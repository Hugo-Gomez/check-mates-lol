import PySimpleGUI as sg
import webbrowser

# TODO : save infos
# TODO : add more languages
# TODO : add more search engines
# TODO : clean, fragment in multiple files and comment

# TEST VARIABLES
FR_TEST_message = 'JakubMichalak a rejoint le salon\nLubiar a rejoint le salon\nÉ T a rejoint le salon\nTorethiel a ' \
               'rejoint le salon\nCasual Dada a rejoint le salon'

# CONSTANTS
regions = ['EUNE', 'JP', 'LAN', 'NA', 'RU', 'BR', 'EUW', 'KR', 'LAS', 'OCE', 'TR']
languages = ['FR', 'EN']
search_engines = {
    'LeagueOfGraphs': 'https://www.leagueofgraphs.com/summoner/CML-REGION/CML-USERNAME',
    'op.gg': 'https://CML-REGION.op.gg/summoner/userName=CML-USERNAME'
}
lobby_language_message = {
    'FR': ' a rejoint le salon',
    'EN': ' joined the lobby'
}


# PYSIMPLEGUI LAYOUT
layout = [[sg.Text('Username'), sg.InputText(size=(20, 1), key='username', default_text='Lubiar')],
          [sg.Text('Region'), sg.InputOptionMenu(regions, size=(7, 1), key='region', default_value='EUW'),
           sg.Text('Client language'), sg.InputOptionMenu(languages, size=(5, 1), key='language', default_value='FR'),
           sg.Text('Website'), sg.InputOptionMenu([*search_engines.keys()], size=(20, 1), key='engine', default_value='LeagueOfGraphs')],
          [sg.Checkbox('Save infos', size=(10, 1), key='save')],
          [sg.Text('Lobby arrival message'), sg.Multiline(size=(50, 5), key='message', default_text=FR_TEST_message)],
          [sg.OK('Check Mates', key='search')]]


def get_mates(message, username, language):
    players = message.replace('\n', '').replace(lobby_language_message[language], '|').split('|')
    return [x for x in players if (len(x) > 0 and not x == username)]


def open_search_tab(username, region, engine):
    url = search_engines[engine].replace('CML-USERNAME', username).replace('CML-REGION', region.lower())
    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    window = sg.Window('Check Mates LoL', layout)
    while True:
        event, values = window.read()
        if event == 'search':
            print(values)
            mates = get_mates(values['message'], values['username'], values['language'])
            for mate in mates:
                open_search_tab(mate, values['region'], values['engine'])
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
    window.close()
