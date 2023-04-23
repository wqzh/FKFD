
from Environment.const import AIRCRAFT_X, AIRCRAFT_Y,DESTROYER_DIST
pi2 = 3.14 / 2

aircraft_x, aircraft_y = AIRCRAFT_X, AIRCRAFT_Y
dis = DESTROYER_DIST

red_aircraft = [
    {'x' : aircraft_x, 'y' : aircraft_y, 'speed' : 10, 'missles' : 20, 'name' : 'a1'},
]

red_destroyer = [
    {'x' : AIRCRAFT_X+DESTROYER_DIST, 'y' : AIRCRAFT_X-DESTROYER_DIST, 'speed' : 5, 'radar' : 0, 'incr' : 0.04,
     'missles' : 10, 'idx': 1, 'name' : 'd1', 'fpu': ['far', 'mid', 'near']},
    {'x' : AIRCRAFT_X-DESTROYER_DIST, 'y' : AIRCRAFT_X-DESTROYER_DIST, 'speed' : 5, 'radar' : 0, 'incr' : 0.05,
     'missles' : 10, 'idx': 2, 'name' : 'd2', 'fpu': ['far', 'mid', 'near']},
    {'x' : AIRCRAFT_X-DESTROYER_DIST, 'y' : AIRCRAFT_X+DESTROYER_DIST, 'speed' : 5, 'radar' : 0, 'incr' : 0.06,
     'missles' : 10, 'idx': 3, 'name' : 'd3', 'fpu': ['far', 'mid', 'near']},
    {'x' : AIRCRAFT_X+DESTROYER_DIST, 'y' : AIRCRAFT_X+DESTROYER_DIST, 'speed' : 5, 'radar' : 0, 'incr' : 0.07,
     'missles' : 10, 'idx': 4, 'name' : 'd4', 'fpu': ['far', 'mid', 'near']},
]


red_frigate = [
    #{'x' : 230, 'y' : 250, 'speed' : 5, 'missles' : 10, 'name' : 'f1'},
]

red_missile = [
    #{'x' : 220, 'y' : 340, 'tarx' : 400, 'tary' : 400, 'speed' : 20, 'type' : 'Unknow', 'name' : 'rm1'},
]


blue_missile = [
    ####{'x' : 400, 'y' : 240, 'tarx' : aircraft_x, 'tary' : aircraft_y, 'speed' : 20, 'type' : 'Unknow', 'name' : 'm1'},
    #{'x' : 400, 'y' : 150, 'tarx' : aircraft_x, 'tary' : aircraft_y, 'speed' : 20, 'type' : 'Unknow', 'name' : 'm2'},
    ####{'x' : 240, 'y' : 150, 'tarx' : aircraft_x, 'tary' : aircraft_y, 'speed' : 20, 'type' : 'Unknow', 'name' : 'm3'},
    #{'x' : 100, 'y' : 100, 'tarx' : aircraft_x, 'tary' : aircraft_y, 'speed' : 20, 'type' : 'Unknow', 'name' : 'm4'},
    ####{'x' : 100, 'y' : 240, 'tarx' : aircraft_x, 'tary' : aircraft_y, 'speed' : 20, 'type' : 'Unknow', 'name' : 'm5'},
    #{'x' : 80, 'y' : 350, 'tarx' : aircraft_x, 'tary' : aircraft_y, 'speed' : 20, 'type' : 'Unknow', 'name' : 'm6'},
    ####{'x' : 240, 'y' : 400, 'tarx' : aircraft_x, 'tary' : aircraft_y, 'speed' : 20, 'type' : 'Unknow', 'name' : 'm7'},
    #{'x' : 450, 'y' : 430, 'tarx' : aircraft_x, 'tary' : aircraft_y, 'speed' : 20, 'type' : 'Unknow', 'name' : 'm8'},
]

