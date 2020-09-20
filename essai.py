# from Tests.Mocks.JobMock import JobMock
# from src.Mappeurs.JobMappeur import JobMappeur
# from src.DTOs.JobDTO import JobDTO
# from src.Repositories.JobRepository import JobRepository
# from src.Repositories.ChildRepository import ChildRepository
# from Tests.Mocks.ChildMock import ChildMock
# from src.Mappeurs.ChildMappeur import ChildMappeur
# from src.DTOs.ChildDTO import ChildDTO


# mock = JobMock()
# entity = mock.createEntityWithRelationship()
# repository = JobRepository()
# mappeur = JobMappeur()

# # child_mock = ChildMock()
# # child_entity = child_mock.createEntityWithRelationship(Job=entity)
# # child_repository = ChildRepository()
# # child_mappeur = ChildMappeur()


# dto = mappeur.toDTO(entity)
# print("before : ", dto)
# # print(child_mappeur.toDTO(child_entity))

# with app.app_context() as ctx:
#     res = repository.save(entity)

#     print("after : ", mappeur.toDTO(res))
# # with app.test_client() as c:
# #     with app.app_context() as ctx:
# #         child_repository.save(child_entity)
# #     rv = c.post('/Job', json=dto)
# #     json_data = rv.get_json()
# #     assert rv.status_code == 201
# #     assert json_data['id'] != None
# #     assert dto['name'] == json_data['name']

from Tests.Repositories.test_PresentRepositoryTest import PresentRepositoryTest
from src import app, db
test = PresentRepositoryTest()

test.setUp()

with app.app_context():
    db.session.expire_on_commit = False
    test.test_save_with_relationship_check_auto_increment_id()