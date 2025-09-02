# Flask Blog with Environment Variables

This Flask blog application now uses environment variables for secure configuration management.

## Setup Instructions

1. **Copy the environment template:**
   ```
   copy .env.example .env
   ```

2. **Edit the .env file with your actual values:**
   - `SECRET_KEY`: Generate a secure random string (you can use `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `DATABASE_URI`: Set your database connection string
   - `FLASK_DEBUG`: Set to `True` for development, `False` for production
   - `PORT`: Port number for the Flask server (default: 5001)

3. **Example .env file:**
   ```
   SECRET_KEY=your-very-secure-secret-key-here
   DATABASE_URI=sqlite:///posts.db
   FLASK_DEBUG=True
   PORT=5001
   ```

## Environment Variables

### Required
- `SECRET_KEY`: Flask secret key for session security
- `DATABASE_URI`: Database connection string

### Optional
- `FLASK_DEBUG`: Enable/disable debug mode (default: False)
- `PORT`: Server port (default: 5001)

## Production Deployment

For production:
1. Set `FLASK_DEBUG=False`
2. Use a strong, randomly generated `SECRET_KEY`
3. Use a production database (PostgreSQL, MySQL, etc.) instead of SQLite
4. Ensure .env file is not committed to version control (already in .gitignore)

## Security Notes

- Never commit your .env file to version control
- The .env file is already excluded in .gitignore
- Use strong, unique secret keys in production
- Consider using a key management service for production deployments
