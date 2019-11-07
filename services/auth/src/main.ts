import { Server } from "@overnightjs/core";
import * as bodyParser from 'body-parser';
// Reflect metadata needed for TypeORM
import "reflect-metadata";
import { Connection, createConnection } from 'typeorm';
// Controllers
import { LoginController, RegisterController, UserController } from './controllers';
import { Logger } from '@overnightjs/logger';

export class AuthServer extends Server {

    public static async start(port: number) {
        const s = new AuthServer();
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
    }

    private async setup() {
        // Setup database
        this.db = await createConnection();
        Logger.Info(`Database connection established: ${ this.db.isConnected}`);

        // Add controllers
        const loginController = new LoginController(this.db);
        const registerController = new RegisterController(this.db);
        const userController = new UserController(this.db);

        super.addControllers([loginController, registerController, userController]);
    }

}

const server = AuthServer.start(8000);
