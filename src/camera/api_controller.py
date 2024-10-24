from datetime import datetime, timedelta , timezone
import re
import requests
import cv2
import pytz


def build_rtsp_url(camera_ip, camera_username, camera_password , camera_port):
    return f"rtsp://{camera_username}:{camera_password}@{camera_ip}:{camera_port}/cam/realmonitor?channel=1&subtype=1"


def is_iso_format(date_string: str) -> bool:
    # Regular expression to match the ISO 8601 date format
    iso_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$'
    return bool(re.match(iso_regex, date_string))

# recording_url = app.config['RECORDING_URL']
# ai_url = app.config['AI_URL']
recording_url = 'http://192.168.10.108/'
ai_url = 'http://192.168.10.107/'


payload = {}
header = {
    'Content-Type': 'application/json'
}


def check_recording_api():
    try:
        response  = requests.get(recording_url)
        if response.status_code in range(500 , 599):
            return False 
    except Exception as e:
        return False
    return True

def check_ai_module_api():
    try:
        response  = requests.get(ai_url)
        if response.status_code in range(500,599):
            return False
    except Exception as e:
        print('AI module:' + e)
        return False
    return True 

def check_modules_status():
    if not check_ai_module_api or not check_recording_api():
        return False
    return True

    

def add_camera_api(camera_ip: str, camera_name: str, username: str, password: str, ai_properties: list, run_detection: bool):
    label = f"{camera_ip}-{camera_name}"
    rtsp_url = build_rtsp_url(camera_ip, username, password)
    
    payload = {
        "label": label,
        "input": rtsp_url
    }
    
    ai_payload = {
        "label": label, 
        "input": rtsp_url,
        "detections": ai_properties,
        "run_detection": run_detection
    }

    if not check_modules_status():
        return "Modules are not available", 500
    
    try:
        ai_response = requests.post(ai_url + "devices/", headers=header, json=ai_payload)
        ai_response.raise_for_status()
        
        print(f"AI Response Status Code: {ai_response.status_code}")
        print(f"AI Response Body: {ai_response.text}")

        print("Sending payload to recording URL:", payload)
        response = requests.post(recording_url + "devices/", headers=header, json=payload)
        response.raise_for_status()

        if ai_response.status_code in range(400, 600):
            return None, 506

        return ai_response.json(), ai_response.status_code

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while calling the API: {e}")
        return f"An error occurred: {str(e)}", 500

def edit_camera(camera_ip:str, camera_new_ip:str, camera_name:str, camera_new_name:str, username:str, new_username:str, password:str, new_password:str,recording:bool, ai_properties:list, run_detection:bool):

    label = f"{camera_ip}-{camera_name}"
    new_label = f"{camera_new_ip}-{camera_new_name}"

    rtsp_url = build_rtsp_url(camera_ip, username, password)
    new_rtsp_url = build_rtsp_url(camera_new_ip, new_username, new_password)

    # Define payloads based on whether the label has changed
    if label == new_label:
        payload = {"recording": recording}
        ai_payload = {
            "input": rtsp_url,
            "detections": ai_properties,
            "run_detection": run_detection
        }
    else:
        payload = {
            "label": new_label,
            "recording": recording
        }
        ai_payload = {
            "label": new_label,
            "input": new_rtsp_url,
            "detections": ai_properties,
            "run_detection": run_detection
        }

    if not check_modules_status():
        return None, 500

    try:
        response = requests.patch(recording_url + "devices/", headers=header, json=payload)
        response.raise_for_status() 

        ai_response = requests.patch(ai_url + "devices/", headers=header, json=ai_payload)
        ai_response.raise_for_status()

        return {
            "recording_module": response.json(),
            "ai_module": ai_response.json()
        }, 200

    except requests.RequestException as e:
        return False, f"Error in external service: {str(e)}"
    

def delete_camera_api(camera_ip:str , camera_name:str):
    label = f'{camera_ip} - {camera_name}'
    if not check_modules_status():
        return 500
    
    #sending delete request to ai api
    ai_response = requests.delete(ai_url + "devices/" + label , headers=header)
    ai_response.raise_for_status()

    return ai_response , True , "camera deleted successfully."


def get_all_cameras_from_record_module():
    if not check_modules_status():
        return None , 500
    response = requests.get(recording_url + "devices/" , headers=header, json=payload)
    response.raise_for_status()
    return response.json(), response.status_code
    
def toggle_recording_specific_camera(ip:str , name:str , bool:bool):
    payload = {"recording" :bool}
    camera_label = f'{ip}-{name}'
    if not check_modules_status():
        return 500
    response = requests.patch(recording_url + "devices/"+ camera_label , headers=header , json=payload)
    response.raise_for_status()
    return True , "Recording toggled successfully." , 200



def toggle_record_option_for_all(bool:str):
    payload = {"recording" :bool}
    cameras , status_code = get_all_cameras_from_record_module()
    if status_code == 500:
        return status_code
    for camera in cameras['data']['devices']:
        camera_label = camera['label']
        response = requests.patch(recording_url + "devices/"+camera_label , headers=header , json=payload)
        response.raise_for_status()
    return True , "Recording toggled successfully." , status_code


def get_alerts_from_api():
    response = requests.get(ai_url+"alerts/" , headers=header )
    response.raise_for_status()
    data = response.json()

    return data , response.status_code
def get_records_from_api(ip: str, name: str, start_time, end_time):
    if not start_time or not end_time:
        return "error: Start time or end time is missing", 400  

    try:
        if is_iso_format(start_time) and is_iso_format(end_time):
            start_time_gmt = start_time
            end_time_gmt = end_time
        else:
            start_time_gmt , end_time_gmt=make_time_gmt(start_time=start_time , end_time=end_time)

        params = {
            'from': start_time_gmt,
            'to': end_time_gmt
        }
        print(f"Request params: {params}")

        search_file_url = recording_url + "devices/" + ip + "-" + name + "/search_files"
        
        if not check_modules_status():
            return None, 500
            
        response = requests.get(search_file_url, headers=header, params=params)
        response.raise_for_status()

        data = response.json()
        print(f"Response data from API: {data}")  

        return data, response.status_code

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}, response.status_code  
    except Exception as err:
        return {"error": f"An error occurred: {err}"}, 500  
    

def make_time_gmt(start_time , end_time):

    if not start_time and end_time :
        return "error: Start time or end time is missing" , 400
    
    input_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    start_datetime = datetime.strptime(start_time, input_format)
    end_datetime = datetime.strptime(end_time, input_format)

    local_tz =  timezone('Asia/Tehran')

    start_datetime_local  = local_tz.localize(start_datetime)
    end_datetime_local = local_tz.localize(end_datetime)

    # Convert to UTC
    start_datetime_utc = start_datetime_local.astimezone(pytz.utc)
    end_datetime_utc = end_datetime_local.astimezone(pytz.utc)

    start_time_iso = start_datetime_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3]
    end_time_iso = end_datetime_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] 


    return start_time_iso , end_time_iso


