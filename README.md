# Runwayml-Video-Generation-API-Call
This repo has codes for runwayml video image generation API call

This code uses **DALL-E-3** as base image generator model. User gives **text prompt** hardcoded into the code to generate an image and download it in local directory called **"generated_content"**. The images are named as _image_1.png_, _image_2.png_ and so on. Images are downlaoded as .png format with size 1024x1024. The format can be changed to .jpg also. 

Then, the image (say image_1.png) is converted to **base64** format. Such conerverted format + **text prompt** together used to call the **gen3a_turbo** model from runwayml API. The call generated a video of _5 seconds_ duration. Then the generated video is downloaded as _video_1.mp4, video_2.mp4_, so on (in .mp4 format) in the same directory i.e. **"generated_content"**. 

The code uses one generated image (from DALL-E-3) to generate one video (from runwayml).

# Buy API credits

  Buy API credits for runwayml by making an organization.

  Buy ChatGPT4o pro subscription that gives DALL-E-3 service too. 

# Use .env 

1. **Install dependencies**

   pip install -r requirements.txt
   
2. **Make a .env file**

   The **.env** file where you replace **ENTER-YOUR-DALL-E-API-KEY** and **ENTER-YOUR-RUNWAYML-API-KEY** with your actual API key from  [runwayml API](https://dev.runwayml.com/organization/11823b9f-5ee7-4412-84fe-0c226e71c628/api-keys))

   OPENAI_API_KEY=**ENTER-YOUR-DALL-E-API-KEY**

   RUNWAYML_API_SECRET=**ENTER-YOUR-RUNWAYML-API-KEY**

  **AND**

  In a **shell terminal** (Linux and MAC):
  
    export RUNWAYML_API_SECRET=**ENTER-YOUR-RUNWAYML-API-KEY**

 _Note: For windows, no key export support exists_

3. **Change the  "num_generations"**

    If num_generations = 2, then 2 images and 2 videos will be generated and downloaded. If num_generations = 5, then 5 images and 5 videos will be generated and downloaded. So, change the value as per your requirement. 
 
4. **Run the code below**

   python runwayml_gen3a_turbo.py

  This code calls **gen3a_turbo** image-to-video generation model API to generate 5 second video. This model needs both "Image" + "Text". "Image" is mandatory. The prompt is already given inside the code _main_prompt_. You can change the _main_prompt_ accordingly. 

