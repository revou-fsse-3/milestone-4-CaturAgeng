from unittest import TestProgram
import pytest
from resources.user import Animals, Animal
from resources.account import Employees, Employee
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from resources.user import AnimalModel



@pytest.fixture
def data_animal():
    animal = {
        "species": "Mamalia",
        "age": 2,
        "gender": "Male"
    }
    yield animal

@pytest.fixture
def data_employee():
    employee = {
        "name": "Amanda",
        "role": "CEO",
        "schedule": "Monday"
    }
    yield employee

# POST /animals
def test_post_animals(test_app, data_animal):
    with test_app.test_request_context(json=data_animal):
        response = Animals.post(data_animal)
        assert response.status_code == 200
        assert response.get_json() == {
            'id': 1,
            **data_animal
        }

# POST /employees
def test_post_employees(test_app, data_employee):
    with test_app.test_request_context(json=data_employee):
        response = Employees.post(data_employee)
        assert response.status_code == 200
        assert response.get_json() == {
            'id': 1,
            **data_employee
        }

# GET /animals
def test_get_animals_empty(test_app):
    with test_app.test_request_context():
        response = Animals.get(None)
        assert response.status_code == 200
        assert response.get_json() == []

# def test_get_animals(test_app, data_animal):
#     with test_app.test_request_context(json=data_animal):
#         Animals.post(None)
#         response = Animal.get(None)
#         assert response.status_code == 200
#         assert len(response.get_json()) == 1

# GET /employees
def test_get_employees_empty(test_app):
    with test_app.test_request_context():
        response = Employees.get(None)
        assert response.status_code == 200
        assert response.get_json() == []

# def test_get_employees(test_app, data_employee):
#     with test_app.test_request_context(json=data_employee):
#         Employees.post(None)
#         response = Employee.get(None)
#         assert response.status_code == 200
#         assert len(response.get_json()) == 1

# GET /animals/{animal_id}
def test_get_animal(test_app, data_animal):
    with test_app.test_request_context(json=data_animal):
        Animals.post(None)
        response = Animal.get(self=None, animal_id=1)
        assert response.status_code == 200
        assert response.get_json() == {
            'id': 1,
            **data_animal
        }

def test_get_animal_not_found(test_app):
    with test_app.test_request_context():
        with pytest.raises(NotFound):
            Animal.get(self=None, animal_id=1)

# # GET /employees/{employee_id}
# def test_get_employee(test_app, data_employee):
#     with test_app.test_request_context(json=data_employee):
#         Employees.post(None)
#         response = Employee.get(self=None, animal_id=1)
#         assert response.status_code == 200
#         assert response.get_json() == {
#             'id': 1,
#             **data_employee
#         }

# def test_get_employee_not_found(test_app):
#     with test_app.test_request_context():
#         with pytest.raises(NotFound):
#             Employee.get(self=None, employee_id=1)

# DELETE /animals{animal_id}
def test_delete_animal(test_app, data_animal):
    with test_app.test_request_context(json=data_animal):
        Animals.post(None)
        response = Animal.delete(self= None, animal_id=1)
        assert response == {"message": "Animal deleted"}

def test_delete_animal_not_found(test_app):
    with test_app.test_request_context():
        with pytest.raises(NotFound):
            Animal.delete(self=None, animal_id=1)

# DELETE /employees{employee_id}
def test_delete_employee(test_app, data_employee):
    with test_app.test_request_context(json=data_employee):
        Employees.post(None)
        response = Employee.delete(self= None, Employee_id=1)
        assert response == {"message": "Employee deleted"}

def test_delete_employee_not_found(test_app):
    with test_app.test_request_context():
        with pytest.raises(NotFound):
            Employee.delete(self=None, Employee_id=1)


# # PUT /animals{animal_id}
# def test_put_animal(test_app, data_animal):
#     with test_app.test_request_context(json=data_animal):
#         Animals.post(None)
#         response = Animal.put(data_animal={
#             **data_animal,
#             "gender": "female",
#         }, animal_id=1)

#         assert response.status_code == 200
#         assert response.get_json() == {
#             'id': 1,
#             **data_animal,
#             "gender": "female"
#         }

def test_put_animal_not_found(test_app, data_animal):
    with test_app.test_request_context(json=data_animal):
        with pytest.raises(NotFound):
            Animal.put(data_animal, animal_id=1)

# def test_put_animals_integrity_error(test_app, data_animal):
#     animal_2 = {
#         "species": "burung",
#         "age": 3,
#         "gender": "Male"
#     }
#     with test_app.test_request_context(json=data_animal):
#         Animals.post(data_animal)
#     with test_app.test_request_context(json=animal_2):
#         with pytest.raises(BadRequest):
#             Animals.post(animal_2)
#             Animal.put(animal_2, animal_id=1)

# # PUT /employees{animal_id}
# def test_put_employee(test_app, data_employee):
#     with test_app.test_request_context(json=data_employee):
#         Employees.post(None)
#         response = Employees.put(data_employee={
#             **data_employee,
#             "name": "iman",
#         }, employee_id=1)

#         assert response.status_code == 200
#         assert response.get_json() == {
#             'id': 1,
#             **data_employee,
#             "name": "Iman"
#         }

# def test_put_employee_not_found(test_app, data_employee):
#     with test_app.test_request_context(json=data_employee):
#         with pytest.raises(NotFound):
#             Employee.put(data_employee, employee_id=1)

# def test_put_employees_integrity_error(test_app, data_employee):
#     employee_2 = {
#         "name": "Iman",
#         "role": "CEO",
#         "schedule": "Monday"
#     }
#     with test_app.test_request_context(json=data_employee):
#         Animals.post(data_employee)
#     with test_app.test_request_context(json=employee_2):
#         with pytest.raises(BadRequest):
#             Animals.post(employee_2)
#             Animal.put(employee_2, employee_id=1)

# # animals
# @TestProgram('resources.animal.AnimalModel')
# def test_put_animals_sql_error(mock_AnimalModel, test_app, data_animal):
#     with test_app.test_request_context(json=data_animal):
#         mock_AnimalModel.side_effect = SQLAlchemyError
#         with pytest.raises(InternalServerError):
#             Animals.post(data_animal)
#             Animal.put(data_animal, animal_id=1)

# # employees
# @TestProgram('resources.employee.Employees')
# def test_put_employees_sql_error(mock_Employees, test_app, data_employee):
#     with test_app.test_request_context(json=data_employee):
#         mock_Employees.side_effect = SQLAlchemyError
#         with pytest.raises(InternalServerError):
#             Employees.post(data_employee)
#             Employee.put(data_employee, employee_id=1)