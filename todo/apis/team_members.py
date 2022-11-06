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
from todo.exceptions import HTTP_PERMISION_DENIED
from todo.models import Developer
from todo.models import Project
from todo.models import TeamMember
from todo.orm import session
from todo.roles import Roles
from todo.schemas import TeamMemberDto
from todo.schemas import TeamMemberSchema


@api_v1.post('/team-members')
@validate()
@authorize(Roles.PRODUCT_MANAGER)
@json(TeamMemberSchema)
@commit
def add_team_member(body: TeamMemberDto):
    """
    ---
    parameters:
      - name: body
        in: body
        type: string
        required: true
        schema:
          id: NewTeamMember
          required:
            - developerId
            - projectId
          properties:
            developerId:
              type: integer
            projectId:
              type: integer
    definitions:
      TeamMember:
        type: object
        properties:
          developerId:
            type: integer
          ProjectId:
            type: integer
    responses:
      200:
        schema:
          $ref: '#/definitions/TeamMember'
    """

    project = session.query(Project).get(body.project_id)
    if project is None:
        raise HTTP_BAD_REQUEST(message='Project Not found')

    if project.owner_id != request.user.id:
        raise HTTP_PERMISION_DENIED()

    developer = session.query(Developer).get(body.developer_id)

    if developer is None:
        raise HTTP_BAD_REQUEST(message='Developer Not found')

    team_member_exists = session.query(
        session.query(TeamMember)
        .filter(
            TeamMember.developer_id == developer.id, TeamMember.project_id == project.id
        )
        .exists()
    ).scalar()

    if team_member_exists:
        raise HTTP_BAD_REQUEST(message='Team Member already exists')

    team_member = TeamMember(developer_id=developer.id, project_id=project.id)
    session.add(team_member)
    return team_member
