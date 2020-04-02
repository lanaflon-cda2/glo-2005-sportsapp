from app.tests.forms import FakeForm


class FakeUsersForm(FakeForm):

    def __init__(self, all=None, username=None, email=None, first_name=None, last_name=None, phone_number=None):
        self.all = self.empty_or_data(all)
        self.username = self.empty_or_data(username)
        self.email = self.empty_or_data(email)
        self.first_name = self.empty_or_data(first_name)
        self.last_name = self.empty_or_data(last_name)
        self.phone_number = self.empty_or_data(phone_number)
