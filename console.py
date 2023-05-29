import requests

url = 'http://127.0.0.1:5000/process_invoice'
file_path = './sample.png'

with open(file_path, 'rb') as file:
    files = {'invoice_photo': file}
    response = requests.post(url, files=files)

print(response.json())