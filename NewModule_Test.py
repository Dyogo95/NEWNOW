
import pandas as pd
import re
from get_TMs import get_TM_names_list as gtm


class GetResponse():
    def __init__(self, topic, date, gender, name, subject_topic,
                 case, PZ, sender):
        self.topic = topic
        self.date = date
        self.gender = gender
        self.name = name
        self.subject_topic = subject_topic
        self.case = case
        self.PZ = PZ
        self.sender = sender

    def get_PZ_info(self, PZ, language):
        # Email info from PZ excel
        PZ_list = pd.read_excel(r"E-Mail_Porsche_Zentren.xlsx")
        df = pd.DataFrame(PZ_list)
        # Info from PZ Excel
        location = []
        self.PZ_stadt = self.PZ[2:]
        for index, row in df.iterrows():
            if PZ == row[1]:
                street = row['Strasse']
                plz = str(f"{row['PLZ']} ")
                ort = row['Ort']
                location = str(plz) + str(ort)
                tel = row['PZ-Tel']
                tel = re.sub('^[0]', '+49 ', tel)
                tel = re.sub('[/&-]', '', tel)
                email_address = row['E-mails']
                info = "{}\n\n{}\n\n{}\n\nTel:    {}\n\nE-Mail: {}".format(
                        self.PZ, street, location, tel, email_address)
                if self.language == "en":
                    PZ_info = re.sub(r"Zentrum", "Centre", info)
                    PZ_info = re.sub(r"Straße", "Street", PZ_info)
                    PZ_info = re.sub(r"Ort", "City", PZ_info)
                    PZ_info = re.sub(r"Telefonnummer", "Phonenumber", PZ_info)
                    info = PZ_info

                return info

    def get_module(self, topic):
        # Get's only the needed text module for the e-mail
        modules = ''
        with open('New_TM.txt') as f:
            # Read the file fully and as string. Name it TM
            TM = f.read()
            # Split TM by "----------" to seperate each module
            modules = TM.split("----------")
        for module in modules:
            if self.topic in module:
                self.mail = module
        return self.mail

    def response(self):
        mail = str(self.get_module(self.topic))
        self.gname = ""
        self.language = ""
        Subj = f"Ihre Anfrage {self.subject_topic} vom {self.date} ({self.case})"
        PZ_info = self.get_PZ_info(self.PZ, self.language)
        # Recognize the language to specify the greeting
        if "Sehr" in mail:
            self.language = "de"
        elif "Dear" in mail:
            self.language = "en"
        # Match the greeting to the correct gender in the right language
        if self.gender == "m" and self.language == "de":
            self.gname = f"r Herr {self.name}"
        elif self.gender == "f" and self.language == "de":
            self.gname = f" Frau {self.name}"
        elif self.gender == "m" and self.language == "en":
            self.gname = f". {self.name}"
            Subj = f"Your request regarding {self.subject_topic} dated {self.date} ({self.case})"
        elif self.gender == "f" and self.language == "en":
            self.gname = f". {self.name}"
            Subj = f"Your request regarding {self.subject_topic} dated {self.date} ({self.case})"
        # replacing the variables in the needed module
        mail = mail.format(name=self.gname,
                           date=self.date,
                           subject_topic=self.subject_topic,
                           PZ_info=PZ_info,
                           PZ_stadt=self.PZ_stadt,
                           sender=self.sender)
        '''else:
            mail = self.mail.format(name=self.gname, date=self.date,
                                         subject_topic=self.subject_topic)'''

        # mail = self.mail.replace(f"{self.topic}", f"{Subj}")
        mail = mail.replace(f"{self.topic}", f"{Subj}")
        # print(mail)
        return mail

# PZ_info = GetResponse.get_PZ_info('Porsche Zentrum Berlin')
# topic, date, gender, name, subject_topic, case, PZ, sender


def main():
    '''gettit = GetResponse(topic="TM - Bewerbung",
                         date="12. Mai 2021", gender="m",
                         name="Hilal Sharifi", subject_topic="zur Bewerbung",
                         case="63426932",
                         PZ="Porsche Zentrum Braunschweig",
                         sender="Dyogo Lorenz")'''
    gettit = GetResponse(topic='', date='', gender='', name='',
                         subject_topic='', case='', PZ="", sender="")
    res = gettit.response()
    print(res)



if __name__ == "__main__":
    main()
