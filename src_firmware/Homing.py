
# !/usr/bin/python3

from __future__ import print_function
import odrive
from odrive.enums import *
# from odrive.utils import start_liveplotter
import time
import math

## Inicializar odrives, ver estados de axis y encoders

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#my_drive = odrive.find_any("serial:/dev/ttyUSB0")

def def_mot(ID, nombre, home, vel, LS_steps):
    '''ID = ID odrv
    axis_i = axis asociado al motor que se quiere inicializar
    nombre = nombre de la articulacion
    home = 1, realizar secuancia de homing'''
    print("Buscando Odrive asociado a: " + str(nombre))
    odrv_i = odrive.find_any(ID)
    print(str(nombre) + " axis errors:")
    if nombre == hombro or nombre == z:
        mot_i = odrv_i.axis0
    if nombre == codo:
        mot_i = odrv_i.axis1
    print(str(nombre) + " axis encoder errors:")
    encdr_i = mot_i.encoder
    print("motor is calibrated = " + str(mot_i.motor.is_calibrated))
    if home == 1:
        #Aqui puede incluirse el offset para no volver a calibrar
        if mot_i.motor.is_calibrated == 0 and mot_i.encoder.is_read == 0:
            mot_i.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
            print("waiting for encoder offset calibration to end..")
            while mot_i.current_state != AXIS_STATE_IDLE:
                time.sleep(0.1)
            print("State: " + str(mot_i.current_state))
            print("encoder is ready = " + str(mot_i.encoder.is_ready))  # Esta listo el encoder?
            print("entering close loop control mode..")
        mot_i.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  # entrar en modo closed loop control
        print("State: " + str(mot_i.current_state))
        mot_i.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL  # controlar por velocidad para llegar a LS
        while LS == 0:
            mot_h.controller.vel_setpoint = vel
        mot_i.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL  # volver a controlar por posicion (devolverse del LS
        mot_i.controller.pos_setpoint = (mot_i.encoder.pos_estimate + LS_steps)
        print("Position setpoint is " + str(mot_i.controller.pos_setpoint))
        print(str(nombre) + "is in home")
    return [odrv_i, mot_i, encdr_i]

# Hombro
ID_h = ""
axis_h = 0
[odrv_h, mot_h, encdr_h] = def_mot(ID_h, hombro)
#vel = -100
#pasos_LS = 100
#[odrv_h, mot_h, encdr_h] = def_mot(ID_h, hombro, 1, vel, pasos_LS)  # para calibrar

# Codo
ID_cz = ""
[odrv_cz, mot_c, encdr_c] = def_mot(ID_cz, codo)
#vel = VERIFICAR
#pasos_LS = VERIFICAR
#[odrv_cz, mot_c, encdr_c] = def_mot(ID_cz, codo, 1, vel, pasos_LS) # para calibrar

# Z
[mot_z, encdr_z] = def_mot(ID_cz, z)[1:]
#vel = VERIFICAR
#pasos_LS = VERIFICAR
#[mot_z, encdr_z] = def_mot(ID_cz, z, 1, vel, pasos_LS)[1:] # para calibrar

#LS_break =   # definir esta variable como el 'or' entre todos los LS. Cortar en caso de emergencia, ignorando esto en el homing



