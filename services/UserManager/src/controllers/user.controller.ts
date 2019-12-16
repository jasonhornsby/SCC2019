import { Controller, Get } from '@overnightjs/core';
import { Connection } from 'typeorm';
import { Request, Response } from 'express';
import { User } from '../entities/user';

@Controller('auth/users')
export class UserController {

    constructor(private db: Connection) {}

    @Get('')
    public async getListOfUsers(req: Request, res: Response) {
        const userRepo = this.db.getRepository(User);
        const users = await userRepo.find();
        res.send(users);
    }

    @Get(':id')
    public async getUserById(req: Request, res: Response) {
        const id = req.params.id;
        const userRepo = this.db.getRepository(User);
        const user = await userRepo.findOne(id);

        if (!user) {
            res.status(404).send();
            return;
        }

        res.send(user);
    }

}
