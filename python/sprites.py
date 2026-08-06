import os, sys, json, pickle
import xml.etree.ElementTree as ET
from python.loghandle import LogHandler
import pygame as pg
from python.userdata import DataHandler
from python.settings import Properties


class Character(pg.sprite.Sprite):
    def __init__(self, name):
        pass


class Arrow(pg.sprite.Sprite):
    def __init__(self, pos, type_, arrow, isOppArrow, groups):
        super().__init__(groups)
        self.isOpp = isOppArrow
        self.image = pg.Surface((0, 0)).convert_alpha()
        self.rect = self.image.get_frect(center=pos[arrow])
        arrows = "assets//images//noteSkins//"
        self.spritesheet = pg.image.load(
            os.path.join(arrows, f"{type_}.png")
        ).convert_alpha()
        self.current_press_and_took = False
        self.pos = pos
        self.animation_speed = 24
        self.xml_data = ET.parse(os.path.join(arrows, f"{type_}.xml"))
        self.root_data = self.xml_data.getroot()
        self.arrow = arrow
        self.keys = DataHandler.getProperty("GameKeys")
        self.actual_data = {}
        self.frame_index = 0
        self.current_press = False
        if arrow == "left":
            self.names = ["arrowLEFT", "left confirm", "left press"]
        elif arrow == "up":
            self.names = ["arrowUP", "up confirm", "up press"]
        elif arrow == "down":
            self.names = ["arrowDOWN", "down confirm", "down press"]
        elif arrow == "right":
            self.names = ["arrowRIGHT", "right confirm", "right press"]

        temp = ""
        for obj in self.root_data:
            temp = self.removeNumbersFromName(obj.get("name"))
            if temp not in self.actual_data:
                if temp in self.names:
                    self.actual_data.update({temp: []})
        for obj in self.root_data:
            if self.removeNumbersFromName(obj.get("name")) in self.names:
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
                self.actual_data[self.removeNumbersFromName(n)].append(
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

        LogHandler.printLog(f"Setted up self.actual_data: {self.actual_data}")
        self.converted_data = {}
        # self.test = {"list": ["hiya"]}
        i = 0
        for spr in self.actual_data:
            if spr not in self.converted_data:
                self.converted_data.update({spr: []})

        for name in self.names:
            # print(name)
            for spritesl in self.actual_data:
                spritesl = self.actual_data[spritesl]
                for spr in spritesl:
                    # print(f"{spr}\n")
                    nn2 = self.removeNumbersFromName(spr["name"])
                    if nn2 == name:
                        img = self.retrieve_image(spr["name"])
                        self.converted_data[nn2].append(img)
        LogHandler.printLog(f"Setted up self.converted_data: {self.converted_data}")
        if self.isOpp:
            self.playAnimation(Properties.dt, self.names[0])

    def noteHit(self, dt):
        pass

    def removeNumbersFromName(self, name):
        t = ""
        for c in name:
            if not c.isnumeric():
                t += c
        return t

    def retrieve_image(self, name):
        for spritesl in self.actual_data:
            spritesl = self.actual_data[spritesl]
            for spr in spritesl:
                if spr["name"] == name:
                    image = pg.Surface(
                        (int(spr["width"]), int(spr["height"])), pg.SRCALPHA
                    )
                    # image.set_colorkey((0, 0, 0))
                    image.blit(
                        self.spritesheet,
                        (0, 0),
                        (
                            int(spr["x"]),
                            int(spr["y"]),
                            int(spr["width"]),
                            int(spr["height"]),
                        ),
                    )
                    return image.convert_alpha()

    def playAnimation(self, dt, n):
        frames = self.converted_data[n]
        self.frame_index += self.animation_speed * dt

        if int(self.frame_index) < len(frames):
            self.image = frames[int(self.frame_index)]
            # print(self.image)
        else:
            try:
                if self.isOpp and self.current_press_and_took:
                    self.frame_index = 0
                    self.playAnimation(dt, self.names[0])
                    self.current_press_and_took = False
            except RecursionError:
                for i in Properties.all_notes:
                    i.kill()

    def update(self, dt):
        # here inputsif
        if not self.isOpp:
            key = pg.key.key_code(self.keys[self.arrow])
            keys = pg.key.get_pressed()
            isPressed = keys[key]
            if isPressed and not self.isOpp:
                for spr in Properties.all_notes:
                    try:
                        if (
                            spr
                            and spr.arrow == self.arrow
                            and self.current_press
                            and not spr.isOpp
                        ):
                            nearest = None
                            for spr in Properties.all_notes:
                                if spr and spr.arrow == self.arrow and not spr.isOpp:
                                    if nearest is None:
                                        nearest = spr
                                    elif abs(nearest.rect.y - self.rect.y) > abs(
                                        spr.rect.y - self.rect.y
                                    ):
                                        nearest = spr
                            self.current_press = False
                            current_time = pg.time.get_ticks()
                            tth = nearest.timeToHit
                            song_pos = current_time - Properties.song_start_time
                            res = abs(tth - song_pos)
                            """ print(
                                f"{Properties.song_start_time=}, {tth=}, {song_pos=}, {res=}, {current_time=}, {Properties.all_notes=}"
                            ) """
                            # print(res)
                            """ if nearest:
                                nearest.image.set_alpha(100) """
                            if res <= 30:
                                if Properties.isSeperatedVoices:
                                    Properties.player_song_part.set_volume(1)
                                else:
                                    Properties.voices_song_part.set_volume(1)

                                self.current_press_and_took = True
                                self.playAnimation(dt, self.names[1])

                                nearest.kill()
                                Properties.all_notes.remove(nearest)
                                Properties.song_score += 3000
                                current_time = 0
                                res = 0
                                Properties.song_perfects += 1
                                break
                            elif res <= 60:
                                if Properties.isSeperatedVoices:
                                    Properties.player_song_part.set_volume(1)
                                else:
                                    Properties.voices_song_part.set_volume(1)
                                self.current_press_and_took = True

                                self.playAnimation(dt, self.names[1])
                                Properties.song_score += 2500
                                nearest.kill()
                                Properties.all_notes.remove(nearest)
                                Properties.song_goods += 1

                                current_time = 0
                                res = 0
                                break
                            elif res <= 90:
                                if Properties.isSeperatedVoices:
                                    Properties.player_song_part.set_volume(1)
                                else:
                                    Properties.voices_song_part.set_volume(1)
                                self.current_press_and_took = True

                                self.playAnimation(dt, self.names[1])
                                Properties.song_score += 2000
                                nearest.kill()
                                Properties.all_notes.remove(nearest)
                                Properties.song_decents += 1

                                current_time = 0
                                res = 0
                                break
                            elif res <= 120:
                                if Properties.isSeperatedVoices:
                                    Properties.player_song_part.set_volume(1)
                                else:
                                    Properties.voices_song_part.set_volume(1)
                                self.current_press_and_took = True
                                self.playAnimation(dt, self.names[1])
                                Properties.song_score += 1500
                                nearest.kill()
                                Properties.all_notes.remove(nearest)
                                Properties.song_bads += 1
                                current_time = 0
                                res = 0
                                break

                    except AttributeError:
                        pass
                if not self.current_press_and_took:
                    self.playAnimation(dt, self.names[2])
                else:
                    self.playAnimation(dt, self.names[1])
            else:
                if not isPressed:
                    self.current_press = True
                    self.current_press_and_took = False
                    self.frame_index = 0
                    self.image = self.converted_data[self.names[0]][0]
            self.noteHit(dt)
            self.rect = self.image.get_frect(center=self.pos[self.arrow])
        else:
            for spr in Properties.all_notes:
                if spr.isOpp and spr.arrow == self.arrow:
                    nearest = None
                    for spr in Properties.all_notes:
                        if spr and spr.arrow == self.arrow and spr.isOpp:
                            if nearest is None:
                                nearest = spr
                            elif abs(nearest.rect.y - self.rect.y) > abs(
                                spr.rect.y - self.rect.y
                            ):
                                nearest = spr

                    current_time = pg.time.get_ticks()
                    tth = nearest.timeToHit
                    song_pos = current_time - Properties.song_start_time
                    res = abs(tth - song_pos)
                    if res <= 20:
                        if Properties.isSeperatedVoices:
                            Properties.opponent_song_part.set_volume(1)
                        else:
                            Properties.voices_song_part.set_volume(1)
                        self.current_press_and_took = True
                        Properties.all_notes.remove(nearest)
                        nearest.kill()
                        self.playAnimation(dt, self.names[1])
            if self.current_press_and_took:
                self.playAnimation(dt, self.names[1])
            self.rect = self.image.get_frect(center=self.pos[self.arrow])


class ConstantSprite(pg.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)


class ConstantStageSprite(pg.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.position = pos

    def update(self):
        self.rect.centerx = self.position[0] + Properties.camera_position[0]
        self.rect.centery = self.position[1] + Properties.camera_position[1]


class ArrowToHit(pg.sprite.Sprite):
    def __init__(self, pos, type_, arrow, groups, timeToHit, sectionBeats, isOpp):
        super().__init__(groups)
        self.timeToHit = timeToHit
        # print(self.timeToHit)
        self.starty = pos[1]
        self.isOpp = isOpp
        self.image = pg.Surface((0, 0)).convert_alpha()
        # print(pos)
        self.rect = self.image.get_frect(center=pos)
        self.currentSB = sectionBeats
        arrows = "assets//images//noteSkins//"

        self.pos = pos
        self.animation_speed = 24

        self.arrow = arrow
        self.keys = DataHandler.getProperty("GameKeys")
        self.frame_index = 0

        if arrow == "left":
            self.names = ["purple", "purple hold end", "purple piece end"]
        elif arrow == "up":
            self.names = ["green", "green hold end", "green piece end"]
        elif arrow == "down":
            self.names = ["blue", "blue hold end", "blue piece end"]
        elif arrow == "right":
            self.names = ["red", "red hold end", "red piece end"]

        # print(Properties.all_notes_converted)
        self.image = Properties.all_notes_converted[self.names[0]][0]

        self.rect = self.image.get_frect(center=(pos[0], self.rect.y))
        Properties.all_notes.append(self)

    def removeNumbersFromName(self, name):
        t = ""
        for c in name:
            if not c.isnumeric():
                t += c
        return t

    def playAnimation(self, dt, n):
        frames = self.converted_data[n]
        self.frame_index += self.animation_speed * dt
        if int(self.frame_index) < len(frames):
            self.image = frames[int(self.frame_index)]
            # print(self.image)

    def update(self, dt):
        # here inputs
        try:
            scroll_speed = (
                Properties.CONSTANT_MS_TIME
                * Properties.song_speed
                * (Properties.dt * 1000)
            )
            """ print(
                f"{bps=}, {pd=}, {ppb=}, {pps=}, {Properties.current_bpm=}, {self.currentSB=}, {self.starty=}, {self.timeToHit=}, {self.rect.y}"
            ) """
            if self.rect.y <= -400:
                if not self.isOpp:
                    Properties.song_misses += 1

                if Properties.isSeperatedVoices:
                    if self.isOpp:
                        Properties.opponent_song_part.set_volume(0)
                    else:
                        Properties.player_song_part.set_volume(0)
                else:
                    Properties.voices_song_part.set_volume(0)
                self.kill()
            self.rect.y -= scroll_speed
        except:
            pass
