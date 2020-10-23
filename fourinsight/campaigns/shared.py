from enum import Enum


class Channels(Enum):
    A = ['Ax', 'Ay', 'Az']
    G = ['Gx', 'Gy', 'Gz']
    AG = ['Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz']
    PR = ['Pitch', 'Roll']
    PULSE_AG = ['Ax', 'Ay', 'Az', 'Gx', 'Gy']
