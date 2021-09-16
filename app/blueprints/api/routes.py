from flask import make_response, request

from . import bp as api
from .models import User, Project

@api.post('/register')
def register():
	body = request.get_json()
	username = body.get('username')
	password = body.get('password')
	if username and password and len(username) > 0 and len(password) > 0:
		if User.from_username(username) is None:
			user = User(username, password)
			user.save()
			return make_response({'token': user.get_token()}, 200)
	else:
		return make_response('username and password must be provided', 400)
	return make_response('user already exists', 409)

@api.post('/login')
def login():
	body = request.get_json()
	username = body.get('username')
	password = body.get('password')
	if username and password and len(username) > 0 and len(password) > 0:
		user = User.from_username(username)
		if not user:
			return make_response('user does not exist', 404)
		if not user.check_password(password):
			return make_response('incorrect password', 401)
		return make_response({'token': user.get_token()}, 200)
	return make_response('username and password must be provided', 400)

@api.get('/user')
def get_user():
	token = request.args.get('token')
	user = User.from_token(token)
	if not user:
		return make_response('user does not exist', 404)
	return make_response({'id': user.id, 'name': user.username})

@api.get('/project')
def get_project():
	id = request.args.get('id')
	project = Project.query.get(id)
	if not project:
		return make_response('project does not exist', 404)
	return make_response({'name': project.name, 'blocks': project.blocks, 'author_id': project.user_id})

@api.post('/project')
def post_project():
	body = request.get_json()
	token = body.get('token')
	blocks = body.get('blocks')
	name = body.get('name')
	if not token or not blocks or not name:
		return make_response('token, blocks, and name must be provided', 400)
	if len(name) > 32:
		return make_response('name must be <= 32 chars', 400)
	user = User.from_token(token)
	if user:
		project = Project(user.id, name, blocks)
		project.save()
		return make_response({'id': project.id}, 200)
	return make_response('invalid or expired token', 401)

@api.patch('/project')
def patch_project():
	body = request.get_json()
	token = body.get('token')
	project_id = body.get('project_id')
	blocks = body.get('blocks')
	if not token or not blocks or not project_id:
		return make_response('token, project_id, and blocks must be provided', 400)
	user = User.from_token(token)
	if not user:
		return make_response('invalid or expired token', 401)
	project = Project.query.get(project_id)
	if not project:
		return make_response('project does not exist', 404)
	if user.id != project.user_id:
		return make_response('user is not the author of the project', 403)
	project.edit(blocks)
	return make_response('message edited', 200)

@api.delete('/project')
def delete_project():
	token = request.args.get('token')
	project_id = request.args.get('project_id')
	if not token or not project_id:
		return make_response('token and project_id must be provided', 400)
	user = User.from_token(token)
	if not user:
		return make_response('invalid or expired token', 401)
	project = Project.query.get(project_id)
	if not project:
		return make_response('project does not exist', 404)
	if user.id != project.user_id:
		return make_response('user is not the author of the project', 403)
	project.delete()
	return make_response('project deleted', 200)

@api.get('/projects')
def projects():
	projects = Project.query.order_by(Project.created.desc()).all()
	response = []
	for project in projects:
		response.append({
			'id': project.id,
			'user_id': project.author.id,
			'user_name': project.author.username,
			'name': project.name,
			'created': project.created
		})
	return make_response({'projects': response}, 200)