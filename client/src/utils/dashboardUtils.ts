import { Socket } from "socket.io-client";

export function isSocket(obj: unknown): obj is Socket {
  return obj instanceof Socket;
}