module.exports = {
  directory: "dist",
  logFormat: "tiny",
  rewrite: ["conn", "djrf"].map(name => ({
    from: `/${name}/(.*)`,
    to: `http://bck-${name}:8000/$1`,
  })),
  spa: "index.html",
}
