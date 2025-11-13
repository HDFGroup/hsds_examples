import time
import signal
import sys
import numpy as np
import h5pyd as h5py

def signal_handler(sig, frame):
    print('quitting!')
    sys.exit(0)

def lerp(a, b, t):
    """
    Linear interpolation between two values.
    
    Parameters:
    - a (float): Start value.
    - b (float): End value.
    - t (float): Interpolation factor between 0.0 and 1.0.
    
    Returns:
    - result (float): Interpolated value between a and b.
    """
    return a + t * (b - a)

def smoothstep(t):
    """
    Smoothstep function for interpolation.
    
    Parameters:
    - t (float): Interpolation value between 0.0 and 1.0.
    
    Returns:
    - result (float): Smoothstep interpolated value.
    """
    return t * t * (3 - 2 * t)


def generate_perlin_noise(width, height, scale):
    """
    Generate Perlin noise using the given parameters.
    
    Parameters:
    - width (int): Width of the noise array.
    - height (int): Height of the noise array.
    - scale (int): Scale factor for generating the noise.
    
    Returns:
    - noise (n-dimensional array): Perlin noise array of shape (height, width).
    """

    
    # Create an empty noise array
    noise = np.zeros((height, width))
    
    # Generate random gradient vectors
    gradients = np.random.randn(height // scale + 2, width // scale + 2, 2)
 
    # Iterate over each pixel in the noise array
    for y in range(height):
        for x in range(width):
            # Calculate the grid cell coordinates for the current pixel
            cell_x = x // scale
            cell_y = y // scale
 
            # Calculate the position within the cell as fractional offsets
            cell_offset_x = x / scale - cell_x
            cell_offset_y = y / scale - cell_y
 
            # Calculate the dot products between gradients and offsets
            dot_product_tl = np.dot([cell_offset_x, cell_offset_y], gradients[cell_y, cell_x])
            dot_product_tr = np.dot([cell_offset_x - 1, cell_offset_y], gradients[cell_y, cell_x + 1])
            dot_product_bl = np.dot([cell_offset_x, cell_offset_y - 1], gradients[cell_y + 1, cell_x])
            dot_product_br = np.dot([cell_offset_x - 1, cell_offset_y - 1], gradients[cell_y + 1, cell_x + 1])
          
            # Interpolate the dot products using smoothstep function
            weight_x = smoothstep(cell_offset_x)
            weight_y =  smoothstep(cell_offset_y)
            interpolated_top = lerp(dot_product_tl, dot_product_tr, weight_x)
            interpolated_bottom = lerp(dot_product_bl, dot_product_br, weight_x)
            interpolated_value = lerp(interpolated_top, interpolated_bottom, weight_y)
 
            # Store the interpolated value in the noise array
            noise[y, x] = interpolated_value
            
    # Normalize the noise values within the range of 0 to 1
    noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
 
    return noise


def sensor_update(sensor, scale_factor, frequency, update_interval):
    """ generate fake sensor signlas and update the hdf5 dataset based
    on the frequency and update_interval parameters."""

    packet_count = 0
    elements_per_packet = int(frequency * update_interval)

    # create 10 minutes of perlin noise data (will wrap if we run past that)
    count = elements_per_packet * 1000  # pre-compute some packet data
    noise = generate_perlin_noise(count, 1, scale_factor)
    noise = noise[0,:]  # convert to a 1D array
    start_time = sensor.attrs["start_time"]

    while True:
        # wait till we've crossed the next update interval
        next_update = start_time + (packet_count + 1) * update_interval
        sleep_time = next_update - time.time()
        if sleep_time > 0:
            print(f"sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        else:
            print("no sleep needed")
        num_elements = (packet_count + 1) * elements_per_packet
        if num_elements > sensor.shape[0]:
            print("extending dataset for next packet")
            # extend the dataset to stop_index
            sensor.resize((num_elements,))
        # write the data packet
        start_index = elements_per_packet * packet_count
        stop_index = elements_per_packet * (packet_count + 1)
        print(f"sensor {sensor.name} writing packet {packet_count}")
        sensor[start_index:stop_index] = noise[(start_index%count):(stop_index%count)]
        packet_count += 1

#
# main program
#

filepath = "hdf5://home/john/streamtest.h5"
sensor_name = "sensor1"
scale_factor = 500
frequency = 0.1
update_interval = 1.0 # seconds

if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
    print("Usage: python siggen.py [--filepath filepath] [--name name] [--scale n] [--freq n] [--update m]")
    sys.exit(0)

argname = None
for arg in sys.argv[1:]:
    if argname:
        if argname == "--filepath":
            filepath = arg
        elif argname == "--name":
            sensor_name = arg
        elif argname == "--scale":
            scale_factor = int(arg)
        elif argname == "--freq":
            frequency = int(arg)
        elif argname == "--update":
            update_interval = int(arg)
        argname = None
    elif arg.startswith("--"):
        argname = arg

print("filepath:", filepath)
print("sensor name:", sensor_name)
print("scale factor:", scale_factor)
print("frequency:", frequency)
print("update_interval:", update_interval)

signal.signal(signal.SIGINT, signal_handler)  # catch ctrl-c

with h5py.File(filepath, "a") as f:
    if "sensors" not in f:
        f.create_group("sensors")
    sensors_group = f["sensors"]
    if sensor_name in sensors_group:
        print(f"deleting previous run of sensor: {sensor_name}") 
        del sensors_group[sensor_name]

    print(f"creating sensor dataset /sensors/{sensor_name}")
    sensor = sensors_group.create_dataset(sensor_name, (0,), maxshape=(None,), dtype='f')
    sensor.attrs["description"] = f"sensor data for sensor {sensor_name}"
    sensor.attrs["frequency"] = frequency
    sensor.attrs["scale_factor"] = scale_factor
    sensor.attrs["update_interval"] = update_interval
    sensor.attrs["start_time"] = time.time()
    sensor.attrs["min_value"] = -1.0
    sensor.attrs["max_value"] = 1.0
    sensor.attrs["units"] = "amps"

    sensor_update(sensor, scale_factor, frequency, update_interval)

