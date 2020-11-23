import axios from 'axios';
const baseUrl = 'http://localhost:5000';

// 
export const blockchainService = {
    getAll,
    createWallet,
    createTransaction,
    mine,
    getTransactions
};




function getAll() {
    // console.log("test");
    const data = getData(`${baseUrl}/wallet`);
    console.log(data);
    return data;
}

async function getTransactions() {
    // console.log("test");
    const data = await getData(`${baseUrl}/transaction`);
    console.log(data);
    return data;
}

function mine() {
    // console.log("test");
    const data = getData(`${baseUrl}/mine`);
    console.log(data);
    return data;
}

async function createWallet(body){
    const resp = await post(`${baseUrl}/wallet/new`, body);
    console.log(resp);
    return resp;
}

function createTransaction(body){
    console.log(body);
    const resp = post(`${baseUrl}/transactions/new`, body);
    return resp;
}


async function getData(url){
    const res = await axios(url);
    return await res.data;
 };
 

// function get(url) {
//     axios.get(url)
//       .then(res => {
//         return(res.data)
//       })
// }

async function post(url, body) {
    const resp = await axios.post(url, body)
    .then( response => { return response })
    .catch( error => { return error });

    return await resp.data;
}