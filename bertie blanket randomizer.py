import matplotlib.pyplot as plt
from matplotlib import colors, figure
import numpy as np
import time

# fmt: off
morse_code = {
    1: [3, 4, 5, 7, 9, 11],  					# B  --- . . .
    4: [4],  									# E  .
    7: [5, 7, 8, 9, 11],  						# R  . --- .
    10: [7, 8, 9],  							# T  ---
    13: [9, 11],  								# I  . .
    16: [12],  									# E  .
    19: [5, 7, 8, 9, 11, 12, 13, 15, 16, 17],  	# J  . --- --- ---
    22: [8, 9, 10, 12, 14, 15, 16, 18],  		# C  --- . --- .
    25: [15, 17, 18, 19],  						# A  . ---
    28: [18, 19, 20],  							# T  ---
}
# fmt: on

# Change to values between 1 and 9 for which grey blocks to use
darkest_color = 2
lightest_color = 7

data = np.random.randint(darkest_color, lightest_color, (30, 24))

prev_row = [0] * 24

for row_num, strip in enumerate(data):
    if row_num not in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28]:
        data[row_num] = [0] * 24

    else:
        prev_color = None
        for block, color in enumerate(strip):
            while color == prev_color or color == prev_row[block]:
                color = np.random.randint(darkest_color, lightest_color)
            strip[block] = color
            prev_color = color

        # morse code
        white_spots = morse_code.get(row_num)
        for spot in white_spots:
            strip[spot] = 9

        # eye-nose-eye
        nose_position = np.random.randint(2, 23)
        while (
            nose_position in white_spots
            or nose_position - 1 in white_spots
            or nose_position + 1 in white_spots
        ):
            nose_position = np.random.randint(2, 23)

        nose = np.random.randint(12, 14)
        while prev_row[nose_position] == nose:
            nose = np.random.randint(12, 14)

        eye = np.random.randint(10, 12)
        while prev_row[nose_position - 1] == eye:
            eye = np.random.randint(10, 12)

        strip[nose_position - 1] = eye
        strip[nose_position] = nose
        strip[nose_position + 1] = eye

        prev_row = strip

# create discrete colormap
cmap = colors.ListedColormap(
    [
        "#000000",
        "#262626",
        "#404040",
        "#595959",
        "#808080",
        "#a6a6a6",
        "#bfbfbf",
        "#d9d9d9",
        "#f2f2f2",
        "#ffffff",
        "olivedrab",
        "yellowgreen",
        "#654321",
        "#3F250B",
    ]
)
bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
norm = colors.BoundaryNorm(bounds, 14)

fig, ax = plt.subplots()
fig.set_figheight(30)
fig.set_figwidth(24)
ax.imshow(data, cmap=cmap, norm=norm)

# draw gridlines
# ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(0, 24, 1))
ax.set_xticklabels(np.arange(1, 25, 1))
ax.set_yticks(np.arange(0, 30, 1))
ax.set_yticklabels(np.arange(1, 31, 1))

filename = int(time.time())

f = open(f"{filename}.txt", "w")

inventory = {}

print("Layout:")
f.write("Layout:\n")
for row_num, strip in enumerate(data):
    if row_num in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28]:
        print(f"{row_num + 1: >2}: {strip}")
        f.write(f"{row_num + 1: >2}: {strip}\n")
        for block in strip:
            inventory[block] = inventory.get(block, 0) + 1

print()
f.write("\n")

print("Inventory:")
f.write("Inventory:\n")
for block in sorted(inventory):
    print(f"{block: >2}: {inventory[block]: >2}")
    f.write(f"{block: >2}: {inventory[block]: >2}\n")

f.close()

# plt.show()
# plt.close()

fig.savefig(f"{filename}.pdf", dpi=300, bbox_inches="tight")
