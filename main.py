import pygame as pg
import os, sys, pickle, json, traceback
import xml.etree.ElementTree as ET
from tkinter import messagebox
from screeninfo import screeninfo
import logging
from datetime import datetime
from python.exceptions import NoMonitorFound
from python.userdata import DataHandler
from python.loghandle import LogHandler
from python.songhandler import ChartHandler
from python.settings import Properties
from python.filehandler import FileHandler
import python.sprites as spr
from threading import Thread
from queue import Queue
import time

# logging settings
LogHandler()


class Main:
    def moveCameraTo(self, position, t, inorout, way):
        def ease(st, position, t, outorin):
            # linear move
            pass

        def linear(position, t):
            # linear move

            if t == 0:
                return
            self.easingDistanceX = abs(Properties.camera_position[0] - position[0])
            self.easingDistanceY = abs(Properties.camera_position[1] - position[1])
            self.easingTime = t
            self.currentEasingStyle = "linear"
            self.easingTargetD = position
            self.currentlyEasing = True

        t = t
        starting_position = Properties.camera_position
        if way == "linear":
            Thread(
                target=linear,
                args=(
                    position,
                    t,
                ),
            ).start()
        elif way == "ease":
            Thread(
                target=ease,
                args=(starting_position, position, t, inorout),
            ).start()

    def loadStage(self, stage):
        stage_path = os.path.join("assets", "images", "stages", stage)
        stage_things = self.all_stages[stage]
        stage_data = FileHandler.loadJsonData(
            os.path.join(stage_path, "..", f"{stage}.json")
        )

        Properties.defaultZoom = stage_data["defaultZoom"]
        Properties.camSpeed = stage_data["camera_speed"]
        self.camera_characters_offsets = stage_data["camera_positions"]
        self._editorMeta_stage = stage_data["_editorMeta"]
        self.preload_stage = stage_data["preload"]
        self.characters_positions = stage_data["positions"]
        Properties.current_stage = []
        img_surf = ["png", "jpg", "jpeg"]
        objects_list = [prl for prl in self.preload_stage]
        for part in stage_things:
            LogHandler.printLog(f"Found path: {part}, creating it as stage part.")
            # check if it is an image or a xml for animations
            name = FileHandler.getFN(part)
            print(name)
            if name.split(".")[1] in img_surf and name.split(".")[0] in objects_list:
                getOptions = self.preload_stage[name.split(".")[0]]
                isSpriteSheet = getOptions[1]
                layer = getOptions[0]
                if isSpriteSheet:
                    pass
                else:
                    # classic surface

                    a = spr.ConstantStageSprite(
                        pg.image.load(part).convert_alpha(),
                        (10, 0),
                        Properties.game_sprites_group,
                    )
                    Properties.current_stage.append(a)
        # self.moveCameraTo(Properties.current_stage[0].position, 10, "out", "linear") this is a test, useless

    def loadImages(self):
        arrows = ["left", "up", "down", "right"]
        converted_data = {}
        actual_data = {}

        def removeNumbersFromName(name):
            t = ""
            for c in name:
                if not c.isnumeric():
                    t += c
            return t

        def loadArrows(arrow, type_):
            spritesheet = pg.image.load(
                os.path.join("assets", "images", "noteSkins", f"{type_}.png")
            ).convert_alpha()

            def retrieve_image(name, actual_data):
                for spritesl in actual_data:
                    spritesl = actual_data[spritesl]
                    for spr in spritesl:
                        if spr["name"] == name:
                            image = pg.Surface(
                                (int(spr["width"]), int(spr["height"])), pg.SRCALPHA
                            )
                            # image.set_colorkey((0, 0, 0))
                            image.blit(
                                spritesheet,
                                (0, 0),
                                (
                                    int(spr["x"]),
                                    int(spr["y"]),
                                    int(spr["width"]),
                                    int(spr["height"]),
                                ),
                            )
                            return image.convert_alpha()

            # arrows
            xml_data = ET.parse(
                os.path.join("assets", "images", "noteSkins", f"{type_}.xml")
            )
            root_data = xml_data.getroot()
            if arrow == "left":
                names = ["purple", "purple hold end", "purple piece end"]
            elif arrow == "up":
                names = ["green", "green hold end", "green piece end"]
            elif arrow == "down":
                names = ["blue", "blue hold end", "blue piece end"]
            elif arrow == "right":
                names = ["red", "red hold end", "red piece end"]

            temp = ""
            # actual_data = {}
            for obj in root_data:
                temp = removeNumbersFromName(obj.get("name"))
                if temp not in actual_data:
                    if temp in names:
                        actual_data.update({temp: []})
                # print(actual_data)
            for obj in root_data:
                if removeNumbersFromName(obj.get("name")) in names:
                    # print(obj.get("name"))

                    n = obj.get("name")
                    x = obj.get("x")
                    y = obj.get("y")
                    width = obj.get("width")
                    height = obj.get("height")
                    frameX = obj.get("frameX")
                    frameY = obj.get("frameY")
                    frameWidth = obj.get("frameWidth")
                    frameHeight = obj.get("frameHeight")
                    actual_data[removeNumbersFromName(n)].append(
                        {
                            "name": n,
                            "x": x,
                            "y": y,
                            "width": width,
                            "height": height,
                            "frameX": frameX,
                            "frameY": frameY,
                            "frameWidth": frameWidth,
                            "frameHeight": frameHeight,
                        }
                    )

            LogHandler.printLog(f"Setted up actual_data: {actual_data}")
            # self.test = {"list": ["hiya"]}
            i = 0
            for spr in actual_data:
                if spr not in converted_data:
                    converted_data.update({spr: []})

            for name in names:
                # print(name)
                for spritesl in actual_data:
                    spritesl = actual_data[spritesl]
                    for spr in spritesl:
                        # print(f"{spr}\n")
                        nn2 = removeNumbersFromName(spr["name"])
                        if nn2 == name:
                            img = retrieve_image(spr["name"], actual_data)
                            converted_data[nn2].append(img)
            Properties.all_notes_converted = converted_data

        skins = []
        for arrowskin in os.listdir(os.path.join("assets", "images", "noteSkins")):
            if arrowskin.split(".")[0] in skins:
                for arrow in arrows:
                    loadArrows(arrow, arrowskin.split(".")[0])
            skins.append(arrowskin.split(".")[0])
        # loading some other shit
        images_dir = os.path.join("assets", "images")
        self.ready_image = pg.image.load(os.path.join(images_dir, "more", "ready.png"))
        self.set_image = pg.image.load(os.path.join(images_dir, "more", "set.png"))
        self.go_image = pg.image.load(os.path.join(images_dir, "more", "go.png"))
        # loading stage things
        stages_dir = os.path.join(images_dir, "stages")
        self.all_stages = {}
        for stage in os.listdir(stages_dir):
            name = stage
            stage = os.path.join(images_dir, "stages", stage)
            if os.path.isdir(
                stage
            ):  # means for sure that this is the stage, must be a directory
                for path in os.listdir(stage):
                    if name not in self.all_stages:
                        self.all_stages.update({name: []})
                    self.all_stages[name].append(os.path.join(stage, path))

    def setupArrows(self):
        # bf
        spr.Arrow(
            self.BF_ARROW_POS, "classic", "left", False, Properties.ui_sprites_group
        )
        spr.Arrow(
            self.BF_ARROW_POS, "classic", "down", False, Properties.ui_sprites_group
        )
        spr.Arrow(
            self.BF_ARROW_POS, "classic", "up", False, Properties.ui_sprites_group
        )
        spr.Arrow(
            self.BF_ARROW_POS, "classic", "right", False, Properties.ui_sprites_group
        )
        # opponent
        spr.Arrow(
            self.OPPONENT_ARROW_POS,
            "classic",
            "left",
            True,
            Properties.ui_sprites_group,
        )
        spr.Arrow(
            self.OPPONENT_ARROW_POS,
            "classic",
            "down",
            True,
            Properties.ui_sprites_group,
        )
        spr.Arrow(
            self.OPPONENT_ARROW_POS, "classic", "up", True, Properties.ui_sprites_group
        )
        spr.Arrow(
            self.OPPONENT_ARROW_POS,
            "classic",
            "right",
            True,
            Properties.ui_sprites_group,
        )

    def loadSounds(self):
        _dir = os.path.join("assets", "sounds")
        values = {}
        for sound in os.listdir(_dir):
            path = os.path.join(_dir, sound)
            s = pg.mixer.Sound(path)
            values.update({sound.split(".")[0]: s})
            LogHandler.printLog(f"Loaded sound asset: {path}")

        return values

    def songEnd(self):
        # scores are FUNKY, S+, S, A, B, C, D, E, F
        score = ""
        if Properties.song_accuracy >= 98.0:
            score = "Funky"
        elif Properties.song_accuracy >= 96:
            if Properties.song_misses > 0:
                score = "S"
            else:
                score = "S+"
        elif Properties.song_accuracy >= 90:
            if Properties.song_misses > 0:
                score = "A"
            else:
                score = "S"
        elif Properties.song_accuracy >= 80:
            if Properties.song_misses > 0:
                score = "B"
            else:
                score = "A"
        elif Properties.song_accuracy >= 60:
            if Properties.song_misses > 0:
                score = "C"
            else:
                score = "B"
        elif Properties.song_accuracy >= 50:
            if Properties.song_misses > 0:
                score = "D"
            else:
                score = "C"
        elif Properties.song_accuracy >= 40:
            if Properties.song_misses > 0:
                score = "E"
            else:
                score = "D"
        elif Properties.song_accuracy >= 20:
            if Properties.song_misses > 0:
                score = "F"
            else:
                score = "E"
        elif Properties.song_accuracy < 20:
            score = "F"
        messagebox.showinfo("Finish", f"Final results: {score}", parent=Properties.root)
        self.running = False
        pg.quit()
        sys.exit(0)

    def checkSongTotalScore(self):
        sections = Properties.current_chart["notes"]
        Properties.song_totalScore = 0
        for section in sections:
            noteSection = section["sectionNotes"]
            for arrows in noteSection:
                actual_check = arrows[1].split("//")[1]
                actual_check = actual_check.split(".")[0]
                if actual_check == "player":
                    Properties.song_totalScore += 3000

    def fadeImage(self, sprite, timeToFade):
        timeToFade = timeToFade / 510
        i = 255
        while i != 0:
            i -= 1
            sprite.image.set_alpha(i)
            time.sleep(timeToFade)
        sprite.kill()

    def startShowSong(self):
        time.sleep(60 / Properties.current_bpm)

        # three
        Properties.allSounds["intro3"].play()
        time.sleep(60 / Properties.current_bpm)

        # two
        Properties.allSounds["intro2"].play()
        sprite = spr.ConstantSprite(
            self.ready_image,
            (self.currentResolution[0] / 2, self.currentResolution[1] / 2),
            Properties.ui_sprites_group,
        )
        self.fadeImage(sprite, 60 / Properties.current_bpm)

        # one
        Properties.allSounds["intro1"].play()
        sprite = spr.ConstantSprite(
            self.set_image,
            (self.currentResolution[0] / 2, self.currentResolution[1] / 2),
            Properties.ui_sprites_group,
        )
        self.fadeImage(sprite, 60 / Properties.current_bpm)

        # go!
        Properties.allSounds["introGo"].play()
        sprite = spr.ConstantSprite(
            self.go_image,
            (self.currentResolution[0] / 2, self.currentResolution[1] / 2),
            Properties.ui_sprites_group,
        )
        self.fadeImage(sprite, 60 / Properties.current_bpm)

    def checkSongForArrows(self):
        self.loadingSprite.image.set_alpha(0)
        self.startShowSong()
        arrow_at_the_start = False
        sections = Properties.current_chart["notes"]

        for arrows in sections[0]["sectionNotes"]:
            arrow_at_the_start = True
        if Properties.current_chart["needsVoices"]:
            if Properties.isSeperatedVoices:
                t1 = Thread(target=Properties.opponent_song_part.play)
                t2 = Thread(target=Properties.player_song_part.play)

                t1.start()
                t2.start()
            else:
                t1 = Thread(target=Properties.voices_song_part.play)
                t1.start()

        t3 = Thread(target=pg.mixer.music.play)
        t3.start()
        self.counter_start = time.perf_counter()
        Properties.fps = 60
        Properties.song_start_time = pg.time.get_ticks()
        # check if notes in first section
        if Properties.song_started:
            current_section_total_beats = 0
            sections = Properties.current_chart["notes"]
            for section in sections:
                Properties.total_song_beats += section["sectionBeats"]
            Properties.song_speed = Properties.current_chart["speed"]
            i = 0
            for section in sections:
                # print(Properties.fps)
                current_section_total_beats += section["sectionBeats"]
                try:
                    if section["changeBPM"]:
                        Properties.current_bpm = section["bpm"]
                        pg.time.set_timer(
                            self.BEAT_EVENT, int(60000 // Properties.current_bpm)
                        )

                except KeyError:
                    pass
                # print(Properties.current_bpm)
                # print(sections[i + 1]["sectionNotes"])
                try:
                    for arrows in sections[i]["sectionNotes"]:
                        args = f"{arrows[1]}.{str(arrows[0]).replace('.', ',')}.{section['sectionBeats']}"
                        self.eventHandler(args)
                        if not self.running:
                            return
                    while Properties.current_beat <= current_section_total_beats:
                        if not self.running:
                            return
                        pass
                    i += 1
                except IndexError:
                    LogHandler.printLog(
                        f"Got the indexerror in the section check, but usually it's normal in this case, more information: {traceback.format_exc()}"
                    )
            Properties.song_speed = 0
            # Properties.song_started = False
            Properties.song_start_time = 0

    def startSong(self, songname, difficulty):
        self.setupArrows()
        self.loadImages()
        Properties.all_notes = []
        Properties.song_accuracy = 100
        Properties.song_bads = 0
        Properties.song_perfects = 0
        Properties.song_decents = 0
        Properties.song_goods = 0
        Properties.song_misses = 0
        Properties.song_name = songname
        Properties.song_difficulty = difficulty
        Properties.current_chart = ChartHandler.loadChart(
            f"{songname.lower()}-{difficulty.lower()}.json"
        )["song"]
        stage = Properties.current_chart["stage"]
        # self.loadStage(stage) still not completed
        songdir = ChartHandler.getSongDirectory(songname)
        Properties.player_song_part = None
        Properties.opponent_song_part = None
        # Properties.instrumental_song_part = None
        Properties.voices_song_part = None
        Properties.isSeperatedVoices = True
        for f in os.listdir(songdir):
            if ChartHandler.canBePlayed(f):
                try:
                    if f.split(".")[0] == "Inst":
                        pg.mixer.music.load(os.path.join(songdir, f))
                    if f.split(".")[0] == "Voices":
                        Properties.isSeperatedVoices = False
                        Properties.voices_song_part = pg.mixer.Sound(
                            os.path.join(songdir, f)
                        )

                    elif f.split("-")[1].split(".")[0] == "Player":
                        if Properties.isSeperatedVoices:
                            Properties.player_song_part = pg.mixer.Sound(
                                os.path.join(songdir, f)
                            )

                    elif f.split("-")[1].split(".")[0] == "Opponent":
                        if Properties.isSeperatedVoices:
                            Properties.opponent_song_part = pg.mixer.Sound(
                                os.path.join(songdir, f)
                            )
                except IndexError:
                    pass
        # play music
        # print(Properties.current_chart)
        self.checkSongTotalScore()
        if Properties.current_chart["pyengine_version"] != 1:
            LogHandler.printWarning(
                "The version of this chart is not the same as the current version of pyengine, ignoring and continuing."
            )

        Properties.current_bpm = Properties.current_chart["bpm"]
        # i is for counting all the characters (player1, player2, player3, player4 ecc, one of them must be 'player')
        i = 1
        # in this version there can be more opponents, depends on their position in the stage
        for player in Properties.current_chart:
            if player == f"player{i}":
                char = spr.Character(
                    Properties.current_chart[player],
                )
                Properties.characters.append(char)
            i += 1
        # song loaded
        pg.time.set_timer(self.BEAT_EVENT, int(60000 // Properties.current_bpm))

        Properties.song_started = True

        pg.mixer.music.set_endevent(self.SONG_ENDED_EVENT)
        # song arrows positioning
        t = Thread(target=self.checkSongForArrows)
        t.start()

    def eventHandler(self, event):
        LogHandler.printLog(f"Got an event! >> {event}")
        if self.loading_something:
            return
        if event == "mainfnf:getScreenResolution":
            monitor_list = screeninfo.get_monitors()
            monitor = None
            LogHandler.printLog(f"Monitor list: {monitor_list}")
            for monitor in monitor_list:
                if monitor.is_primary:
                    self.currentMonitor = monitor

            if not self.currentMonitor:
                raise NoMonitorFound()
            LogHandler.printLog(f"Monitor found! >> {self.currentMonitor}")
            self.currentResolution = (
                self.currentMonitor.width,
                self.currentMonitor.height,
            )
        if event == "mainfnf:beat":
            Properties.current_beat += 1
            if self.ticking_sound:
                Properties.allSounds["Metronome_Tick"].play()
        if event.split("//")[0] == "mainfnf:callNote":
            args = event.split("//")[1]
            part = args.split(".")[0]
            character = args.split(".")[1]
            arrowtype = args.split(".")[2]
            pos = args.split(".")[3].replace(",", ".")
            pos = float(pos)
            sb = int(args.split(".")[4])
            if part == "opponent":
                height = (
                    Properties.CONSTANT_MS_TIME
                    * abs(pos - (time.perf_counter() - self.counter_start) * 1000)
                    * Properties.song_speed
                    + Properties.arrow_offset
                )
                # print(height)
                spr.ArrowToHit(
                    (
                        self.OPPONENT_ARROW_POS[arrowtype][0],
                        height,
                    ),
                    Properties.arrow_type,
                    arrowtype,
                    Properties.ui_sprites_group,
                    pos,
                    sb,
                    True,
                )
            else:
                height = (
                    Properties.CONSTANT_MS_TIME
                    * abs(pos - (time.perf_counter() - self.counter_start) * 1000)
                    * Properties.song_speed
                    + Properties.arrow_offset
                )
                # print(height)
                spr.ArrowToHit(
                    (
                        self.BF_ARROW_POS[arrowtype][0],
                        height,
                    ),
                    Properties.arrow_type,
                    arrowtype,
                    Properties.ui_sprites_group,
                    pos,
                    sb,
                    False,
                )

    def __init__(self):
        DataHandler.__check_data__()
        Properties.arrow_offset = DataHandler.getProperty("KeyOffset")
        self.loading_something = False
        # global logfile, printLog, printWarning
        self.BF_ARROW_POS = {
            "left": (1140, 100),
            "down": (1320, 100),
            "up": (1500, 100),
            "right": (1680, 100),
        }
        self.OPPONENT_ARROW_POS = {
            "left": (240, 100),
            "down": (420, 100),
            "up": (600, 100),
            "right": (780, 100),
        }
        # Variables
        self.currentEasingStyle = "Linear"
        self.easingDistanceX = 0
        self.easingDistanceY = 0
        self.easingTime = 0
        self.easingTargetD = [0, 0]
        self.currentlyEasing = False

        Properties.current_build_version = 1
        self.BEAT_EVENT = pg.USEREVENT + 1
        self.SONG_TICK_EVENT = pg.USEREVENT + 2
        self.SONG_ENDED_EVENT = pg.USEREVENT + 3
        self.running = True
        Properties.current_chart = None
        Properties.dt = 0
        Properties.current_beat = 0
        Properties.fps = 0
        Properties.arrow_type = "classic"
        Properties.Debug = DataHandler.getProperty("Debug")
        self.ticking_sound = DataHandler.getProperty("TickingSound")
        self.menu_scene = []
        self.game_scene = []
        self.sprite_arrow_queue = Queue()
        self.currentMonitor = None
        Properties.vcr_font = pg.Font(os.path.join("assets", "fonts", "vcr.ttf"))
        self.currentResolution = (0, 0)
        self.eventHandler("mainfnf:getScreenResolution")

        # sprite groups

        Properties.ui_sprites_group = pg.sprite.Group()
        Properties.game_sprites_group = pg.sprite.Group()
        Properties.ui_important_sprites = pg.sprite.Group()
        # other things
        self.loadingSprite = spr.ConstantSprite(
            pg.image.load(os.path.join("assets", "images", "more", "funkay.png")),
            (self.currentResolution[0] / 2, self.currentResolution[1] / 2),
            Properties.ui_important_sprites,
        )
        Properties.characters = []
        Properties.song_name = None
        Properties.song_difficulty = None
        Properties.song_chart = None
        Properties.song_events = None
        Properties.song_started = False
        Properties.song_speed = 1
        Properties.current_bpm = 0
        # Data Handler
        self.VSync = DataHandler.getProperty("VSync")
        self.loading_something = False
        # Fix if property is invalid!
        if self.VSync is not False or self.VSync is not True:
            DataHandler.saveProperty("VSync", True)
            self.VSync = True
        # Startup
        pg.init()
        pg.mixer.init()
        Properties.allSounds = self.loadSounds()
        self.display = pg.display.set_mode(
            self.currentResolution, pg.SCALED, vsync=self.VSync
        )
        Properties.window_size = (self.display.get_width(), self.display.get_height())
        self.render_surf = pg.Surface((1920, 1080))
        LogHandler.printLog(
            f"Got window size: {self.display.get_size()} and created render surface, now trying to set it."
        )
        pg.display.set_caption("Friday Night Funkin: PyEngine")
        pg.display.set_icon(pg.image.load("icon.ico"))
        self.clock = pg.Clock()

        self.loadingSprite.image.set_alpha(255)
        # Start game loop
        # pg.time.wait(1000)
        self.startSong("Tutorial", "Hard")
        self.run()

    def run(self):
        LogHandler.printLog("Starting main loop.")
        while self.running:
            Properties.dt = self.clock.tick() / 1000
            Properties.fps = self.clock.get_fps()

            # Pygame loop and events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    LogHandler.logfile.close()
                    if os.path.exists(LogHandler.logname):
                        os.remove(LogHandler.logname)
                    Properties.fps = 0
                    Properties.song_started = False
                    pg.time.wait(1000)
                    pg.quit()

                    sys.exit(0)
                if event.type == self.SONG_ENDED_EVENT:
                    if Properties.song_started:
                        Properties.song_started = False
                        self.songEnd()
                if event.type == self.BEAT_EVENT:
                    if Properties.song_started:
                        self.eventHandler("mainfnf:beat")
                if pg.key.get_just_pressed()[pg.K_F11]:
                    pg.display.toggle_fullscreen()
            # easing update
            if self.currentlyEasing:
                if self.currentEasingStyle == "linear":
                    if int(Properties.camera_position[0]) != int(
                        self.easingTargetD[0]
                    ) or int(Properties.camera_position[1]) != int(
                        self.easingTargetD[1]
                    ):
                        if not self.running:
                            return
                        if Properties.fps != 0:
                            moving_distancex = self.easingDistanceX * (
                                Properties.dt / self.easingTime
                            )
                            moving_distancey = self.easingDistanceY * (
                                Properties.dt / self.easingTime
                            )

                            Properties.camera_position[0] = (
                                Properties.camera_position[0] + moving_distancex
                            )
                            Properties.camera_position[1] = (
                                Properties.camera_position[1] + moving_distancey
                            )
                    else:
                        self.currentlyEasing = False
                        LogHandler.printLog(
                            f"Done doing easing in the style: {self.currentEasingStyle}"
                        )
            # update screen
            if Properties.song_started:
                Properties.song_accuracy = (
                    Properties.song_score / Properties.song_totalScore
                ) * 100
                # print(Properties.song_totalScore)
            self.textTestScore = Properties.vcr_font.render(
                f"Score: {Properties.song_score} | Misses: {Properties.song_misses} | FPS: {round(Properties.fps)} | Accuracy: {Properties.song_accuracy:.2f}%\nPerfect: {Properties.song_perfects} | Good: {Properties.song_goods} | Decent: {Properties.song_decents} | Bad: {Properties.song_bads}",
                False,
                "white",
            )
            text_rect = self.textTestScore.get_rect(
                center=(self.render_surf.get_width() // 2, 900)
            )

            self.render_surf.fill("black")
            self.render_surf.blit(self.textTestScore, text_rect)

            # print([s.image for s in self.ui_sprites_group])
            Properties.game_sprites_group.draw(self.render_surf)
            Properties.game_sprites_group.update()
            Properties.ui_important_sprites.update()
            Properties.ui_sprites_group.draw(self.render_surf)

            Properties.ui_sprites_group.update(Properties.dt)
            Properties.ui_important_sprites.draw(self.render_surf)
            Properties.ui_important_sprites.update()

            scaled = pg.transform.scale(
                self.render_surf,
                Properties.window_size,
            )
            self.display.fill("grey")
            self.display.blit(scaled, (0, 0))

            pg.display.flip()


def program():
    try:
        Main()
    except Exception:
        error = traceback.format_exc()
        LogHandler.printWarning(error)
        messagebox.showwarning("Warning Error", f"Error: {error}")
        pg.quit()
        sys.exit(1)


if __name__ == "__main__":
    program()
