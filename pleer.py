import sys
import requests
import json
import argparse
import os
import wget

# Console colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", help="search field")
    parser.add_argument("-d", "--download", type=int, help="download the track.", nargs='+')
    parser.add_argument("-q", "--quality", help="quality wanted for the search")
    parser.add_argument("-H", "--history", help="Show the last downloaded tracks.", action="store_true")
    parser.add_argument("-r", "--result", type=int, help="Number of results displayed.")

    return parser.parse_args()


def getToken(userId, appToken):
    auth = userId, appToken
    postData = {'grant_type': 'client_credentials'}

    r = s.post('http://api.pleer.com/token.php', auth = auth, data = postData)
    return(r.json()['access_token'])


def initJsonFile(homedir):
    print('['+G+'+'+W+'] No .pleer_config file found, initializing it.')
    userId= input('UserID: ')
    appToken = input('Application Token: ')
    token = getToken(userId, appToken)

    config = {
        'userId': userId,
        'appToken': appToken,
        'token': token,
        'nb_results' : 20,
        'download_history': [],
        'search_history': {},
        'quality': 'all'
    }

    fHistory = open(homedir+'/.pleer_config', 'w+')
    json.dump(config,fHistory)
    fHistory.close()


def get_config(homedir):
    if not os.path.exists(homedir+'/.pleer_config'):
        initJsonFile()

    fConfig = open(homedir+'/.pleer_config', 'r+')
    config = json.load(fConfig)
    return config


def parse_result(results):
    lastSearch = []
    for result in results:
        music = results[result]
        lastSearch.append(music['id'])
        print('['+G+str(len(lastSearch))+W+'] '
            +music['track']
            +'('+C+music['artist']+W+') '
            +parse_bitrate(music['bitrate']))
    return lastSearch


def parse_bitrate(bitrate):
    if bitrate == "VBR":
        return B+'VBR'+W
    else:
        bitrate = int(bitrate)
        if bitrate >= 320:
            return G+'High'+W
        elif bitrate >= 192:
            return O+'Medium'+W
        else:
            return R+'Low'+W


def search_track(args, token, quality, nb_results):
    rSearch = s.post('http://api.pleer.com/index.php',
        data = {'access_token':token,
        'method':'tracks_search',
        'query': args.search,
        'page': 1,
        'quality': quality,
        'result_on_page': nb_results})

    lastSearch = []
    if rSearch.status_code == 200:
        lastSearch = parse_result(rSearch.json()['tracks'])
    elif rSearch.status_code == 401:
        if rSearch.json()['error'] == "invalid_token":
            config['token'] = getToken(config['userId'], config['appToken'])
            search_track(args, config['token'], quality, nb_results)
    else:
        print(rSearch.text)
    return lastSearch


def download_track(track_id, token):
    rDownload = s.post('http://api.pleer.com/index.php',
        data = {'access_token':token,
        'method':'tracks_get_download_link',
        'track_id': track_id,
        'reason': 'save'})


    mp3name = ""
    if rDownload.status_code == 200:
        url = rDownload.json()["url"]
        mp3name = wget.download(url)
        print('\n['+G+'Completed'+W+'] '+mp3name+W)
    elif rDownload.status_code == 401:
        if rDownload.json()['error'] == "invalid_token":
            config['token'] = getToken(config['userId'], config['appToken'])
            download_track(track_id, config['token'],)
    else:
        print('['+R+'Error'+W+']')
        print(rSearch.text)
    return mp3name


if __name__ == "__main__":
    s = requests.Session()
    homedir = os.path.expanduser('~')
    config = get_config(homedir)
    args = parse_args()

    token = config['token']

    if args.search:
        if args.quality in ['all','bad','good','best']:
            config['quality'] = args.quality

        if args.result and int(args.result) <= 100:
            config['nb_results'] = args.result

        lastSearch = search_track(args, token, config['quality'], config['nb_results'])
        if len(lastSearch) > 0:
            config['search_history'] = lastSearch

        fHistory = open(homedir+'/.pleer_config', 'w+')
        json.dump(config,fHistory)
        fHistory.close()

    elif args.download:
        for track in args.download:
            if track>=config['nb_results'] or track<=0:
                print('['+R+'Error'+W+'] Unexpected index. (index given:'+str(track)+')')
                continue
            lastDownload=download_track(config['search_history'][track-1], token)
            if len(lastDownload)>0:
                if len(config['download_history']) >= 20:
                    config['download_history'].pop(0)
                config['download_history'].append(lastDownload)

        fHistory = open(homedir+'/.pleer_config', 'w+')
        json.dump(config, fHistory)
        fHistory.close()

    if args.history:
        print('Last downloads '+GR+'(lastest first):\n')
        for track in config['download_history']:
            print('['+G+'+'+W+'] '+track)

    sys.exit(0)