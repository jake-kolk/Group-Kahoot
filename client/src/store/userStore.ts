// src/store/userStore.ts

const TOKEN_KEY = "userToken"; // This is for storing the hosts game server auth token, seperate from db auth w/ cookies
// We need this because ws does not support credentials like axios

export function setUserToken(token: string): void {
  console.log("Token set to ", token);
  localStorage.setItem(TOKEN_KEY, token);
}

export function getUserToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function clearUserToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}
