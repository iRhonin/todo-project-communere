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
from todo.models import TeamMember
from todo.orm import session
from todo.roles import Roles
from todo.schemas import AssignTaskDto
from todo.schemas import TaskDto
from todo.schemas import TaskSchema


@api_v1.post('/tasks')
@validate()
@authorize(Roles.PRODUCT_MANAGER, Roles.DEVELOPER)
@json(TaskSchema)
@commit
def add_task(body: TaskDto):
    """
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: body
        in: body
        type: string
        required: true
        schema:
          id: NewTask
          required:
            - name
            - projectId
          properties:
            name:
              type: string
            projectId:
              type: string
    definitions:
      Task:
        type: object
        properties:
          id:
            type: integer
          name:
            type: string
          projectId:
            type: integer
          developers:
            type: array
            items:
              $ref: '#definitions/User'
    responses:
      200:
        schema:
          $ref: '#/definitions/Task'
    """
    project = session.query(Project).get(body.project_id)
    if project is None:
        raise HTTP_BAD_REQUEST(message='Project Not Found')

    task = Task(name=body.name, project_id=project.id)

    if request.user.type == Roles.DEVELOPER:
        # Can be optimized
        if request.user not in project.team_members:
            raise HTTP_PERMISION_DENIED()

        task.developers.append(request.user)

    elif request.user.type == Roles.PRODUCT_MANAGER:
        if project.owner != request.user:
            raise HTTP_PERMISION_DENIED()
    else:
        raise HTTP_PERMISION_DENIED()

    session.add(task)
    return task


@api_v1.post('/tasks/<id>/assign')
@validate()
@authorize(Roles.PRODUCT_MANAGER, Roles.DEVELOPER)
@json(TaskSchema)
@commit
def assign_task(body: AssignTaskDto, id: int):
    """
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: body
        in: body
        type: string
        required: true
        schema:
          id: AssignTaskBody
          required:
            - developerId
          properties:
            developerId:
              type: integer
      - name: id
        in: path
        type: string
        required: true
        schema:
          id: AssignTaskPath
          required:
            - taskId
          properties:
            taskId:
              type: integer
    definitions:
      Task:
        type: object
        properties:
          id:
            type: integer
          name:
            type: string
          projectId:
            type: integer
          developers:
            type: array
            items:
              $ref: '#definitions/User'
    responses:
      200:
        schema:
          $ref: '#/definitions/Task'
    """
    task = session.query(Task).get(id)
    if task is None:
        raise HTTP_NOT_FOUND()

    developer = session.query(Developer).get(body.developer_id)
    if developer is None:
        raise HTTP_BAD_REQUEST('Developer Not Found')

    if developer in task.developers:
        raise HTTP_BAD_REQUEST(message='Already Assigned')

    if request.user.type == Roles.DEVELOPER:
        # Can be optimized
        if request.user not in task.project.team_members:
            raise HTTP_PERMISION_DENIED()

    elif request.user.type == Roles.PRODUCT_MANAGER:
        if task.project.owner != request.user:
            raise HTTP_PERMISION_DENIED()

    else:
        raise HTTP_PERMISION_DENIED()

    task.developers.append(developer)
    return task
