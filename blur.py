import sys
from PIL import Image

# Define a type shortcut
pixel = tuple[int, int, int, int]

# Check for correct number of args
if len(sys.argv) not in (2, 3): raise Exception("Invalid number of arguments")

if len(sys.argv) != 3:
	strength = 1
else:
	strength = int(sys.argv[2])

# Open the image
with Image.open(sys.argv[1]).convert('RGBA') as in_img:
	out_img = Image.new('RGBA', (in_img.width, in_img.height))

	data: dict[(int, int), pixel] = in_img.load() # type: ignore
	for x in range(in_img.width):
		for y in range(in_img.height):
			neighbors = [data[a+x, b+y] for b in range(-strength, strength+1)
										for a in range(-strength, strength+1)
						
						if (a + x>= 0 and a + x < in_img.width - 1
							and b + y >= 0 and b + y < in_img.height-1)]
			
			total = len(neighbors)

			new_px = [0, 0, 0, 0]
			for neigh in neighbors:
				for n in range(4):
					new_px[n] += neigh[n]

			for n in range(4):
				new_px[n] = new_px[n] // total

			out_img.putpixel((x, y), tuple(new_px))
	
	out_img.save("out2.png")