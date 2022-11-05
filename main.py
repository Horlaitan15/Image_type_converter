from bs4 import BeautifulSoup
import re
import requests
from tqdm import tqdm
import pyfiglet
from PIL import Image
import glob
import os
from colorama import Fore



font = pyfiglet.figlet_format('Image Downloader and Type Converter.', font = 'utopia', width=150) # doh, utopia xsans, gothic, 5lineoblique
print(font)
print(Fore.MAGENTA + "-- The script automatically downloads JPEG images from https://unsplash.com/s/photos/jpg.\n")
print(Fore.WHITE + "-- It then convert the JPEG images to PNG.\n")
print(Fore.CYAN + "-- Then it creates a LEFT-RIGHT mirror of the png image.\n\n")

def image_downloader():
    print(Fore.YELLOW + "Downloading Images...\n" + Fore.WHITE)
    images = []
    res = requests.get("https://unsplash.com/s/photos/jpg").content
    soup = BeautifulSoup(res, 'lxml')
    image_elements = soup.find_all('img')
    for image in image_elements:
        images.append(image['src'])

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'}
    for image_link in images[:21]:
        filename = os.path.join("output/", re.findall(r'https://([a-zA-Z0-9-.//]*)?', image_link)[0].split('/')[-1])
        if not filename.endswith('.jpg'):
            filename += '.jpg'


        d_image = requests.get(image_link, headers=headers, stream=True)

        vid_size = int(d_image.headers['content-length'])

        # Save image content.
        with open(filename, 'wb') as con:
            for data in tqdm(iterable=d_image.iter_content(chunk_size=1024), total = vid_size/1024, unit = 'KB'):
                con.write(data)

        print(Fore.GREEN + f"Image saved to output folder as {filename.split('/')[1]}\n")

def convert_format():
    print(Fore.BLUE + "Starting images to PNG format...\n")
    for image in glob.glob('output/*.jpg'):
        im = Image.open(image)
        rgb_im = im.convert('RGB')
        rgb_im.save(image.replace("jpg", "png"), quality=95)
        print(Fore.WHITE + f"{image.split('/')[1]} converted and saved to in the output folder as {image.split('/')[1].replace('jpg', 'png')}\n")

    print(Fore.GREEN + "All images has been succefully converted to PNG.\n")

def transpose_image():
    print("Transposing images...")
    for image in glob.glob("output/*.png"):
        im = Image.open(image)
        mirror = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        image_mirror = image.split('.')
        image_mirror.insert(1, "-mirrored.")
        mirror.save("".join(image_mirror))
        print(Fore.WHITE + f"{image.split('/')[1]} converted and saved to in the output folder as {''.join(image_mirror).split('/')[1]}\n")

    print("JOB DONE!".center(150))

    print(pyfiglet.figlet_format("Thanks,\nAjani", font='doh', width=400))

if __name__ == "__main__":
    # image_downloader()
    convert_format()
    # transpose_image()
    
