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

export function emptyRestore(){
	var data=new FormData();
	return post('/api/project/empty/',data);
}

export function removeProject(project_id){
	var data=new FormData();
	data.append("project_id",project_id);
	return post('/api/project/remove/',data);
}

export function getProjectInformation(project_id){
	return get('/api/project/getinfo/?project_id='+project_id);
}

export function getRestoreList(team_id){
	return get('/api/project/get_deletelist/?team_id='+team_id);
}