import re

class Parser:
    
    @staticmethod
    def date(text:str) -> str:
        _ , _date , _time = text.split('،')
        year = re.findall(r'(\d{4})',_date)[0]
        day = re.findall(r'(\d{1,2} )',_date)[0]
        months = {
            'فروردین': 1,
            'اردیبهشت': 2,
            'خرداد': 3,
            'تیر':4,
            'مرداد':5,
            'شهریور':6,
            'مهر':7,
            'آبان':8,
            'آذر':9,
            'دی':10,
            'بهمن':11,
            'اسفند':12,
        }
        for key,value in months.items():
            if key in _date:
                month = value
                break
        date = f'{year}-{month}-{day}'.strip()
        time = re.findall(r'(\d{1,2}:\d{1,2})',_time)[0]
        if 'عصر' in _time:
            hours , minutes = time.split(':')
            hours = int(hours) + 12
            time = f'{hours}:{minutes}'

        return f'{date}|{time}'

    @staticmethod
    def remaining(text:str) -> str:
        return text.replace(' روز','d').replace(' ساعت','h').replace(' دقیقه','m')
