FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY chall.py .

ENV PORT=3000
ENV PYTHONUNBUFFERED=1
ENV FLAG=nullctf{n3v3r_run_4ny7hing_y0u_find_0n_7h3_n37}

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["python", "chall.py"]