import { JwtManager } from '@overnightjs/jwt';

export const jwtManager = new JwtManager('secret', '10h');
