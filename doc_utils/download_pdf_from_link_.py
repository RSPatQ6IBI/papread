import requests

def download_pdf(url, save_path):
    # Use stream=True to download in chunks
    response = requests.get(url, stream=True)
    
    # Check if the request was successful
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"File downloaded successfully to: {save_path}")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

