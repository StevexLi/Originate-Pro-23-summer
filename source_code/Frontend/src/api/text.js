import { post, get} from './api';

export function createText(name,project_id,text_url){
	var data=new FormData();
	data.append("name",name);
    data.append("project_id",project_id);
	data.append("text_url",text_url);
    console.log(data);
	return post('/api/text/create/',data);
}

export function saveText(text_id,project_id,content){
	var data=new FormData();
	data.append("text_id",text_id);
	data.append("project_id",project_id);
	data.append("content",content);
	return post('/api/text/save/',data);
}

export function deleteText(text_id){
	var data=new FormData();
	data.append("text_id",text_id);
	return post('/api/text/delete/',data);
}

export function changeTextAuthority(text_id,project_id,is_shared,is_write){
	var data=new FormData();
	data.append("text_id",text_id);
	data.append("project_id",project_id);
	data.append("is_shared",is_shared);
	data.append("is_write",is_write);
	return post('/api/text/change_role/',data);
}

export function getAText(text_id,project_id){
	return get('/api/text/gettext/?text_id='+text_id+'&project_id='+project_id);
}

export function getAllText(project_id){
	return get('/api/text/gettexts/?project_id='+project_id);
}

export function getTextHistory(text_id,project_id){
	return get('/api/text/get_history/?text_id='+text_id+'&project_id='+project_id);
}