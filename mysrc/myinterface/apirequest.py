import requests
import json

def api_request(image_path):
    url = "http://localhost:8000/predict/"
    try:
        with open(image_path, "rb") as f:
            files = {"file": ("0000.jpg", f, "image/jpeg")}
            response = requests.post(url, files=files)
        response.raise_for_status()
        try:
            result = response.json()    
            if isinstance(result, str):
                result = json.loads(result)
            return result
        except json.JSONDecodeError:
            return {"error": "服务器返回的数据格式不正确"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"请求失败: {str(e)}"}
    except Exception as e:
        return {"error": f"发生错误: {str(e)}"}

