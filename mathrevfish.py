def read_ppm(filename):
    with open(filename, 'rb') as f:
        header = f.readline().decode().strip()
        if header != 'P6':
            raise ValueError('Only binary PPM (P6) is supported.')

        while True:
            line = f.readline().decode()
            if line.startswith('#'):
                continue
            else:
                width, height = map(int, line.strip().split())
                break

        maxval = int(f.readline().decode())
        assert maxval == 255

        data = list(f.read(width * height * 3))
        image = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
        idx = 0
        for y in range(height):
            for x in range(width):
                image[y][x][0] = data[idx]
                image[y][x][1] = data[idx+1]
                image[y][x][2] = data[idx+2]
                idx += 3
        return image, width, height

def write_ppm(filename, image, width, height):
    with open(filename, 'wb') as f:
        f.write(f'P6\n{width} {height}\n255\n'.encode())
        for y in range(height):
            for x in range(width):
                pixel = image[y][x]
                f.write(bytes(pixel))

def sqrt_approx(x):
    # Newton-Raphson method
    if x == 0:
        return 0
    guess = x / 2.0
    for _ in range(5):
        guess = 0.5 * (guess + x / guess)
    return guess

def pow5(x):
    x2 = x * x
    return x2 * x2 * x

# Load image
input_image, width, height = read_ppm('fisheye.ppm')

# Zoom Out
zoom_out_factor = 1.0
output_width = int(width * zoom_out_factor)
output_height = int(height * zoom_out_factor)

# Auto-determined parameters
cx_in = width / 2.0
cy_in = height / 2.0
cx_out = output_width / 2.0
cy_out = output_height / 2.0

# Change factors if need be
fx = fy = 0.8 * width
k1 = -0.56
k2 = 0.04

# Output image
output_image = [[[0, 0, 0] for _ in range(output_width)] for _ in range(output_height)]

# Dewarp
for y_out in range(output_height):
    for x_out in range(output_width):
        x = (x_out - cx_out) / fx
        y = (y_out - cy_out) / fy

        r2 = x * x + y * y
        r = sqrt_approx(r2)
        if r < 1e-6:
            r = 1e-6

        theta = r
        r_distorted = theta + k1 * theta * theta * theta + k2 * pow5(theta)

        x_distorted = x * r_distorted / r
        y_distorted = y * r_distorted / r

        x_src = int(fx * x_distorted + cx_in)
        y_src = int(fy * y_distorted + cy_in)

        if 0 <= x_src < width and 0 <= y_src < height:
            output_image[y_out][x_out] = input_image[y_src][x_src]
        else:
            output_image[y_out][x_out] = [0, 0, 0]

# Save image
write_ppm('undistorted.ppm', output_image, output_width, output_height)

