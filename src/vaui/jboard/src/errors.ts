export class FetchError extends Error {
  code: string | null

  name: string

  url: string

  constructor({ err, res, url }: { err?: Error; res?: Response; url: URL }) {
    super(res ? res.statusText : err ? err.message : "")
    this.code = res ? res.status.toString() : null
    this.name = "FetchError"
    this.url = url.toString()
  }
}
