
from __future__ import unicode_literals


import youtube_dl
import argparse 
import sys
from pydub import AudioSegment


DEFAULT_DOWNLOAD_URL = 'https://www.youtube.com/watch?v=pYWrTdXl8RM'
DEFAULT_SAVE_DIRECTORY = '.'
DEFAULT_SAVE_NAME = 'audiobook.mp3'
DEFAULT_SPLIT_TIME = 30

def download(args):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '{0}/{1}'.format(args.save_directory, args.save_name),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        return ydl.download([args.url])


def splitMP3(args):
    
    filename = '{0}/{1}'.format(args.save_directory, args.save_name)
    
    sound = AudioSegment.from_mp3(filename)
    return True

    duration = args.split_time * 1000

    for i in range(0, len(sound), duration):
        # TODO make it parallel
        s = sound[i:i+duration]
        s.export_mp3('{0}-chunk{1}.mp3'.format(filename, i), format='mp3')

    return True


def get_parser(args):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--url', type=str, default=DEFAULT_DOWNLOAD_URL)
    parser.add_argument('--save_name', type=str, default=DEFAULT_SAVE_NAME)
    parser.add_argument('--save_directory', type=str, default=DEFAULT_SAVE_DIRECTORY)
    parser.add_argument('--split_time', type=int, default=DEFAULT_SPLIT_TIME)

    return parser.parse_args(args)



if __name__ == '__main__':
    args = get_parser(sys.argv[1:])
    
    d = download(args)
    if d == 0:
        s = splitMP3(args)
    else:
        print ('Cannot download specified file')
    

