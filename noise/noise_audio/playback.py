import pygame as pg


def play_music(music_file, volume=0.8):
    """
    Play back audio clip to user.
    """
    freq = 44100
    bitsize = -16
    channels = 2
    buffer = 2048
    pg.mixer.init(freq, bitsize, channels, buffer)
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music_file)
        print("Music file {} loaded!".format(music_file))
    except pg.error:
        print("File {} not found! ({})".format(music_file, pg.get_error()))
    return
    pg.mixer.music.play()
    while pg.mixer.music.get_busy():
        clock.tick(30)
