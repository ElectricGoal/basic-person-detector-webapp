# Use the official Node.js Alpine image
FROM node:18-alpine

# Set the working directory
WORKDIR /frontend

# Copy the rest of the application code
COPY . .

RUN npm install && \
    npm run build

# Expose port 3000
EXPOSE 3000

# Start the Next.js application
CMD ["npm", "start"]