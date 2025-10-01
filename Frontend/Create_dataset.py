from duckduckgo_search import DDGS
import requests, os
import os
from PIL import Image
from tqdm import tqdm
import time
from urllib.parse import urlparse
import random
time.sleep(random.uniform(1, 3))

def download_images(query, folder, max_images=50):
    """Download images for a given query using DuckDuckGo search"""
    os.makedirs(folder, exist_ok=True)
    
    # Initialize DDGS and get image results
    try:
        ddgs = DDGS()
        results = list(ddgs.images(
            keywords=query,
            max_results=max_images
        ))
    except Exception as e:
        print(f"Error with DDGS search: {e}")
        return 0
    
    print(f"Found {len(results)} results for '{query}'")
    
    successful_downloads = 0
    
    for i, result in enumerate(tqdm(results, desc=f'Downloading {query}')):
        try:
            # Get image URL
            img_url = result.get('image')
            if not img_url:
                continue
                
            # Download with proper headers and timeout
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(img_url, headers=headers, timeout=10, stream=True)
            response.raise_for_status()
            
            # Check if content is actually an image
            content_type = response.headers.get('content-type', '').lower()
            if not content_type.startswith('image/'):
                continue
            
            # Get file extension from content type or URL
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = 'jpg'
            elif 'png' in content_type:
                ext = 'png'
            elif 'gif' in content_type:
                ext = 'gif'
            elif 'webp' in content_type:
                ext = 'webp'
            else:
                # Fallback to URL extension
                parsed_url = urlparse(img_url)
                ext = parsed_url.path.split('.')[-1].lower()
                if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                    ext = 'jpg'  # Default fallback
            
            # Create safe filename
            safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_query = safe_query.replace(' ', '_')
            filename = f"{safe_query}_{successful_downloads:03d}.{ext}"
            filepath = os.path.join(folder, filename)
            
            # Save the image
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Validate the image by trying to open it
            try:
                with Image.open(filepath) as img:
                    # Convert to RGB if necessary and save as JPG for consistency
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    
                    # Optionally resize large images
                    if img.size[0] > 1024 or img.size[1] > 1024:
                        img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                    
                    # Save as JPG for consistency
                    if ext != 'jpg':
                        jpg_filepath = filepath.rsplit('.', 1)[0] + '.jpg'
                        img.save(jpg_filepath, 'JPEG', quality=95)
                        os.remove(filepath)  # Remove original
                        
                successful_downloads += 1
                
            except Exception as img_error:
                # Remove invalid image file
                if os.path.exists(filepath):
                    os.remove(filepath)
                print(f"Invalid image file removed: {filename}")
                continue
            
            # Small delay to be respectful to servers
            time.sleep(0.1)
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image {i} for {query}: Network error - {e}")
            continue
        except Exception as e:
            print(f"Failed to download image {i} for {query}: {e}")
            continue
    
    print(f"Successfully downloaded {successful_downloads} images for '{query}'")
    return successful_downloads

# Categories you want
categories = ['dog', 'cat', 'elephant', 'snake', 'parrot', 'butterfly', 'fish']

# Create main dataset directory
os.makedirs('dataset', exist_ok=True)

total_downloaded = 0
for animal in categories:
    print(f"\n--- Processing {animal} ---")
    downloaded = download_images(animal, folder=f'dataset/{animal}', max_images=50)
    total_downloaded += downloaded
    
    # Small delay between categories
    time.sleep(1)

print(f"\n=== Download Complete ===")
print(f"Total images downloaded: {total_downloaded}")
print(f"Dataset saved in: ./dataset/")
