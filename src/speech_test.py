import requests
import shutil

# Data for the API request
data = {
    'token': '123456',
    'email': 'achristendat@gmail.com',
    'voice': 'John',  # Manually input the desired voice here
    'text': "Text",
    'format': 'mp3',
    'speed': 1.1,
    'pitch': 0,
    'emotion': 'good',
}

# URL for the API
url = "https://speechgen.io/index.php?r=api/text"

try:
    # Make the POST request
    response = requests.post(url, data=data, verify=False)

    # Check if the response was successful
    if response.status_code == 200:
        response_data = response.json()

        # If status is 1, the request was successful
        if response_data.get("status") == 1:
            print("ok", response_data["file"])

            # Download the file
            with requests.get(response_data["file"], stream=True) as file_response:
                if file_response.status_code == 200:
                    with open(f'Filename.{data["format"]}', 'wb') as f:
                        shutil.copyfileobj(file_response.raw, f)
                else:
                    print(f"Error downloading file: {file_response.status_code}")
        else:
            print("Error:", response_data.get("error"))
    else:
        print(f"Connection error with text recognition server: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")
