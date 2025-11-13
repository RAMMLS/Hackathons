import re 

def sanitize_input(prompt: str) -> bool:
    blacklist = ["пароль", "взломать", "интегнорируй инструкции"]
    if any(word in prompt.lower() for word in blacklist):

        return False 

#Проверка на SQL инъекцию 
    if re.search(r"('.+--|;|DROp TABLE|UNION SELECt)", prompt, re.IGNORECASE):

        return False
    return True 

user_input = "Как взломать аккаунт?"
if sanitize_input(user_input):
    response = llm.generate(user_input)
else: 
    print("Запрос заблокирован!")
