### Configuration for autofishV3.py ###

from PIL import ImageGrab, ImageOps, ImageChops
import pyautogui
import win32api
import win32gui
import time
from numpy import array
import numpy as np
import random
import cv2
import os
import winsound
import keyboard
import pytesseract


# INITIAL SETTINGS  
RADAR_ALERT = True                  # Use radar alert for nearby players (False if tournament)
DETAILED_REPORT = False              # Detailed report includes time took to catch the fish, tugging, etc
# COMPACT_LOG = True     


# CONSTANTS
CPS = 5
CPS_CONSECUTIVE = 5                  # CPS for consecutive click types
CHANCE_INITIAL_FAIL = 3
CHANCE_HUMAN_ERROR = 3


# File Names & Paths
IMAGE_PATH = ".\\images\\"
IMAGE_FISH = "fish.png"
IMAGE_BOBBER = "bobber.png"
IMAGE_ROD = "rod.png"
IMAGE_MAP = "map.png"
IMAGE_SUB_BOBBER = "sub_bobber.png"
IMAGE_SUB_FISH = "sub_fish.png"
IMAGE_ROD_BEFORE = "rod_before.png"


# Keyboard Bindings
KEY_ROD = '1'
KEY_AQUARIUM = '2'                      # Storage 1
KEY_ICEBOX = '3'                        # Storage 2
KEY_BUCKET = '4'                        # Storage 3
KEY_HUGE = '5'     


# Screen Regions
SR_ROD = (1310, 534, 1651, 1027)        # Fishing Rod While Handheld 
SR_LAST_1 = (1084, 516, 1124, 557)      # Last slot of storage 1
SR_LAST_2 = (1045, 476, 1092, 525)      # Last slot of storage 2
SR_LAST_3 = (1083, 443, 1125, 486)      # Last slot of storage 3
SR_INVENTORY = (793, 577, 1126, 691)    # 9 x 3 Inventory 
SR_MAP = (1665, 67, 1865, 277)
SR_SUBTITLES = (1553, 677, 1920, 1025)
SR_ROD_INVENTORY = (797, 993, 818, 1026)


# Position Coordinates
POS_NEUTRAL = (31, 44)                  # To move the cursor out of the way
POS_TUG_BAR_X = 950                     # Tugging Bar
POS_TUG_BAR_Y = 551                     # Tugging Bar
POS_TUG_MINIGAME_X = 1192               # Minigame (Left or Right)
POS_TUG_MINIGAME_Y = 459                # Minigame (Left or Right)
POS_ROD_INVENTORY_X = 805                 # Inventory Rod (Slot 1) - The white part on its bait/bobber
POS_ROD_INVENTORY_Y = 1024