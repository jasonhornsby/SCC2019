import axios, { AxiosResponse } from 'axios';
import { IFile } from '@/models/file.model';

async function getFiles(): Promise<IFile[]> {
    let response: AxiosResponse = await axios.get('http://localhost:5000/files');

    return response.data;
}

async function getFile(id: number): Promise<IFile> {
    let response: AxiosResponse = await axios.get(`http://localhost:5000/files/${ id }`);
    return response.data;
}


export const fileService = {
    getFiles, getFile
};
