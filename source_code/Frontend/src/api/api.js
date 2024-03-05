import axios from 'axios';
import store from '@/store';
import { ElMessage } from 'element-plus';

export function post(url,data){
    return new Promise((resolve,reject)=>{
        axios.post('http://8.130.25.189'+url,data,{headers:{'Authorization': store.state.token}}).then(response=>
            {resolve(response.data)}).catch((error)=>{
                ElMessage({
                    message: "1网络连接失败",
                    grouping: true,
                    type: 'error',
                });
            });
    });
}

export function get(url){
    return new Promise((resolve,reject)=>{
        axios.get('http://8.130.25.189'+url,{headers:{"Authorization": store.state.token}}).then(response=>
            {resolve(response.data)}).catch((error)=>{
                ElMessage({
                    message: "网络连接失败",
                    grouping: true,
                    type: 'error',
                });
            });
    });
}