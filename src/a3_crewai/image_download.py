import os
import requests
import json

def batch_download_image_assets():
    images_json_path = "./images/manifest.json"  # Or wherever your manifest is

    if os.path.exists(images_json_path):

        with open(images_json_path, "r") as f:
            manifest = json.load(f)

        assets = manifest.get("assets", [])

        if not assets:
            print("⚠️ No assets found in the manifest!")
            return

        os.makedirs("output/images", exist_ok=True)

        for asset in assets:
            filename = asset.get("filename")
            url = asset.get("url")

            if not filename or not url:
                print(f"⚠️ Skipping invalid entry: {asset}")
                continue

            try:
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    image_path = os.path.join("output/images", filename)
                    with open(image_path, "wb") as img_file:
                        img_file.write(response.content)
                    print(f"✅ Image saved: {filename}")
                else:
                    print(f"⚠️ Failed to download {filename}: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Error downloading {filename}: {e}")

    else:
        print("❌ Manifest file not found at:", images_json_path)

batch_download_image_assets()