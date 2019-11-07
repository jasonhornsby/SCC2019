import { BaseEntity, BeforeInsert, Column, Entity, PrimaryGeneratedColumn } from 'typeorm';
import { hash, compare } from 'bcrypt';

@Entity()
export class User extends BaseEntity {

    @PrimaryGeneratedColumn()
    public id: number;

    @Column()
    public username: string;

    @Column({ select: false })
    public password: string;

    @BeforeInsert()
    public async beforeInsert() {
        const saltRounds = 10;
        this.password = await hash(this.password, saltRounds);
    }

    public async checkPassword(password: string): Promise<boolean> {
        return await compare(password, this.password);
    }

}
