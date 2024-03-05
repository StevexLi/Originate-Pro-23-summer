import { post, get} from './api';

export function userRister(username,password_1,password_2,email,vcode){
    var data=new FormData();
    data.append("username",username);
    data.append("password_1",password_1);
    data.append("password_2",password_2);
    data.append("email",email);
    data.append("vcode",vcode);
    return post('/api/user/register/',data);
}

export function userLogin(username,password){
    var data=new FormData();
    data.append("username",username);
    data.append("password",password);
    return post('/api/user/login/',data);
}

export function sendVCode(email,func){
    var data=new FormData();
    data.append("email",email);
    data.append("func",func);
    return post('/api/user/send_vcode/',data);
}

export function findPassword(email,vcode,password_1,password_2){
    var data=new FormData();
    data.append("email",email);
    data.append("vcode",vcode);
    data.append("password_1",password_1);
    data.append("password_2",password_2);
    return post('/api/user/find_password/',data);
}

export function updateUserInformation(username,first_name,last_name,gender,phone,introduction,icon){
	var data=new FormData();
	data.append("username",username);
	data.append("first_name",first_name);
	data.append("last_name",last_name);
	data.append("gender",gender);
	data.append("phone",phone);
	data.append("introduction",introduction);
	data.append("icon",icon);
    return post('/api/user/change_profile/',data);
}

export function getUserInformation(user_id){
	return get('/api/user/get_profile/?user_id='+user_id);
}

export function getUserGroup(){
    return get('/api/user/get_team/');
}

export function checkUserInGroup(user_id,team_id){
	return get('/api/user/check_in_team/?user_id='+user_id+'&team_id='+team_id);
}

export function getUserChatRoom(){
    return get('/api/user/get_group/');
}