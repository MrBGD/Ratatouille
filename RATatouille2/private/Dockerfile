FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY chall.py .

ENV PORT=5000
ENV PYTHONUNBUFFERED=1
ENV FLAG=nullctf{b3_c4r3full_wi7h_y0ur_ki7ch3n_R3my!}

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "chall.py"]