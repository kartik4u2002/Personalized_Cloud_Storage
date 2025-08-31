# Use official Node.js image
FROM node:20-alpine

# Create app directory
WORKDIR /frontend

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all frontend files

# Expose port
EXPOSE 3000

# Start the server
CMD ["node", "server.js"]
