import { post, get} from './api';

export function createMessage(receiver_id,content){
	var data=new FormData();
	data.append("receiver_id",receiver_id);
	data.append("content",content);
	return post('/api/notification/create/',data);
}