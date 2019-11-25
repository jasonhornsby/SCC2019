import { Controller, Post } from '@overnightjs/core';
import { Request, Response } from 'express';
import { Connection } from 'typeorm';
import { User } from '../entities/user';
import { LoginError } from '../errors/login.error';
import { jwtManager } from '../util/jwtManager.util';

@Controller('login')
export class LoginController {

    constructor(private db: Connection) { }

    @Post()
    public async login(req: Request, res: Response) {
        const userRepo = this.db.getRepository(User);

        let user: User;

        try {
            user = await userRepo.findOneOrFail({
                username: req.body.username ,
            }, {
                select: ['password', 'username', 'id'],
            });
        } catch (e) {
            res.status(401).send(new LoginError());
            return;
        }

        const correctPassword = await user.checkPassword(req.body.password);

        if (!correctPassword) {
            res.status(401).send(new LoginError());
            return;
        }

        const jwtToken = await jwtManager.jwt({
            id: user.id,
            username: user.username,
        });

        res.send({
            id: user.id,
            username: user.username,
            token: jwtToken,
        });
    }

}
