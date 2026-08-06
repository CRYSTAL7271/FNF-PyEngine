import os, sys, pickle, json, pygame
import tkinter as tk


class Properties:
    pygame.font.init()
    song_name = ""
    current_chart = {}
    current_bpm = 0
    characters = []
    current_build_version = 1
    fps = 0
    song_difficulty = ""
    current_beat = 0
    dt = 0
    song_speed = 0
    song_started = False
    song_events = None
    ui_sprites_group = None
    game_sprites_group = None
    allSounds = None
    total_song_beats = 0
    arrow_type = "classic"
    tick_song_current = 0
    all_notes = []
    song_score = 0
    vcr_font = pygame.Font(os.path.join("assets", "fonts", "vcr.ttf"))
    window_size = (0, 0)
    song_start_time = 0
    CONSTANT_MS_TIME = 0.45
    Debug = False
    all_notes_converted = None
    arrow_offset = 70
    song_misses = 0
    song_accuracy = 0
    song_totalScore = 0
    song_perfects = 0
    song_goods = 0
    song_decents = 0
    song_bads = 0
    voices_song_part = None
    # instrumental_song_part = None
    player_song_part = None
    opponent_song_part = None
    isSeperatedVoices = False
    ui_important_sprites = None
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    root.attributes("-topmost", True)  # Force focus above other windows
    defaultZoom = 1
    camSpeed = 1
    current_stage = None
    camera_position = [0, 0]
