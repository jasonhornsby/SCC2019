import axios, { AxiosResponse } from 'axios';
import { IFile } from '@/models/file.model';

export const fileServiceURL = 'http://api.scc2019.local.app.garden/files';

async function getFiles(): Promise<IFile[]> {
    let response: AxiosResponse = await axios.get(fileServiceURL);

    return response.data;
}

async function getFile(id: number): Promise<IFile> {
    let response: AxiosResponse = await axios.get(fileServiceURL + "/" + id );
    return response.data;
}


export const fileService = {
    getFiles, getFile
};
