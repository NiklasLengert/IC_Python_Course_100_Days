# TechShop - eCommerce Platform

A modern eCommerce website built with Flask featuring secure payment processing and responsive design.

## Features

- User authentication system with secure password hashing
- Product catalog with image support
- Shopping cart functionality
- Simulated payment processing (no actual charges)
- Order history and management
- Mobile-responsive design
- SQLite database backend

## Quick Start

1. Install dependencies:
   ```bash
   pip install flask stripe werkzeug
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Visit `http://127.0.0.1:5000` in your browser

## Project Structure

- `app.py` - Main Flask application
- `templates/` - HTML templates
- `static/` - Static assets (images, CSS, JS)
- `ecommerce.db` - SQLite database
- `ecommerce.db` - SQLite database (created automatically)
- `requirements.txt` - Python dependencies

## Database Schema

- **Users**: User accounts with authentication
- **Products**: Product catalog with pricing
- **Orders**: Order tracking and history
- **Order Items**: Individual items within orders

## Security Features

- Password hashing with Werkzeug
- Secure session management
- CSRF protection
- Input validation
- SQL injection prevention

## Payment Processing

The application uses Stripe for secure payment processing:
- Client-side card validation
- Server-side payment confirmation
- Order creation after successful payment
- Error handling for failed transactions

## Products

The application includes sample products across different categories:
- Electronics (headphones, gaming mouse, bluetooth speaker)
- Accessories (laptop stand, phone case)  
- Home & Office (coffee mug, desk lamp, notebook)

## Technologies

- Backend: Flask (Python)
- Database: SQLite  
- Payment: Stripe API (simulation mode)
- Frontend: HTML, CSS, JavaScript
- Security: Werkzeug password hashing

Built as a complete eCommerce platform with secure payment processing.
