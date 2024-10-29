import requests
import time

# ASCII logo of Lx
def show_logo():
    print(r"""
##       ##   #   
##        ##  #   
##        ## #    
##         ##     
##         ##     
##        # ##    
##       #  ##    
######   #   ##   
      
    """)
    
# Function to enhance photo from URL
def enhance_via_url():
    image_url = input("Enter the URL of the image: ")
    response = requests.get(image_url)
    if response.status_code == 200:
        files = {
            'file': ('image_from_url.jpg', response.content, 'image/jpeg')
        }
        code = enhance(files)
        print(f"Image enhancement started with code: {code}")
        result(code)
    else:
        print("Failed to fetch image from URL.")

# Function to enhance photo from file
def enhance_via_file():
    file_path = input("Enter the file path: ")
    try:
        with open(file_path, 'rb') as file:
            files = {
                'file': (file_path, file, 'image/jpeg')
            }
            code = enhance(files)
            print(f"Image enhancement started with code: {code}")
            result(code)
    except FileNotFoundError:
        print("File not found. Please check the file path.")

# Function to send the image and get the enhancement code
def enhance(files):
    url = "https://photoai.imglarger.com/api/PhoAi/Upload"
    data = {
        'type': '2',
        'scaleRadio': '2'
    }
    headers = {
        "Host": "photoai.imglarger.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Origin": "https://imglarger.com",
        "X-Requested-With": "mark.via.gp",
        "Referer": "https://imglarger.com/"
    }
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        result_data = response.json()
        return result_data["data"]["code"]
    else:
        print("Error uploading image.")
        return None

# Function to check the status of the image enhancement
def result(code):
    check_status_url = "https://photoai.imglarger.com/api/PhoAi/CheckStatus"
    headers = {
        "Host": "photoai.imglarger.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Origin": "https://imglarger.com",
        "X-Requested-With": "mark.via.gp",
        "Referer": "https://imglarger.com/"
    }
    data = {
        "code": code,
        "type": 2
    }
    
    # Polling the result until it's successful
    while True:
        response = requests.post(check_status_url, headers=headers, json=data)
        if response.status_code == 200:
            result_data = response.json()
            status = result_data["data"]["status"]
            if status == "success":
                download_url = f"https://photoai.imglarger.com/color-enhancer/{code}.jpg"
                print(f"Enhancement completed! Download your image here: {download_url}")
                break
            else:
                print("Enhancement in progress... checking again in 5 seconds.")
                time.sleep(5)
        else:
            print("Error checking status.")
            break

# Function to simulate joining a community
def join_community():
    print("Redirecting to community... (simulated)")

# Main menu loop
def main_menu():
    while True:
        show_logo()
        print("1. Enhance photo via URL")
        print("2. Enhance photo from file")
        print("3. Join my community")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            enhance_via_url()
        elif choice == '2':
            enhance_via_file()
        elif choice == '3':
            join_community()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main_menu()
