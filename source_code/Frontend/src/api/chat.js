import { post, get} from './api';

export function inviteUserIntoChatGroup(receiver_id,group_id){
	var data=new FormData();
	data.append("receiver_id",receiver_id);
	data.append("group_id",group_id);
	return post('/api/chat/invite/',data);
}

export function createChatGroup(name){
	var data=new FormData();
	data.append("name",name);
	return post('/api/chat/create/',data);
}

export function breakupChatGroup(group_id){
	var data=new FormData();
	data.append("group_id",group_id);
	return post('/api/chat/break_up/',data);
}

export function exitChatGroup(group_id){
	var data=new FormData();
	data.append("group_id",group_id);
	return post('/api/chat/exit/',data);
}

export function getChatGroupHistory(group_id){
	return get('/api/chat/history/?group_id='+group_id);
}