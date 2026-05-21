import os, time, random
from PIL import Image
from multiprocessing import Pool

INPUT_DIR = "input"
OUTPUT_DIR = "processed"
PREFIX = "out_"

def create_test_images(n=10):
    
    os.makedirs(INPUT_DIR, exist_ok=True)
    for i in range(n):
        w, h = random.randint(400, 1200), random.randint(300, 900)
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        Image.new('RGB', (w, h), color).save(os.path.join(INPUT_DIR, f"img_{i}.jpg"))

def process_one(in_path):
   
    out_name = PREFIX + os.path.basename(in_path)
    out_path = os.path.join(OUTPUT_DIR, out_name)
    img = Image.open(in_path)
    img = img.rotate(-90, expand=True)            
    img = img.resize((800, 600), Image.LANCZOS)   
    img = img.convert('L')                         
    img.save(out_path)
    return out_path

if __name__ == "__main__":
   
    if not os.path.exists(INPUT_DIR) or not os.listdir(INPUT_DIR):
        create_test_images(10)

    
    files = sorted([
        os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR)
        if f.lower().endswith('.jpg')
    ])
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    
    start = time.time()
    for f in files:
        process_one(f)
    seq_time = time.time() - start
    print(f"Последовательно: {seq_time:.2f} сек")

    
    start = time.time()
    with Pool() as pool:
        pool.map(process_one, files)
    par_time = time.time() - start
    print(f"Параллельно:      {par_time:.2f} сек")