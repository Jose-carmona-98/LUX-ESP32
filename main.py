import time
from machine import Pin, I2C, PWM
from bh1750 import BH1750
 
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # bus I2C
sensor = BH1750(i2c)                    # direccion 0x23
led_pwm = PWM(Pin(18), freq=1000)       # PWM 1 kHz -> MOSFET
 
SETPOINT = 500.0   # consigna [lx]
Kp = 0.05          # evita saltos bruscos
Ki = 0.08          # accion integral suave
Kd = 0.0           # sin derivada
error_previo = 0.0
integral = 0.0
tiempo_previo = time.ticks_ms()
 
try:
    while True:
        tiempo_actual = time.ticks_ms()
        dt = time.ticks_diff(tiempo_actual,
                             tiempo_previo) / 1000.0
        if dt <= 0:
            dt = 0.01
        tiempo_previo = tiempo_actual
        try:
            lux_actual = sensor.luminance(
                BH1750.CONT_HI_RES)
        except Exception as e:
            print('Error leyendo sensor:', e)
            time.sleep(0.2)
            continue
        error = SETPOINT - lux_actual
        integral += error * dt
        integral = max(0.0, min(12000.0, integral))
        derivada = (error - error_previo) / dt
        error_previo = error
        salida_pid = (Kp*error + Ki*integral
                      + Kd*derivada)
        pwm_val = max(0, min(1023, int(salida_pid)))
        led_pwm.duty(pwm_val)
        porcentaje_pwm = pwm_val / 1023.0 * 100.0
        print(f'Lux: {lux_actual:6.1f} | '
              f'Error: {error:6.1f} | '
              f'PWM: {pwm_val:4d} ({porcentaje_pwm:5.1f}%)')
        # (opcional) telemetria cada 15 s: omitida aqui
        time.sleep(0.2)
except KeyboardInterrupt:
    led_pwm.duty(0)   # apagado seguro
    print('Control detenido.')
