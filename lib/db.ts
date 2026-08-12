import { Pool } from "pg";

let neonPool: Pool | undefined;

function createPool() {
  const connectionString = process.env.DATABASE_URL;

  if (!connectionString) {
    throw new Error("DATABASE_URL is not set");
  }

  const url = new URL(connectionString);
  const useSsl = url.hostname !== "localhost" && url.hostname !== "127.0.0.1";

  return new Pool({
    connectionString,
    ssl: useSsl ? { rejectUnauthorized: false } : false,
  });
}

function getPool() {
  if (!neonPool) {
    neonPool = createPool();
  }

  return neonPool;
}

export async function executeQuery(text: string, values?: unknown[]) {
  return getPool().query(text, values);
}
