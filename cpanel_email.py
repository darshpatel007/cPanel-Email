import requests
import json

class CPanelLib:
    def __init__(self, domain: str,cpanel_username,cpanel_password):
        self.session = requests.Session()
        self.domain = domain
        self.cpanel_username = cpanel_username
        self.cpanel_password = cpanel_password

    def send_auth(self, user, password):
        r = self.session.post(f'{self.domain}login/?login_only=1',
                              data={'user': user, 'pass': password, 'goto_uri': '/'})
        return r

    @staticmethod
    def save_accounts(content: str):
        with open('accounts.txt', 'a+') as f:
            f.write(content)

    def create_email(self, save: bool, email_domain: str, email: str, password: str, amount: int):
        '''
        https://documentation.cpanel.net/display/DD/UAPI+Functions+-+Email%3A%3Aadd_pop
        '''
        for _ in range(amount):
            data = {
                'email': email,
                'domain': email_domain,
                'password': password,
                'send_welcome_email': 1,
                'quota': 0 # recommended according to docs
            }
            auth = self.send_auth(self.cpanel_username,self.cpanel_password)
            # print(auth)
            auth_json = auth.json()['security_token']
            # print(auth.json())
            auth_headers = auth.headers
            r = self.session.post(f'{self.domain}{auth_json}/execute/Email/add_pop',
                                  data=data, headers=auth_headers)
            if '"errors":null' in r.text:
                if save:
                    self.save_accounts(f'Created: {email}@{email_domain}:{password}')
                return f'Created Account => {email}@{email_domain} : {password}'
            else:
                for i in r.json()['errors'] :
                    print("ERROR =>",i)
                return f'Could Not Create Account => {email}@{email_domain} : {password}'


if __name__ == '__main__':
    URL = 'https://darshpatel.codes:2083/'
    CPANEL_USERNAME = "darshpat"
    CPANEL_PASSWORD = "dc19_220402"
    
    EMAIL_DOMAIN = 'darshpatel.codes'
    EMAIL_USERNAME = "test3"
    EMAIL_PASSWORD = "Test"
    
    client = CPanelLib(URL,CPANEL_USERNAME,CPANEL_PASSWORD)
    
    created_email = client.create_email(True,EMAIL_DOMAIN,EMAIL_USERNAME,EMAIL_PASSWORD, 1)
    print(created_email)