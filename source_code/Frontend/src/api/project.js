import { post, get} from './api';

export function createProject(name,team_id,introduction){
	var data=new FormData();
	data.append("name",name);
	data.append("team_id",team_id);
	data.append("introduction",introduction);
	return post('/api/project/create/',data);
}

export function deleteProject(project_id){
	var data=new FormData();
	data.append("project_id",project_id);
	return post('/api/project/delete/',data);
}

export function updateProject(project_id,name,introduction){
	var data=new FormData();
	data.append("project_id",project_id);
	data.append("name",name);
	data.append("introduction",introduction);
	return post('/api/project/update/',data);
}

export function restoreProject(project_id){
	var data=new FormData();
	data.append("project_id",project_id);
	return post('/api/project/restore/',data);
}

export function emptyRestore(team_id){
	var data=new FormData();
	data.append("team_id",team_id);
	return post('/api/project/empty/',data);
}

export function removeProject(project_id){
	var data=new FormData();
	data.append("project_id",project_id);
	return post('/api/project/remove/',data);
}

export function copyProject(project_id,name){
	var data=new FormData();
	data.append("project_id",project_id);
	data.append("name",name);
	return post('/api/project/copy/',data);
}

export function changeProjectShare(project_id,is_shared){
	var data=new FormData();
	data.append("project_id",project_id);
	data.append("is_shared",is_shared);
	console.log(project_id+' '+is_shared);
	return post('/api/project/change_role/',data);
}

export function getProjectInformation(project_id){
	return get('/api/project/getinfo/?project_id='+project_id);
}

export function getRestoreList(team_id){
	return get('/api/project/get_deletelist/?team_id='+team_id);
}