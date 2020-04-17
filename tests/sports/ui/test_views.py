import unittest

from tests.interfaces.ui.test_views import ViewTests
from tests.sports.fakes import sport1, sport3, sport2


class SportsViewsTests(ViewTests):

    def get_path(self):
        return '/sports'

    def get_view_title(self):
        return 'Sports'

    def test_sports_with_no_sport_should_display_no_sport(self):
        self.remove_sports()
        response = self.request_get()
        self.assert_page_is_found(response)
        self.assert_items_are_not_listed(response, [sport1.name, sport2.name, sport3.name])

    def test_sports_with_sports_should_display_sports(self):
        response = self.request_get()
        self.assert_page_is_found(response)
        self.assert_items_are_listed(response, [sport1.name, sport2.name, sport3.name])

    def test_sports_with_form_should_display_filtered_sports(self):
        response = self.request_post()
        self.assert_page_is_found(response)
        self.assert_items_are_listed(response, [sport1.name])
        self.assert_items_are_not_listed(response, [sport2.name, sport3.name])

    def test_sport_details_should_display_sport_details(self):
        self.assert_item_details_are_displayed([
            (sport1.id, self.get_sport_details(sport1)),
            (sport2.id, self.get_sport_details(sport2)),
            (sport3.id, self.get_sport_details(sport3)),
        ])

    def test_sport_details__without_sport_should_respond_not_found(self):
        self.remove_sports()
        self.assert_item_details_are_not_found([(sport1.id, sport1.name)])

    def test_sport_details_should_display_recommendations(self):
        self.assert_item_details_are_displayed([
            (sport1.id, self.get_recommendations_details(sport1)),
            (sport2.id, self.get_recommendations_details(sport2)),
            (sport3.id, self.get_recommendations_details(sport3))
        ])

    @staticmethod
    def get_sport_details(sport):
        return [sport.name] + list(map(lambda climate: climate.name, sport.climates))

    @staticmethod
    def get_recommendations_details(sport):
        details = []
        for recommendation in sport.recommendations:
            details += [recommendation.username]
        return details


if __name__ == "__main__":
    unittest.main()
