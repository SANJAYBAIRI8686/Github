FROM node:20-alpine AS base
WORKDIR /app

COPY frontend/package.json frontend/tsconfig.json frontend/next.config.mjs frontend/postcss.config.js frontend/tailwind.config.ts frontend/vitest.config.ts /app/
COPY frontend/app /app/app
COPY frontend/components /app/components
COPY frontend/lib /app/lib
COPY frontend/public /app/public
COPY frontend/middleware.ts /app/middleware.ts

RUN npm install
RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "start", "--", "-p", "3000"]