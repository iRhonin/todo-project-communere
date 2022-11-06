# Todo Project

## Run Server

```bash
docker-compose up -d
```

_Server will be up on `http://0.0.0.0:4321`_

_Documents: `http://0.0.0.0:4321/apidocs`_

## Run Tests

```bash
docker-compose run backend pytest -vvv
```

## Routes

- Login: `/api/v1/login`
- Developer Signup: `/api/v1/signup/developer`
- Project Manager Signup: `/api/v1/signup/project-manager`
- Projects (Create and List): `/api/v1/projects`
- Tasks (Create and List): `/api/v1/tasks`
- Assign a task: `/api/v1/tasks/:id/assign`
- Add a developer to project: `/api/v1/team-members`

## Entities

### User

- id
- username
- \_password
- type
- created_at
- updated_at

### Project

- id
- name
- owner_id
- created_at
- updated_at

### Task

- id
- name
- project_id
- created_at
- updated_at

### TaskDeveloper

- task_id
- developer_id
- created_at
- updated_at

### TeamMembers

- project_id
- developer_id
- created_at
- updated_at
