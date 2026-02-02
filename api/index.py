from app import create_app

# Create the Flask app instance
app = create_app()

# This is required for Vercel serverless
if __name__ == '__main__':
    app.run()