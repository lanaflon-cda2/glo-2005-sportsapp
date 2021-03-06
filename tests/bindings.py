from app.interfaces.database import Database
from tests.admin.modules import MockAdminModule
from tests.announces.modules import MockAnnounceModule
from tests.equipment_types.modules import MockEquipmentTypeModule
from tests.climates.modules import MockClimateModule
from tests.equipments.modules import MockEquipmentModule
from tests.interfaces.infrastructure.database import test_database
from tests.manufacturers.modules import MockManufacturerModule
from tests.practice_centers.modules import MockPracticeCenterModule
from tests.recommendations.modules import MockRecommendationModule
from tests.shops.modules import MockShopModule
from tests.sports.modules import MockSportModule
from tests.users.modules import MockUserModule


def configure_test_database(binder):
    binder.bind(Database, to=test_database)


def configure_mock_modules(binder):
    binder.install(MockAdminModule)
    binder.install(MockUserModule)
    binder.install(MockClimateModule)
    binder.install(MockShopModule)
    binder.install(MockManufacturerModule)
    binder.install(MockEquipmentTypeModule)
    binder.install(MockEquipmentModule)
    binder.install(MockAnnounceModule)
    binder.install(MockSportModule)
    binder.install(MockPracticeCenterModule)
    binder.install(MockRecommendationModule)
