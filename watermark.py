import rawpy
import numpy as np
from PIL import Image
import os 
from multiprocessing import Pool, cpu_count

def convert_nef_to_jpeg(nef_path, jpeg_path):
    try:
        with rawpy.imread(nef_path) as raw:
            rgb = raw.postprocess()
            img = Image.fromarray(rgb)
            img.save(jpeg_path, format="JPEG")
    except Exception as e:
            print(f"Error converting {nef_path}: {e}")

def add_watermark(image_path, output_path, watermark_image, quality=85):
    try:
        image = Image.open(image_path).convert("RGBA")
        watermark = Image.open(watermark_image).convert("RGBA")
        
        scale_factor = 0.5
        watermark = watermark.resize((int(image.size[0] * scale_factor), int(image.size[1] * scale_factor)), Image.LANCZOS)
        
        watermarked_image = Image.new("RGB", image.size)
        watermarked_image.paste(image, (0, 0))

        watermark_position = ((image.size[0] - watermark.size[0]) // 2, (image.size[1] - watermark.size[1]) // 2)
        watermarked_image.paste(watermark, watermark_position, watermark)

        watermarked_image = watermarked_image.convert("RGB")
        watermarked_image.save(output_path, format="JPEG", quality=quality, optimize=True)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def process_image(args):
    nef_path, jpeg_path, output_path, portrait_watermark, landscape_watermark = args
    
    try:
        print(f"Converting {nef_path} to JPEG...")
        convert_nef_to_jpeg(nef_path, jpeg_path)
        
        print(f"Adding watermark to {jpeg_path}...")
        with Image.open(jpeg_path) as img:
            width, height = img.size
            if width >= height:
                watermark_image = landscape_watermark
            else:
                watermark_image = portrait_watermark
        
        add_watermark(jpeg_path, output_path, watermark_image)
        print(f"Saved watermarked image to {output_path}")

        os.remove(jpeg_path)
        print(f"Deleted the temporary JPEG file: {jpeg_path}")
    except Exception as e:
        print(f"Error processing {nef_path}: {e}")

def rename_and_watermark_images(directory, portrait_watermark, landscape_watermark):
    image_paths = []
    watermarked_folder = os.path.join(directory, 'watermarked')

    if not os.path.exists(watermarked_folder):
        os.makedirs(watermarked_folder)
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.nef'):
                nef_path = os.path.join(root, file)
                jpeg_path = os.path.join(root, f"{os.path.splitext(file)[0]}.jpg")
                folder_name = os.path.basename(root)
                new_file_name = f"{folder_name}_{os.path.basename(jpeg_path)}"
                output_path = os.path.join(watermarked_folder, new_file_name)
                
                image_paths.append((nef_path, jpeg_path, output_path, portrait_watermark, landscape_watermark))
    
    num_workers = cpu_count()
    print(f"Processing {len(image_paths)} images...")
    with Pool(num_workers) as pool:
        pool.map(process_image, image_paths)

if __name__ == "__main__":
    directory = "./images"  # CHANGE THIS TO IMAGE DIRECTORY
    portrait_watermark = "./watermarks/portrait_watermark.png"
    landscape_watermark = "./watermarks/portrait_watermark.png"
    rename_and_watermark_images(directory, portrait_watermark, landscape_watermark)