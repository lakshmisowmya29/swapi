import requests
def text_response(user_details, msg):
    print (msg)
    headers = {
            'api-key': 'Aeb7066bdec914ab45f6fa42f3facce64'
        }
    data = {
            'from': '+919663312872',
            'to': user_details,
            'type': 'text',
            'channel': 'whatsapp',
            'body': msg
        }
    response = requests.post("https://api.kaleyra.io/v1/HXIN1716747969IN/messages", headers=headers, data=data)
    print (response.text)
    return

def media_response(user_details, msg):
    headers = {
            'api-key': 'Aeb7066bdec914ab45f6fa42f3facce64',
        }
    data = {
            'from': '+919663312872',
            'to': user_details,
            'type': 'media',
            'channel': 'whatsapp',
            'media_url': msg
        }
    response = requests.post('https://api.kaleyra.io/v1/HXIN1716747969IN/messages', headers=headers, data=data)
    print (response.text)
    return

