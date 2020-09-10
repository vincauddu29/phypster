from Tests.Mocks.PresentMock import PresentMock
from src.Mappeurs.PresentMappeur import PresentMappeur
from src.DTOs.PresentDTO import PresentDTO
from src.Repositories.PresentRepository import PresentRepository
from src.Repositories.ChildRepository import ChildRepository
from Tests.Mocks.ChildMock import ChildMock
from src.Mappeurs.ChildMappeur import ChildMappeur
from src.DTOs.ChildDTO import ChildDTO
from src import app

mock = PresentMock()
entity = mock.createEntityWithRelationship()
repository = PresentRepository()
mappeur = PresentMappeur()

child_mock = ChildMock()
child_entity = mock.createEntityWithRelationship()
child_repository = ChildRepository()
child_mappeur = ChildMappeur()


dto = mappeur.toDTO(entity)
dto['id'] = None

# with app.app_context() as ctx:
with app.test_client() as c:
    with app.app_context() as ctx:
        child_repository.save(child_entity)
    rv = c.post('/Present', json=dto)
    json_data = rv.get_json()
    assert rv.status_code == 201
    assert json_data['id'] != None
    assert dto['name'] == json_data['name']