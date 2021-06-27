from enum import Enum

class Gender(Enum):
    male = 'm'
    female = 'f'

class Industry(Enum):
    horeca = ' HoReCa'
    agriculture = 'Agriculture'
    banks = 'Banks'
    consult = 'Consult'
    it = 'IT'

class Profession(Enum):
    accounting = 'Accounting'
    bussiness_development = 'BusinessDevelopment'
    commercial = 'Commercial'
    consult = 'Consult'
    engineer = 'Engineer'
    fianne = 'Finanñe'
    hr = 'HR'
    it = 'IT'
    law = 'Law'
    marketing = 'Marketing'
    pr = 'PR'
    sales = 'Sales'
    teaching = 'Teaching'
    etc = 'etc'
    manage = 'manage'

class Traffic(Enum):
    ka = 'KA'
    advert = 'advert'
    empjs = 'empjs'
    friends = 'friends'
    rabrecnerab = 'rabrecNErab'
    recnerab = 'recNErab'
    referal = 'referal'
    youjs = 'youjs'

class Coach(Enum):
    no = 'no'
    my_head = 'my head'
    yes = 'yes'

class GreyWage(Enum):
    white = 'white'
    grey = 'grey'

class Way(Enum):
    bus = 'bus'
    car = 'car'
    foot = 'foot'

    
class Employee():
    def __init__(self, email: str, firstname: str, lastname: str, gender: str, age: float, industry: str, profession: str, traffic: str, coach: str, head_gender: str, greywage: str, way: str, extraversion: float, independ: float, selfcontrol: float, anxiety: float, novator: float):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age
        self.industry = industry
        self.profession = profession
        self.traffic = traffic
        self.coach = coach
        self.head_gender = head_gender
        self.greywage = greywage
        self.way = way
        self.extraversion = extraversion
        self.independ = independ
        self.selfcontrol = selfcontrol
        self.anxiety = anxiety
        self.novator = novator

    def __repr__(self):
        return str(self.get_json())

    def get_json(self):
        return {
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'gender': self.gender,
            'age': self.age,
            'industry': self.industry,
            'profession': self.profession,
            'traffic': self.traffic,
            'coach': self.coach,
            'head_gender': self.head_gender,
            'greywage': self.greywage,
            'way': self.way,
            'extraversion': self.extraversion,
            'independ': self.independ,
            'selfcontrol': self.selfcontrol,
            'anxiety': self.anxiety,
            'novator': self.novator
        }