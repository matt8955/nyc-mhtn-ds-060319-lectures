import csv
from collections import OrderedDict, Counter
import matplotlib.pyplot as plt
import json

def parse_csv(filename):
    with open(filename) as f:
        # we are using DictReader because we want our information to be in dictionary format.
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            curr = OrderedDict()
            for k, v in row.items():
                curr.update({k:v})
            data.append(curr)
        return data

def parse_txt(filename):
    with open(filename, 'r') as textfile:
        lines = textfile.readlines()
        lines = list(map(lambda line: line.strip().split('\t'), lines))
        songs = []
        categories = ['rank', 'name', 'artist', 'year']
        for line in lines:
            parsed = dict(zip(categories, line))
            songs.append(parsed)
        return songs

albums = parse_csv('Data.csv')
songs = parse_txt('top-500-songs.txt')

# album = find_by_name(song['name'], 'albums')
# this is SONG {'rank': '1', 'name': 'Like a Rolling Stone', 'artist': 'Bob Dylan', 'year': '1965'}
# None

def find_by_name(data, dataset):
    key = None
    if dataset == 'songs':
        dataset = songs
        key = 'name'
    elif dataset == 'albums':
        dataset = albums
        key = 'album'
    for curr_dict in dataset:
        curr = curr_dict[key]
        if curr == data:
            return ({key: curr})

def find_by_rank(data, dataset):
    if dataset == 'songs':
        dataset = songs
        key = 'rank'
        key_2 = 'name'
    elif dataset == 'albums':
        dataset = albums
        key = 'number'
        key_2 = 'album'
    for curr_dict in dataset:
        curr = int(curr_dict[key])
        if data == curr:
            return {key_2: curr_dict[key_2], key:data}
    return None

def find_by_year(year, dataset):
    data = []
    if dataset == 'songs':
        dataset = songs
        key = 'name'
    elif dataset == 'albums':
        dataset = 'albums'
        key = 'album'
    for curr_dict in dataset:
        curr_yearyear = curr_dict['year']
        if year == curr_year:
            data.append(curr_dict['year'])
    return data

def find_by_years(start_year, end_year, dataset):
    data = []
    if dataset == 'songs':
        dataset = songs
        key = 'name'
    elif dataset == 'albums':
        dataset = albums
        key = 'album'
    years = list(range( int(start_year), int(end_year)+1 ))
    for curr_dict in dataset:
        year = int(curr_dict['year'])
        if year in years:
            data.append(curr_dict[key])
    return data

def find_by_ranks(start_rank, end_rank, dataset):
    data = []
    if dataset == 'songs':
        dataset = songs
        key = 'rank'
        key_2 = 'name'
    elif dataset == 'albums':
        dataset = albums
        key = 'number'
        key_2 = 'album'
    ranks = list( range ( int(start_rank), int(end_rank)+1 ))
    for curr_dict in data:
        number = int(curr_dict[key])
        if number in ranks:
            data.append(curr_dict[key2])
    return data

def all_titles(dataset):
    if dataset == 'songs':
        dataset = songs
        key = 'name'
    elif dataset == 'albums':
        dataset = albums
        key = 'album'
    titles = [curr_dict[key] for curr_dict in dataset]
    return titles

def all_artists(dataset):
    if dataset == 'songs':
        dataset = songs
        key = 'name'
    elif dataset == 'albums':
        dataset = albums
        key = 'album'
    artists = [curr_dict['artist'] for curr_dict in dataset]
    return artists

def most_albums(data, dataset):
    counts = dict()
    if dataset == 'songs':
        dataset = songs
        key = 'name'
    elif dataset == 'albums':
        dataset = albums
        key = 'album'
    for curr_dict in dataset:
        curr = curr_dict[key]
        counts[artist] = counts.get(curr, 0) + 1
    return max(counts, key=lambda artist: counts[curr])

def most_popular_word(data, dataset):
    if dataset == 'songs':
        dataset = songs
        key = 'name'
    elif dataset == 'albums':
        dataset = albums
        key = 'album'
    word_counts = dict()
    for curr_dict in dataset:
        words = curr_dict[key].split()
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
    return max(word_counts, key=lambda word: word_counts[word])

def hist_by_decade(data):
    decade_counts = dict()
    for curr_dict in data:
        decade = int(curr_dict['year'][:3] + "0")
        decade_counts[decade] = decade_counts.get(decade, 0) + 1
    xs = decade_counts.keys()
    ys = decade_counts.values()
    plt.bar(xs, ys, width = 5)
    plt.show()
    return None

def hist_by_genre(data):
    genre_counts = dict()
    for curr_dict in data:
        genre = curr_dict['genre']
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    xs = genre_counts.keys()
    ys = genre_counts.values()
    plt.bar(xs, ys)
    plt.xticks(rotation=90)
    plt.show()
    return None

file = open('track_data.json', 'r')
json_data = json.load(file)

def album_most_top_songs():
    most = [0, None, None]
    for album in json_data:
        count = 0
        songs_in_album = album['tracks']
        for song in songs_in_album:
            if find_by_name(song, 'songs'):
                count += 1
        if count >= most[0]:
            most = [count, album['album'], album['artist']]
    return most


def album_with_top_songs():
    albs = []
    for album in json_data:
        top_song = False
        songs_in_album = album['tracks']
        for song in songs_in_album:
            if find_by_name(song, 'songs'):
                top_song = True
        if top_song:
            albs.append(album['album'])
    return albs

def songsThatAreOnTopAlbums():
    top_albums = [album['tracks'] for album in json_data]
    top_songs = []
    for album in top_albums:
        top_songs.extend(album)
    return top_songs

def top10AlbumsByTopSongs():
    albs_with_top_songs = album_with_top_songs() # all albums that contain top songs
    cnter = Counter()
    for song in songs:
        album = find_by_name(song['name'], 'songs')
        album = album['name']
        cnter[album] += 1
    cnter = dict(cnter.most_common()[:10])
    xs = cnter.keys()
    ys = cnter.values()
    plt.bar(xs, ys)
    plt.title('Top 10 albums by top songs')
    plt.xlabel('Album')
    plt.ylabel('Number of top 500 songs')
    plt.xticks(rotation=90)
    plt.show()


def topOverallArtist():
    cnt = Counter()
    top_albums = all_artists('albums')
    top_songs = all_artists('songs')
    for album in top_albums:
        cnt[album] +=1
    for song in top_songs:
        cnt[song] += 1
    return cnt.most_common()[:10]


