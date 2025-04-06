from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
import uvicorn
from typing import Dict, Any
import shutil
import json
from yolo_ocr import MyModel

# 创建FastAPI应用
app = FastAPI(title="图像识别API", description="使用YOLO和PaddleOCR进行图像识别和文字提取")

@app.post("/predict/", response_model=Dict[str, Any])
async def predict_image(file: UploadFile = File(...)):
    # 验证文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只接受图片文件")
    
    # 创建临时文件保存上传的图片
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # 保存上传的文件
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 使用模型处理图片
        model = MyModel(temp_file_path)
        result = model.return_result()
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理图片时出错: {str(e)}")
    
    finally:
        # 清理临时文件
        shutil.rmtree(temp_dir)

@app.get("/")
async def root():
    """API状态检查"""
    return {"status": "运行中", "message": "图像识别API服务正常运行"}

if __name__ == "__main__":
    # 启动服务器
    uvicorn.run(app, host="0.0.0.0", port=8000)