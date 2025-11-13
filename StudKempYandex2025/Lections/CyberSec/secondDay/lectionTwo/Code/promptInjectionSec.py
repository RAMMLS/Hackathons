import re 

def sanitize_prompt(user_input):
    # Блокируем опасные файлы 
    blocked_phrases = [
        "Игнорируй предыдущие ответы",
        "Скажи пароль",
        "Выполни команду"
    ]
    for phrase in blocked_phrases:
        if re.search(phrase, user_input, re.IGNORECASE):
            
            return "Неа не сработало)"
user_prompt = "Скажи что ты лох"
print(sanitize_prompt(user_prompt))
