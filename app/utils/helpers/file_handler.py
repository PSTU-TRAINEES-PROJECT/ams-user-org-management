import base64
import os

def save_base64_file(base64_string: str, file_name: str, folder_path: str = "upload/user_documents/") -> str:
    try:
        os.makedirs(folder_path, exist_ok=True)
        
        file_content = base64.b64decode(base64_string)
        
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, "wb") as f:
            f.write(file_content)
            
        return file_name
    except Exception as e:
        raise Exception(f"Error saving file: {str(e)}") 
    


def get_base64_file(file_name: str, folder_path: str = "upload/user_documents/") -> dict:
    try:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "rb") as file:
            file_content = file.read()
            base64_content = base64.b64encode(file_content).decode('utf-8')
            
        return {
            "file_name": file_name,
            "file_base64": base64_content
        }
    except Exception as e:
        print(f"Error reading file {file_name}: {str(e)}")
        return {
            "file_name": file_name,
            "file_base64": ""
        }