import loging 
from datetime import datetime 

logging.basicConfig(filename = 'llm_audit.log', level = logging.INFO)

def log_request (user_ip: str, prompt: str, response: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{timestamp}] IP: {user_ip} | Prompt: {prompt} | Response: {response[:100]}...")

# Пример использования
log_request("192.168.1.1", "Как взломать wifi?", "Извините, я не могу помочь с этим")
