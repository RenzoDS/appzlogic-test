# frontend/Dockerfile

FROM node:18-alpine

# Set working directory in container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all source files
COPY . .

# Expose port (default for React apps is 3000)
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]
