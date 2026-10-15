export interface HttpResult {
  status: number;
  body: unknown;
}

export const json = (status: number, body: unknown): HttpResult => ({ status, body });

/** Log a failure without request bodies, addresses or secrets. */
export function logFailure(event: string, detail: Record<string, string | number | undefined>): void {
  console.error(JSON.stringify({ severity: "ERROR", event, ...detail }));
}
