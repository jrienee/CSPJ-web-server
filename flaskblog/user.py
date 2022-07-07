class User:
    def __init__(self, username, birthdate, email, phone, gender, password):
        self.__username = username
        self.__email = email
        self.__phone = phone
        self.__birthdate = birthdate
        self.__gender = gender
        self.__password = password
        # self.set_password(password, cfm_password)
        # self.set_nric(nric)
        # self.set_phone(phone)

    def set_username(self, username):
        self.__username = username

    def get_username(self):
        return self.__username

    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate

    def get_birthdate(self):
        return self.__birthdate

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_phone(self, phone):
        self.__phone = phone

    def get_phone(self):
        return self.__phone

    def set_gender(self, gender):
        self.__gender = gender

    def get_gender(self):
        return self.__gender

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password
