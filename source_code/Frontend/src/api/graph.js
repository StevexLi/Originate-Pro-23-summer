import { post, get} from './api';

export function createGraph(name,project_id,width){
	var data=new FormData();
	data.append("name",name);
	data.append("project_id",project_id);
	data.append("width",width);
	return post('/api/graph/create/',data);
}

export function deleteGraph(graph_id,project_id){
	var data=new FormData();
	data.append("graph_id",graph_id);
	data.append("project_id",project_id);
	return post('/api/graph/delete/',data);
}

export function getAGraph(graph_id,project_id){
	return get('/api/graph/getgraph/?graph_id='+graph_id+'&project_id='+project_id);
}

export function getAllGraph(project_id){
	return get('/api/graph/getgraphs/?project_id='+project_id);
}

export function saveGraph(graph_id,project_id,content,width,document){
	var data=new FormData();
	data.append("graph_id",graph_id);
	data.append("project_id",project_id);
	data.append("content",content);
	data.append("width",width);
	data.append("document",document);
	return post('/api/graph/save/',data);
}