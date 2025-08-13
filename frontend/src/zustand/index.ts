import { TUser } from "@/models/user";
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

interface IStore {
  user: TUser | null;
  token?: string;
  setUser: (user: TUser) => void;
  setToken: (token: string) => void;
  logout: () => void;
}

const useStore = create<IStore>()(
  persist(
    (set) => ({
      user: null,
      token: undefined,
      setUser: (user: TUser) => set({ user }),
      setToken: (token: string) => set({ token }),
      logout: () => set({ user: null, token: undefined }),
    }),
    {
      name: "lpse-web-scraper-store",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ user: state.user, token: state.token }),
    }
  )
);

export default useStore;
