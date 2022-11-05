# Todo Project

## Routes

- Login: `/api/v1/login`
- Developer Signup: `/api/v1/signup/developer`
- Project Manager Signup: `/api/v1/signup/project-manager`
- Projects (Create and List): `/api/v1/projects`
- Tasks (Create and List): `/api/v1/tasks`
- Assign a task: `/api/v1/tasks/:id/assign`
- Assign a project: `/api/v1/tasks/:id/assign`

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
- created_at
- updated_at

### TaskAssignment

- id
- project_id
- developer_id
- created_at
- updated_at

### ProjectAssignment

- id
- project_id
- developer_id
- created_at
- updated_at
