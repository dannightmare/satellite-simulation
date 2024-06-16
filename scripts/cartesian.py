import math

# Given coordinates in degrees for New York City
longitude_deg = 35.578811
latitude_deg = 33.235295
R = 6371  # Radius of the Earth in kilometers

# Convert degrees to radians
longitude_rad = math.radians(longitude_deg)
latitude_rad = math.radians(latitude_deg)

# Calculate Cartesian coordinates
x = R * math.cos(latitude_rad) * math.cos(longitude_rad)
y = R * math.cos(latitude_rad) * math.sin(longitude_rad)
z = R * math.sin(latitude_rad)

print(x, z, -y)
