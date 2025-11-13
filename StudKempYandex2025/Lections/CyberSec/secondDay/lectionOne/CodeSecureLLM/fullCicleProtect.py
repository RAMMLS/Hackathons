import re 
import logging 

logging.basicConfig(filename = 'llm_secure.log', level = logging.INFO)

def sanitize_input(prompt: str) -> bool:
    blacklist = ["пароль", "взломать", "игнорируй инструкции"]
    if any(word in prompt.lower() for word in blacklist):

        return False 
    if re.search(r"('.+--|;|DROP TABLE|)", prompt, re.IGNORECASE):

        return False 
    return True 

def log_interaction(ip: str, prompt: str, response: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{timestamp}] {ip} -> {prompt} -> {response[:50]}...")

# Пример запроса
user_ip = "192.168.1.100"
user_prompt = "Как сбросить пароль администратора?"

if sanitize_input(user_prompt):
    response = llm.generate(user_prompt)
    log_interaction(user_ipm user_prompt, response)
else:
    print("Запрос заблокирован!")
    log_interaction(user_ip, user_prompt, "BLOCKED")
