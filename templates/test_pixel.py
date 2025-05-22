from pixel_art import pixel_art_generator

output_file = pixel_art_generator('"C:\Users\arpit\OneDrive\Desktop\doggy.jpg"', pixel_size=32, k_colors=10)
print(f"Pixel art saved as {output_file}")