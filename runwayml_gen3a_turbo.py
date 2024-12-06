# Partha Pratim Ray
# 6/12/2024

## runwayml video generation

#################

# First do export runwayml api otherwise it doesnot work, we can't save it the .env file

################# 
######  export RUNWAYML_API_SECRET=YOUR-RUNWAYML-API
################
######## For windows, no key export support exists


import os
import time
import requests
import base64
from dotenv import load_dotenv
from runwayml import RunwayML
from openai import OpenAI

# Load environment variables from .env file
if load_dotenv():
    print(".env file loaded successfully.")
else:
    print("Failed to load .env file.")

# Retrieve API keys from the .env file
openai_api_key = os.getenv("OPENAI_API_KEY")
runwayml_api_key = os.getenv("RUNWAYML_API_SECRET")

if not openai_api_key or not runwayml_api_key:
    raise ValueError("API keys not found. Please add them to the .env file.")

# Initialize OpenAI and RunwayML clients
openai_client = OpenAI(api_key=openai_api_key)
runwayml_client = RunwayML(api_key=runwayml_api_key)

def encode_image_to_base64(image_path):
    print(f"[DEBUG] Encoding image: {image_path} to base64...")
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")

def generate_single_image(prompt, size="1024x1024", output_folder="generated_content", image_index=1):
    """Generate a single image using the DALL·E 3 model (which requires n=1)."""
    os.makedirs(output_folder, exist_ok=True)
    try:
        print(f"[DEBUG] Generating image {image_index} for prompt: '{prompt}' with DALL·E 3...")
        # Must use n=1 due to model limitation
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            n=1
        )
        print("[DEBUG] 1 image generated successfully.")

        image_data = response.data[0]
        image_url = image_data.url
        print(f"[DEBUG] Downloading image {image_index} from URL: {image_url}")
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image_path = os.path.join(output_folder, f"image_{image_index}.png")
            with open(image_path, "wb") as file:
                file.write(image_response.content)
            print(f"[DEBUG] Image saved: {image_path}")
            return image_path
        else:
            print(f"[ERROR] Failed to download image {image_index} from: {image_url}")
            return None
    except Exception as e:
        print(f"[ERROR] An error occurred during image generation: {e}")
        return None

def generate_video(image_path, prompt, model_name="gen3a_turbo", duration=5, output_folder="generated_content", index=1):
    os.makedirs(output_folder, exist_ok=True)
    try:
        base64_image = encode_image_to_base64(image_path)
        print(f"[DEBUG] Sending prompt and encoded image to RunwayML {model_name} model for video {index}...")
        
        video_task = runwayml_client.image_to_video.create(
            model=model_name,
            prompt_image=f"data:image/png;base64,{base64_image}",
            prompt_text=prompt,
            duration=duration
        )

        task_id = video_task.id
        print(f"[DEBUG] Task created with ID: {task_id}. Polling for status...")

        # Poll the task until it is complete or failed
        while True:
            task_status = runwayml_client.tasks.retrieve(id=task_id)
            current_status = task_status.status
            print(f"[DEBUG] Current task status for video {index}: {current_status}")

            if current_status == "SUCCEEDED":
                print("[DEBUG] Task succeeded. Downloading the video...")
                print("[DEBUG] Output structure:", task_status.output)

                if isinstance(task_status.output, list) and len(task_status.output) > 0:
                    video_url = task_status.output[0]
                    print(f"[DEBUG] Video URL: {video_url}")
                    video_response = requests.get(video_url)

                    if video_response.status_code == 200:
                        # Name the video file to match the image index
                        video_path = os.path.join(output_folder, f"video_{index}.mp4")
                        with open(video_path, "wb") as video_file:
                            video_file.write(video_response.content)

                        abs_video_path = os.path.abspath(video_path)
                        print(f"[DEBUG] Video saved at: {abs_video_path}")
                        return video_path
                    else:
                        print(f"[ERROR] Failed to download video from URL: {video_url}, Status: {video_response.status_code}")
                        return None
                else:
                    print("[ERROR] Output does not contain a valid video URL.")
                    return None

            elif current_status == "FAILED":
                print("[ERROR] Task failed.")
                return None
            else:
                print("[DEBUG] Task is still processing. Waiting for 10 seconds...")
                time.sleep(10)

    except Exception as e:
        print(f"[ERROR] An error occurred during video generation: {e}")
        return None


def generate_images_and_videos(prompt, n=1, image_size="1024x1024", video_duration=5):
    print(f"[DEBUG] Starting generation of {n} images and videos for prompt: '{prompt}'")

    for i in range(1, n + 1):
        # Generate one image at a time
        image_path = generate_single_image(prompt, size=image_size, output_folder="generated_content", image_index=i)
        if image_path is None:
            print(f"[ERROR] Could not generate image {i}, skipping video generation for this iteration.")
            continue

        # Generate corresponding video
        generate_video(
            image_path=image_path,
            prompt=prompt,
            model_name="gen3a_turbo",
            duration=video_duration,
            output_folder="generated_content",
            index=i
        )

    print("[DEBUG] All requested image and video generation tasks completed.")


if __name__ == "__main__":
    main_prompt = "A serene landscape with mountains and a river at sunset." # Change the prompt as your wish
    num_generations = 1  # Change to have 
    generate_images_and_videos(prompt=main_prompt, n=num_generations, image_size="1024x1024", video_duration=5)
