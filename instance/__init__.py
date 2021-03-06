from instance.creation.services import CreationService
from instance.population.services import PopulationService


class Instance:
    injector = None

    def db_create(self):
        creation_service = self.injector.get(CreationService)
        creation_service.db_create()

    def db_populate(self):
        population_service = self.injector.get(PopulationService)
        population_service.db_populate()


instance = Instance()
