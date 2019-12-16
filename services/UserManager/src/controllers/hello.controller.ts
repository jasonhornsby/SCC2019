import { Controller, Get } from '@overnightjs/core';
import { Request, Response } from 'express';

@Controller('auth')
export class HelloController {
    @Get('')
    hello(req: Request, res: Response) {
        res.send('Hello world from User Service');
    }
}
