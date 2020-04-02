from app.tests.forms import FakeForm


class FakePracticeCentersForm(FakeForm):

    def __init__(self, all=None, name=None, email=None, web_site=None, phone_number=None):
        self.all = self.empty_or_data(all)
        self.name = self.empty_or_data(name)
        self.email = self.empty_or_data(email)
        self.web_site = self.empty_or_data(web_site)
        self.phone_number = self.empty_or_data(phone_number)
