import { db, user } from "@/db";
import { eq } from "drizzle-orm";

export const getUserById = async (id: number) => {
  return db
    .select()
    .from(user)
    .where(eq(user.id, id))
    .then((users) => users[0]);
};

export const getUserByUsername = async (username: string) => {
  return db
    .select()
    .from(user)
    .where(eq(user.username, username))
    .then((users) => users[0]);
};
