import axios, { AxiosResponse } from 'axios';
import { IFile } from '@/models/file.model';
import { IFilesStore } from '@/store/files.store';

export const fileServiceURL = 'https://www.nanyte.design/api/files/files';

async function getFiles(): Promise<IFilesStore> {
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
