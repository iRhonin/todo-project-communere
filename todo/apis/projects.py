from argon2.exceptions import VerifyMismatchError
from flask import jsonify
from flask import request
from flask_pydantic import validate

from todo.app import api_v1
from todo.authorization import authorize
from todo.authorization import create_access_token
from todo.decorators import commit
from todo.decorators import json
from todo.exceptions import HTTP_BAD_REQUEST
from todo.exceptions import HTTP_NOT_FOUND
from todo.exceptions import HTTP_PERMISION_DENIED
from todo.models import Developer
from todo.models import ProductManager
from todo.models import Project
from todo.models import Task
from todo.models import TaskDeveloper
from todo.models import TeamMember
from todo.orm import session
from todo.roles import Roles
from todo.schemas import ListProjectTasksQuery
from todo.schemas import ProjectDto
from todo.schemas import ProjectSchema
from todo.schemas import TaskSchema
from todo.schemas import TeamMemberDto
from todo.schemas import TeamMemberSchema


@api_v1.post('/projects')
@validate()
@authorize(Roles.PRODUCT_MANAGER)
@json(ProjectSchema)
@commit
def add_project(body: ProjectDto):
    """
    ---
    parameters:
      - name: body
        in: body
        type: string
        required: true
        schema:
          id: NewProject
          required:
            - name
          properties:
            name:
              type: string
    definitions:
      Project:
        type: object
        properties:
          id:
            type: integer
          name:
            type: string
          ownerId:
            type: integer
          owner:
            $ref: '#/definitions/User'
    responses:
      200:
        description: Project
        schema:
          $ref: '#/definitions/Project'
    """
    project = Project(name=body.name, owner_id=request.user.id)
    session.add(project)
    return project


@api_v1.get('/projects')
@authorize(Roles.PRODUCT_MANAGER)
@json(ProjectSchema, use_list=True)
def list_projects():
    """
    ---
    responses:
      200:
        schema:
          type: array
          items:
            $ref: '#/definitions/Project'
    """
    projects = session.query(Project)
    return projects


@api_v1.get('/projects/<id>/tasks')
@validate()
@authorize(Roles.PRODUCT_MANAGER, Roles.DEVELOPER)
@json(TaskSchema, use_list=True)
def list_project_tasks(id: int, query: ListProjectTasksQuery):
    """
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: developerId
        in: query
        type: integer
    responses:
      200:
        schema:
          type: array
          items:
            $ref: '#/definitions/Task'
    """
    project = session.query(Project).get(id)
    if project is None:
        raise HTTP_NOT_FOUND()

    if request.user.type == Roles.DEVELOPER and request.user not in project.team_members:
        raise HTTP_PERMISION_DENIED()

    tasks = session.query(Task).filter(Task.project_id == id)

    if query.developer_id is not None:
        tasks = tasks.join(TaskDeveloper, Task.id == TaskDeveloper.task_id).filter(
            TaskDeveloper.developer_id == query.developer_id,
        )

    return tasks
