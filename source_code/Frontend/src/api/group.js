import { post, get} from './api';

export function createGroup(name,introduction){
	var data=new FormData();
	data.append("name",name);
	data.append("introduction",introduction);
    return post('/api/team/create/',data);
}

export function deleteGroup(team_id){
	var data=new FormData();
	data.append("team_id",team_id);
	return post('/api/team/break_up/',data);
}

export function changeAuth(user_id,team_id,op_code){
	var data=new FormData();
	data.append("user_id",user_id);
	data.append("team_id",team_id);
	data.append("op_code",op_code);
	return post('/api/team/change_auth/',data);
}

export function inviteMember(team_id,email){
	var data=new FormData();
	data.append("team_id",team_id);
	data.append("email",email);
	return post('/api/team/invite/',data);
}

export function getGroupInformation(team_id){
	return get('/api/team/get_info/?team_id='+team_id);
}

export function updateGroup(team_id,name,introduction,icon){
	var data=new FormData();
	data.append("team_id",team_id);
	data.append("name",name);
	data.append("introduction",introduction);
	data.append("icon",icon);
	return post('/api/team/change_profile/',data);
}