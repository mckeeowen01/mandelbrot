import torch
import subprocess
import time
from torchvision.utils import save_image
import math

torch.set_default_device('cuda') # Use GPU by default
torch.set_default_dtype(torch.float64) # Use 64 Bit floats

# MANDELBROT

def get_mandelbrot_frame(width, height, x_min, x_max, y_min, y_max, max_iter):
    x = torch.linspace(x_min, x_max, width)
    y = torch.linspace(y_min, y_max, height)
    X, Y = torch.meshgrid(x, y, indexing="xy")
    C = X + 1j * Y

    Z = torch.zeros_like(C, dtype=torch.complex128)
    alive = torch.ones(C.shape, dtype=bool)
    escape = torch.full(C.shape, max_iter, dtype=torch.int16) 

    for i in range(max_iter):
        Z[alive] = Z[alive] ** 2 + C[alive]         # Update alive pixels
        escaped_now = alive & (torch.abs(Z) > 2)    # Which just escaped this iteration?
        escape[escaped_now] = i                     # Record when they escaped
        alive &= ~escaped_now                       # Mark them as escaped
        if not alive.any():
            break                                   # All pixels escaped; End loop

    return escape

def mandelbrot_animation(width, height, x_min, x_max, y_min, y_max, max_iter, zoom, num_of_frames, centre):
    subprocess.run('rm -r animation; mkdir animation', shell=True)
    zoom_per_frame = zoom ** (1/num_of_frames)
    tic = time.perf_counter()
    for i in range(num_of_frames):
        # Update the corners of the image according to the zoom factor
        x_min = centre[0] - (centre[0] - x_min)/zoom_per_frame
        x_max = centre[0] + (x_max - centre[0])/zoom_per_frame
        y_min = centre[1] - (centre[1] - y_min)/zoom_per_frame
        y_max = centre[1] + (y_max - centre[1])/zoom_per_frame
        frame = get_mandelbrot_frame(width, height, x_min, x_max, y_min, y_max, max_iter)
        frame = frame.float()/max_iter
        frame = frame.cpu()

        file_name = 'animation/f' + str(i+1) + '.png'
        toc = time.perf_counter()
        print(i+1, '\t\t', str(toc-tic)[:6])
        save_image(frame, file_name)
    print(x_min, x_max, y_min, y_max, file=open("misc/mcorners.txt", "w"))

def get_julia_frame(width, height, x_min, x_max, y_min, y_max, max_iter, C):
    x = torch.linspace(x_min, x_max, width)
    y = torch.linspace(y_min, y_max, height)
    X, Y = torch.meshgrid(x, y, indexing="xy")
    Z = X + 1j * Y
    alive = torch.ones(Z.shape, dtype=bool)
    escape = torch.full(Z.shape, max_iter, dtype=torch.int16) 

    for i in range(max_iter):
        Z[alive] = Z[alive] ** 2 + C                # Update alive pixels
        escaped_now = alive & (torch.abs(Z) > 2)    # Which just escaped this iteration?
        escape[escaped_now] = i                     # Record when they escaped
        alive &= ~escaped_now                       # Mark them as escaped
        if not alive.any():
            break                                   # All pixels escaped; End loop

    return escape

def archimidean_spiral(x_0, y_0, growth_rate, theta):
    x = growth_rate*theta*math.cos(theta) + x_0
    y = growth_rate*theta*maty.sin(theta) + y_0
    return x + 1j*y

def julia_animation(width, height, x_min, x_max, y_min, y_max, max_iter, num_of_frames):
    subprocess.run('rm -r temp; mkdir temp', shell=True)  # Clear temp folder
    
    for i in range(num_of_frames):
        frame = get_julia_frame(width, height, x_min, x_max, y_min, y_max, max_iter, -0.75 + 0.1j)
        tic = time.perf_counter()                       # Start Timer
        frame = frame.float()/max_iter                  # Scale and convert to float32
        frame = frame.cpu()                             # Copy to CPU for speed

        file_name = 'temp/f' + str(i+1) + '.png'   
        toc = time.perf_counter()                       # End timer
        print(i+1, '\t\t', str(toc-tic)[:6])            
        save_image(frame, file_name)