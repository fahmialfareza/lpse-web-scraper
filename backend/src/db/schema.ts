import { integer, pgTable, varchar } from "drizzle-orm/pg-core";

export interface IUser {
  id: number;
  name: string;
  username: string;
  password?: string | null;
}

export const usersTable = pgTable("users", {
  id: integer().primaryKey().generatedAlwaysAsIdentity(),
  name: varchar({ length: 255 }).notNull(),
  username: varchar({ length: 255 }).notNull().unique(),
  password: varchar({ length: 255 }),
});
