import { BaseEntity, Column, Entity, PrimaryGeneratedColumn } from 'typeorm';
import { compare } from 'bcrypt';

@Entity()
export class User extends BaseEntity {

    @PrimaryGeneratedColumn()
    public id: number;

    @Column()
    public username: string;

    @Column({ select: false })
    public password: string;

    public async checkPassword(password: string): Promise<boolean> {
        return await compare(password, this.password);
    }

}
