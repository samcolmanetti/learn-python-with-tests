# Build the Honkit static site, then serve it with nginx.
# Dokploy: create an Application pointed at this repo, build type "Dockerfile". The container
# listens on port 80.

# ---- build stage ----
FROM node:20-alpine AS build
WORKDIR /app

# Install the book toolchain (honkit + plugins). The local "pagetoc" plugin is a file:
# dependency, so copy it in before installing.
COPY package.json package-lock.json ./
COPY tools ./tools
RUN npm install

# Build the site. Honkit reads SUMMARY.md / book.json and writes static HTML to _book.
COPY . .
RUN npx honkit build . _book

# ---- serve stage ----
FROM nginx:alpine
COPY --from=build /app/_book /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
