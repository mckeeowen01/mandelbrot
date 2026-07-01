import render
import subprocess

subprocess.run('rm -r ~/mandelthings/temp; mkdir ~/mandelthings/temp', shell=True) # Clear temporary storage

# VARIABLES
WIDTH = 1620
HEIGHT = 1080
X_MIN_0, X_MAX_0 = -2.2, 1
Y_MIN_0, Y_MAX_0 = -1.2, 1.2
MAX_ITERATIONS = 500

# MANDELBROT SPECIFIC
ZOOM_FACTOR = 1.586 * (10**17)
NUMBER_OF_FRAMES = 3600
CENTRE = (-0.931334024, 0.261442512)



#render.mandelbrot_animation(WIDTH, HEIGHT, X_MIN_0, X_MAX_0, Y_MIN_0, Y_MAX_0, MAX_ITERATIONS, ZOOM_FACTOR, NUMBER_OF_FRAMES, CENTRE) # Style of mandelbrotzoom.mp4

render.julia_animation(1080, 1080, -3, 3, -2, 2, 1000, 1)
