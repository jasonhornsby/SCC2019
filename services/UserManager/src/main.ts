import { Server } from "@overnightjs/core";
import * as bodyParser from 'body-parser';
import cors from 'cors';
// Reflect metadata needed for TypeORM
import "reflect-metadata";
import { Connection, createConnection } from 'typeorm';
// Import swagger for Api Documentation generation
import swaggerUi from 'swagger-ui-express';
import * as swaggerDocument from '../swagger.json';
// Controllers
import { HelloController, LoginController, RegisterController, UserController } from './controllers';
import { Logger } from '@overnightjs/logger';

export class UserManagerServer extends Server {

    public static async start(port: number) {
        const s = new UserManagerServer();
        await s.setup();
        s.app.listen(port, () => {
            Logger.Info(`Server listening on port: ${port}`);
        });
        return s;
    }

    private db: Connection;

    constructor() {
        super(process.env.NODE_ENV === 'development');

        this.app.use(bodyParser.json());
        this.app.use(bodyParser.urlencoded({extended: true}));
        this.app.use(cors());

        // Only add swagger route if we are in dev mode
        if (process.env.NODE_ENV === 'development') {
            Logger.Info('Currently in Development Mode: init swagger...');
            this.app.use('/swagger', swaggerUi.serve, swaggerUi.setup(swaggerDocument))
        }
    }

    private async setup() {
        // Setup database
        this.db = await createConnection();
        Logger.Info(`Database connection established: ${ this.db.isConnected}`);

        // Add controllers
        const loginController = new LoginController(this.db);
        const registerController = new RegisterController(this.db);
        const userController = new UserController(this.db);
        const helloController = new HelloController();


        super.addControllers([loginController, registerController, helloController, userController]);
    }

}

const server = UserManagerServer.start(8000);
