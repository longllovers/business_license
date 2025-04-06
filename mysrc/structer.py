import requests
import json

def mymodel(prompt):
    url = 'http://localhost:11434/api/generate'
    header = {
        'Content-Type': 'application/json'
    }
    data = {
        'model': "qwen2.5",
        'prompt': prompt,
        'parameters': {
            "max_tokens": 100,  # Fixed key name from "max_token" to "max_tokens"
            "temperature": 0.2,
        },
        "stream": False
    }
    res = requests.post(url, headers=header, data=json.dumps(data))
    return json.loads(res.text)['response']

if __name__ == "__main__":  # Fixed comparison (was using assignment operator)
    text = '  "经营范围": "许可经营项目：无一般经营项目：制造销售消防器材：销售五金、化工（不含化学危险品）、汽摩配件、建筑装饰材料（不含化学危险品）；消防设施工程专业承包壹级、安全技术防范工程设计、施工，消防设施专项工程设计（乙级），机电设备安装工程专业承包（叁级），建筑装修装饰工程专业承包（叁级）、【以上范围法律、法规禁止经营的不得经营：法律、法规规定应经审批而未获审批前不得经营！★★",'
    prompt = f"请还原下面的语义和排版,只需要微调,只有个别的排版问题:{text}"
    res = mymodel(prompt)
    print(res)