# config.py
PROXY_LIST = [
    'http://proxy1.ua:8080',
    'http://proxy2.ua:8080', 
    'http://proxy3.ua:8080'
]

UA_CARRIERS = {
    'kyivstar': ['67', '68', '96', '97', '98'],
    'vodafone': ['50', '66', '95', '99'], 
    'lifecell': ['63', '73', '93'],
    '3mob': ['91'],
    'people.net': ['92'],
    'intertelecom': ['89', '94']
}

SMS_TEMPLATES = [
    "Код підтвердження: {code}",
    "Ваш верифікаційний код: {code}",
    "Пароль для входу: {code}",
    "Код активації послуги: {code}",
    "Підтвердіть номер: {code}"
]
