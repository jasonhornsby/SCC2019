import { Controller, Post } from '@overnightjs/core';
import { Request, Response } from 'express';
import { Connection } from 'typeorm';
import { User } from '../entities/user';
import { jwtManager } from '../util/jwtManager.util';
import { hash } from 'bcrypt';

@Controller('register/')
export class RegisterController {

    constructor(private db: Connection) { }

    @Post()
    private async newUser(req: Request, res: Response) {

        const userRepo = this.db.getRepository(User);

        const existingUserCheck = await userRepo.findOne({
            username: req.body.username,
        }, {
            select: ['password'],
        });

        if (existingUserCheck) {
            res.status(409).send();
            return;
        }

        const newUser = new User();
        newUser.username = req.body.username;
        newUser.password = await hash(req.body.password, 10);
        await userRepo.save(newUser);

        const jwtToken = await jwtManager.jwt({
            id: newUser.id,
            username: newUser.username,
        });

        res.status(201).send({
            id: newUser.id,
            username: newUser.username,
            token: jwtToken,
        });
    }

}
