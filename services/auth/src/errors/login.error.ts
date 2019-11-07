export class LoginError  {
    public message: string;

    constructor() {
        this.message = 'Login failed. Username or Password wrong';
    }
}
