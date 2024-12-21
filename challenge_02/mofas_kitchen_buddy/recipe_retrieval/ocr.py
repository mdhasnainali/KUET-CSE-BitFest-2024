import requests
import base64
import json

def extract_text_from_image(image_url, api_key):
    """
    Extracts text from an image using OpenAI API.

    Parameters:
        image_url (str): The URL of the image to process.
        api_key (str): Your OpenAI API key.
        mode (str): The annotation mode ("detailed", "short", or ""). Default is "detailed".

    Returns:
        str: Extracted text from the image.
    """
    # Download the image from the URL
    try:
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        image_data = image_response.content
    except requests.RequestException as e:
        return f"Error downloading the image: {e}"

    # Convert image to Base64
    base64_image = base64.b64encode(image_data).decode("utf-8")

    # Define the payload
    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Extract text from this image. and provide a recipe in this format: 
```
Recipe: <recipe_name>
Taste: <taste_score out of 5> 
Cuisine Type: <cuisine_type>
Preparation Time: <preparation_time>
Reviews: <reviews>
```
example:
```
Recipe: Tacos
Taste: 4.6/5
Cuisine Type: Mexican
Preparation Time: 25 minutes
Reviews: 1200
```
If theres not enough information to provide a recipe like this, repond with 'ERROR'"""

                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    # Define headers
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json; charset=utf-8"
    }

    # Send the request to the OpenAI API
    url = "https://api.openai.com/v1/chat/completions"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        return response_data  # Return the full response for now
    except requests.RequestException as e:
        return f"Error communicating with OpenAI API: {e}"
    except KeyError:
        return "Error: Unexpected response format."

# Example usage
if __name__ == "__main__":
    IMAGE_URL = "https://example.com/sample-image.jpg"
    API_KEY = "your_openai_api_key"
    result = extract_text_from_image(IMAGE_URL, API_KEY, mode="detailed")
    print(result)